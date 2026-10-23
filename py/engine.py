"""Goal and nutrition-target logic. Everything is derived from the latest body-composition report."""
from datetime import date, datetime

ACTIVITY = {
    "sedentary": (1.2, "Desk job, little exercise"),
    "light": (1.375, "Desk job + 1–3 workouts a week"),
    "moderate": (1.55, "Desk job + 3–5 workouts a week"),
}

GOALS = {
    "fat_loss": dict(label="Lose body fat", short="Fat loss", pct=-0.20, protein_per_lbm=2.4, steps=8000, cardio=2),
    "recomp": dict(label="Recomposition: lose fat and build muscle", short="Recomposition",
                   pct=-0.08, protein_per_lbm=2.2, steps=8000, cardio=2),
    "lean_gain": dict(label="Build lean muscle", short="Lean gain", pct=0.08, protein_per_lbm=2.0, steps=7000, cardio=1),
    "general": dict(label="General fitness (gentle)", short="General fitness", pct=0.0, protein_per_lbm=1.8,
                    steps=6000, cardio=1),
}

CONDITIONS = {
    "diabetes": "Diabetes / pre-diabetes",
    "hypertension": "High blood pressure",
    "heart": "Heart condition",
    "chest_pain": "Chest pain or dizziness during exercise",
    "kidney": "Kidney disease",
    "thyroid": "Thyroid condition",
    "pregnant": "Pregnant or breastfeeding",
    "eating_disorder": "History of an eating disorder",
}


def csv(s):
    return [x.strip() for x in (s or "").split(",") if x.strip()]


def age_from(birth_date, today=None):
    today = today or date.today()
    try:
        b = datetime.strptime(birth_date, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        return None
    return today.year - b.year - ((today.month, today.day) < (b.month, b.day))


def safety_flags(profile):
    cond = set(csv(profile.get("conditions")))
    f = dict(no_targets=False, protein_cap_per_kg=None, light_only=False, warnings=[], low_sodium=False)
    if "pregnant" in cond:
        f["no_targets"] = True
        f["light_only"] = True
        f["warnings"].append("Pregnancy / breastfeeding: calorie and weight-loss targets are switched off. "
                             "Please follow the advice of your doctor or midwife; training is limited to gentle sessions.")
    if "eating_disorder" in cond:
        f["no_targets"] = True
        f["warnings"].append("Because of your history, this app will not set calorie or weight targets. "
                             "Please follow the plan agreed with your clinician or dietitian. Training stays gentle and "
                             "is not framed around weight loss.")
        f["light_only"] = True
    if "kidney" in cond:
        f["protein_cap_per_kg"] = 0.8
        f["warnings"].append("Kidney disease: protein is capped at 0.8 g per kg body weight until your doctor or "
                             "dietitian says otherwise. Please have them review this plan.")
    if "heart" in cond or "chest_pain" in cond:
        f["light_only"] = True
        f["warnings"].append("Heart symptoms or condition: get your doctor's clearance before starting. Sessions are "
                             "kept light (you should be able to hold a conversation). Stop and seek care for chest "
                             "pain, dizziness or unusual breathlessness.")
    if "hypertension" in cond:
        f["low_sodium"] = True
        f["warnings"].append("High blood pressure: keep salt, pickles and processed meats low, avoid breath-holding "
                             "on heavy lifts, and check with your doctor before intense training.")
    if "diabetes" in cond:
        f["warnings"].append("Diabetes: keep carbohydrate portions consistent across meals and talk to your doctor "
                             "before changing your diet or exercise if you take insulin or tablets.")
    if "thyroid" in cond:
        f["warnings"].append("Thyroid condition: energy needs can differ from the estimate below; adjust with your doctor.")
    return f


def _fat_loss_at(sex, age):
    base = 22 if sex == "male" else 30
    if age is not None:
        base += 4 if age >= 60 else 2 if age >= 40 else 0
    return base


def _lean_gain_below(sex, age):
    base = 15 if sex == "male" else 22
    if age is not None and age >= 60:
        base += 2
    return base


def muscle_pct(report):
    if report.get("muscle_kg") and report.get("weight_kg"):
        return report["muscle_kg"] / report["weight_kg"] * 100
    return None


def decide_goal(profile, report, safety, age=None):
    """Return dict(key, label, reasons[], low_muscle). Goal is ALWAYS derived from the body-composition report."""
    sex = profile.get("sex") or "male"
    bf = report["body_fat_pct"]
    visc = report.get("visceral_level")
    mp = muscle_pct(report)
    low_muscle = bool(mp is not None and mp < (36 if sex == "male" else 28))
    fl, lg = _fat_loss_at(sex, age), _lean_gain_below(sex, age)
    reasons = [f"Your body fat is {bf:g}% (fat-loss zone starts at {fl}%, lean-gain zone is below {lg}% "
               f"for your sex and age)."]
    if safety["no_targets"]:
        key = "general"
        reasons.append("A safety setting on your profile switches off weight targets.")
    elif visc is not None and visc >= 10 and bf >= lg:
        key = "fat_loss"
        reasons.append(f"Visceral fat level is {visc:g} (10 or higher is considered high), so reducing it is the priority.")
    elif bf >= fl:
        key = "fat_loss"
        reasons.append("Body fat is above the healthy range, so the plan uses a moderate calorie deficit with high "
                       "protein and resistance training to protect muscle.")
    elif bf >= lg:
        key = "recomp"
        reasons.append("Body fat is in a middle range: a small deficit, high protein and strength training lets you "
                       "lose fat while building muscle.")
    else:
        key = "lean_gain"
        reasons.append("Body fat is already low, so the plan uses a small surplus to build muscle without adding much fat.")
    if low_muscle and not safety["no_targets"]:
        reasons.append(f"Skeletal muscle is only {mp:.0f}% of your weight, which is low, so protein is raised and "
                       "strength training is the top priority.")
    return dict(key=key, label=GOALS[key]["label"], short=GOALS[key]["short"], reasons=reasons,
                low_muscle=low_muscle, fat_loss_at=fl, lean_gain_below=lg)


def compute_targets(profile, report, goal, safety, steps_avg=None, kcal_adjust=0):
    if safety["no_targets"]:
        return None
    sex = profile.get("sex") or "male"
    weight, bf = report["weight_kg"], report["body_fat_pct"]
    lbm = weight * (1 - bf / 100)
    if report.get("bmr_kcal"):
        bmr, bmr_src = report["bmr_kcal"], "your body-composition scan"
    else:
        bmr, bmr_src = 370 + 21.6 * lbm, "calculated from your lean mass (Katch-McArdle)"
    factor = ACTIVITY.get(profile.get("activity"), ACTIVITY["sedentary"])[0]
    tdee = bmr * factor
    g = GOALS[goal["key"]]
    kcal = tdee * (1 + g["pct"]) + (kcal_adjust or 0)
    floor = max(1200 if sex == "female" else 1500, 0.9 * bmr)
    floored = False
    if g["pct"] < 0 and kcal < floor:
        kcal, floored = floor, True
    kcal = int(round(kcal / 10) * 10)

    ppl = g["protein_per_lbm"] + (0.2 if goal.get("low_muscle") else 0)
    protein = ppl * lbm
    protein = max(protein, 1.2 * weight)
    protein = min(protein, 2.4 * weight)
    if safety["protein_cap_per_kg"]:
        protein = min(protein, safety["protein_cap_per_kg"] * weight)
    protein = int(round(protein / 5) * 5)
    fat = max(kcal * 0.25 / 9, 0.7 * lbm)
    carbs = (kcal - 4 * protein - 9 * fat) / 4
    if carbs < 100:
        carbs = 100
        fat = max((kcal - 4 * protein - 400) / 9, 0.5 * lbm)
    fat, carbs = int(round(fat / 5) * 5), int(round(carbs / 5) * 5)
    fiber = int(round(max(25, 14 * kcal / 1000)))
    water = int(round(weight * 35 / 100) * 100)

    base_steps = g["steps"]
    steps = base_steps if steps_avg is None else int(min(base_steps, max(5000, round((steps_avg + 1500) / 500) * 500)))
    return dict(kcal=kcal, protein=protein, carbs=carbs, fat=fat, fiber=fiber, water_ml=water,
                bmr=int(round(bmr)), bmr_src=bmr_src, tdee=int(round(tdee)), lbm=round(lbm, 1),
                weekly_change_kg=round((kcal - tdee) * 7 / 7700, 2), steps_target=steps,
                steps_goal=base_steps, floored=floored, kcal_adjust=kcal_adjust or 0, activity_factor=factor)


def mifflin_note():
    return "Estimates are a starting point. The weekly review adjusts them to your real progress."
