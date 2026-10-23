"""Exercise library, equipment-aware alternatives, and weekly program builder."""
from collections import OrderedDict

EQUIPMENT = OrderedDict([
    ("dumbbells", "Dumbbells"), ("barbell", "Barbell & rack"), ("bench", "Bench"),
    ("bands", "Resistance bands"), ("pullup_bar", "Pull-up bar"), ("cable", "Cable machine / lat pulldown"),
    ("leg_press", "Leg press machine"), ("chest_press", "Chest press machine"),
    ("leg_curl_ext", "Leg curl / extension machines"), ("treadmill", "Treadmill"), ("bike", "Stationary bike"),
    ("rower", "Rowing machine"), ("elliptical", "Elliptical"),
])
PRESETS = {"none": [], "home": ["dumbbells", "bands", "bench"], "gym": list(EQUIPMENT)}
INJURIES = OrderedDict([("knee", "Knee"), ("lower_back", "Lower back"), ("shoulder", "Shoulder"),
                        ("wrist", "Wrist / hand"), ("neck", "Neck"), ("hip", "Hip"), ("ankle", "Ankle / foot")])
DOW = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
DOW_FULL = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

EX = {}


def E(key, name, pattern, needs, stress, muscles, cue, kind="strength", timed=False):
    EX[key] = dict(key=key, name=name, pattern=pattern, needs=tuple(needs), stress=tuple(stress),
                   muscles=muscles, cue=cue, kind=kind, timed=timed)


# ---- squat
E("back_squat", "Barbell back squat", "squat", ["barbell"], ["knee", "lower_back", "hip"], "Quads, glutes",
  "Brace your core, sit down and back until thighs are parallel, drive through the mid-foot.")
E("leg_press", "Leg press", "squat", ["leg_press"], ["knee", "hip"], "Quads, glutes",
  "Feet shoulder-width, lower until knees are about 90°, press up without locking out.")
E("goblet_squat", "Goblet squat (dumbbell)", "squat", ["dumbbells"], ["knee"], "Quads, glutes",
  "Hold one dumbbell at your chest, elbows inside the knees, sit between your hips.")
E("box_squat", "Squat to a chair (bodyweight)", "squat", [], [], "Quads, glutes",
  "Sit back to a chair, touch lightly, stand up. Use a higher seat if the knees complain.")
E("split_squat", "Split squat (bodyweight)", "squat", [], ["knee", "hip"], "Quads, glutes",
  "Long stance, drop the back knee straight down, keep the front heel planted.")
E("step_up", "Step-up (sturdy step)", "squat", [], ["knee", "hip"], "Quads, glutes",
  "Place the whole foot on the step and stand tall; lower slowly.")
E("wall_sit", "Wall sit", "squat", [], ["knee"], "Quads",
  "Back flat on the wall, thighs parallel to the floor, hold.", timed=True)
E("leg_extension", "Leg extension machine", "squat", ["leg_curl_ext"], ["knee"], "Quads",
  "Pause for a second at the top, lower under control.")
# ---- hinge
E("romanian_deadlift", "Barbell Romanian deadlift", "hinge", ["barbell"], ["lower_back"], "Hamstrings, glutes",
  "Soft knees, push hips back with a flat back, bar slides down the thighs.")
E("db_rdl", "Dumbbell Romanian deadlift", "hinge", ["dumbbells"], ["lower_back"], "Hamstrings, glutes",
  "Soft knees, push hips back with a flat back, dumbbells slide down the thighs.")
E("hip_thrust_db", "Hip thrust (dumbbell on hips, back on bench)", "hinge", ["dumbbells", "bench"], [],
  "Glutes", "Chin tucked, drive through the heels, squeeze glutes at the top.")
E("glute_bridge", "Glute bridge", "hinge", [], [], "Glutes, hamstrings",
  "Feet flat, drive hips up, squeeze for a second at the top.")
E("single_leg_bridge", "Single-leg glute bridge", "hinge", [], [], "Glutes, hamstrings",
  "One foot on the floor, other leg extended; keep the hips level.")
E("leg_curl", "Leg curl machine", "hinge", ["leg_curl_ext"], [], "Hamstrings",
  "Curl smoothly, lower slowly for 3 seconds.")
E("band_pull_through", "Band pull-through", "hinge", ["bands"], [], "Glutes, hamstrings",
  "Anchor the band low behind you, hinge back, then squeeze the glutes to stand.")
E("hamstring_walkout", "Bridge walk-out", "hinge", [], [], "Hamstrings",
  "From a bridge, walk the feet away slowly and back.")
# ---- horizontal push
E("bench_press", "Barbell bench press", "hpush", ["barbell", "bench"], ["shoulder", "wrist"], "Chest, triceps",
  "Shoulder blades pinched, lower to mid-chest, press up.")
E("db_bench", "Dumbbell bench press", "hpush", ["dumbbells", "bench"], ["shoulder"], "Chest, triceps",
  "Elbows about 45° from the body, press up and slightly in.")
E("chest_press", "Chest press machine", "hpush", ["chest_press"], ["shoulder"], "Chest, triceps",
  "Set the seat so handles are at mid-chest; press without locking out.")
E("floor_press", "Dumbbell floor press", "hpush", ["dumbbells"], ["shoulder"], "Chest, triceps",
  "Lie on the floor, elbows rest lightly on the floor between reps.")
E("push_up", "Push-up", "hpush", [], ["wrist", "shoulder"], "Chest, triceps, core",
  "Body in one line, lower the chest to the floor, elbows about 45°.")
E("incline_push_up", "Incline push-up (hands on a counter or bench)", "hpush", [], ["wrist"], "Chest, triceps",
  "Hands on a stable surface; the higher it is, the easier.")
E("band_chest_press", "Band chest press", "hpush", ["bands"], ["shoulder"], "Chest, triceps",
  "Anchor the band behind you, press forward at chest height.")
# ---- vertical push & shoulders
E("overhead_press", "Barbell overhead press", "vpush", ["barbell"], ["shoulder", "lower_back", "neck"],
  "Shoulders, triceps", "Squeeze glutes, press the bar straight up past your face.")
E("db_shoulder_press", "Dumbbell shoulder press", "vpush", ["dumbbells"], ["shoulder", "neck"],
  "Shoulders, triceps", "Press up without arching the lower back.")
E("pike_push_up", "Pike push-up", "vpush", [], ["shoulder", "wrist", "neck"], "Shoulders, triceps",
  "Hips high, lower the top of your head toward the floor between your hands.")
E("lateral_raise", "Dumbbell lateral raise", "delts", ["dumbbells"], ["shoulder"], "Side shoulders",
  "Light weights, lift to shoulder height with a slight bend in the elbows.")
E("band_lateral_raise", "Band lateral raise", "delts", ["bands"], ["shoulder"], "Side shoulders",
  "Stand on the band, raise the arms to shoulder height.")
# ---- horizontal pull
E("seated_row", "Seated cable row", "hpull", ["cable"], [], "Upper back, biceps",
  "Chest tall, pull the elbows back and squeeze the shoulder blades.")
E("db_row", "One-arm dumbbell row", "hpull", ["dumbbells"], [], "Upper back, biceps",
  "Hand on a bench or thigh, flat back, pull the elbow toward the hip.")
E("band_row", "Band row", "hpull", ["bands"], [], "Upper back, biceps",
  "Anchor the band at chest height, pull the elbows back.")
E("prone_ytw", "Prone Y-T-W raises", "rear", [], [], "Upper back, rear shoulders",
  "Lie face down and raise the arms into Y, T and W shapes; slow and light.")
# ---- vertical pull
E("lat_pulldown", "Lat pulldown", "vpull", ["cable"], [], "Lats, biceps",
  "Pull the bar to the upper chest, lead with the elbows.")
E("pull_up", "Pull-up (or assisted)", "vpull", ["pullup_bar"], ["shoulder"], "Lats, biceps",
  "Start from a full hang, pull the chest to the bar; use a band for assistance.")
E("band_pulldown", "Band lat pulldown", "vpull", ["bands"], [], "Lats, biceps",
  "Anchor the band overhead and pull the elbows down to your ribs.")
# ---- rear delts / posture
E("face_pull", "Cable face pull", "rear", ["cable"], [], "Rear shoulders, upper back",
  "Pull the rope to the face, elbows high, rotate the hands outward.")
E("band_face_pull", "Band face pull / pull-apart", "rear", ["bands"], [], "Rear shoulders, upper back",
  "Pull the band toward the face, elbows high.")
# ---- arms
E("biceps_curl", "Dumbbell biceps curl", "arms", ["dumbbells"], [], "Biceps", "Elbows pinned to the sides.")
E("band_curl", "Band biceps curl", "arms", ["bands"], [], "Biceps", "Stand on the band and curl.")
E("towel_curl", "Towel isometric curl", "arms", [], [], "Biceps",
  "Stand on a towel, pull up on the ends as hard as you can for 5–10 seconds.", timed=True)
E("triceps_pushdown", "Cable triceps pushdown", "arms", ["cable"], [], "Triceps",
  "Elbows pinned, press down until the arms are straight.")
E("band_pushdown", "Band triceps pushdown", "arms", ["bands"], [], "Triceps",
  "Anchor the band overhead and press down.")
E("close_push_up", "Close-grip push-up", "arms", [], ["wrist", "shoulder"], "Triceps, chest",
  "Hands under the shoulders, elbows brushing the ribs.")
E("bench_dip", "Chair / bench dip", "arms", [], ["shoulder", "wrist"], "Triceps",
  "Hands on a stable seat, lower until the elbows reach 90°.")
# ---- core
E("plank", "Plank", "core", [], ["shoulder"], "Core", "Squeeze glutes and abs, no sagging hips.", timed=True)
E("side_plank", "Side plank", "core", [], ["shoulder"], "Obliques", "Stack the feet, lift the hips.", timed=True)
E("dead_bug", "Dead bug", "core", [], [], "Deep core", "Lower back stays pressed into the floor; move slowly.")
E("bird_dog", "Bird dog", "core", [], [], "Core, glutes", "Reach opposite arm and leg, keep the hips level.")
E("pallof_press", "Pallof press (cable)", "core", ["cable"], [], "Core",
  "Press the handle straight out and resist the rotation.")
E("band_pallof", "Band Pallof press", "core", ["bands"], [], "Core",
  "Anchor the band to the side, press out and resist the pull.")
E("hanging_knee_raise", "Hanging knee raise", "core", ["pullup_bar"], ["shoulder"], "Lower abs",
  "Hang tall, lift the knees without swinging.")
E("reverse_crunch", "Reverse crunch", "core", [], [], "Lower abs", "Curl the hips off the floor, slowly.")
E("calf_raise", "Standing calf raise", "calves", [], ["ankle"], "Calves", "Full stretch at the bottom, pause at the top.")
# ---- cardio
E("treadmill", "Treadmill incline walk", "cardio", ["treadmill"], ["ankle"], "Heart & legs",
  "Incline 4–8%, speed that lets you talk in full sentences.", kind="cardio")
E("bike", "Stationary bike", "cardio", ["bike"], [], "Heart & legs",
  "Steady effort where you can still talk in full sentences.", kind="cardio")
E("rower", "Rowing machine", "cardio", ["rower"], ["lower_back"], "Heart & full body",
  "Drive with the legs first, easy pace.", kind="cardio")
E("elliptical", "Elliptical", "cardio", ["elliptical"], [], "Heart & legs", "Smooth and steady pace.", kind="cardio")
E("brisk_walk", "Brisk walk (indoor mall or early morning outdoors)", "cardio", [], [], "Heart & legs",
  "Fast enough to raise your breathing but still able to talk.", kind="cardio")
E("stair_climb", "Stair climbing", "cardio", [], ["knee", "hip"], "Heart & legs",
  "Steady pace, use the handrail.", kind="cardio")
E("step_circuit", "Low-impact step circuit (marching, side steps, punches)", "cardio", [], [], "Heart & full body",
  "Keep moving at a talkable pace; no jumping.", kind="cardio")
# ---- mobility (desk reset)
E("hip_flexor_stretch", "Kneeling hip-flexor stretch", "mobility", [], [], "Hips", "30 s each side; squeeze the glute.",
  kind="mobility", timed=True)
E("thoracic_rotation", "Open-book thoracic rotation", "mobility", [], [], "Upper back",
  "8 slow reps each side, follow your hand with your eyes.", kind="mobility")
E("cat_cow", "Cat–cow", "mobility", [], [], "Spine", "8 slow reps.", kind="mobility")
E("doorway_chest_stretch", "Doorway chest stretch", "mobility", [], [], "Chest, front shoulders",
  "30 s each side.", kind="mobility", timed=True)
E("chin_tuck", "Chin tucks", "mobility", [], ["neck"], "Neck posture", "8 reps, glide the chin straight back.",
  kind="mobility")
E("wall_angel", "Wall angels", "mobility", [], ["shoulder"], "Upper back, shoulders",
  "8 slow reps with back and arms on the wall.", kind="mobility")

ALTS = {
    "back_squat": ["leg_press", "goblet_squat", "split_squat", "box_squat", "wall_sit"],
    "leg_press": ["goblet_squat", "back_squat", "split_squat", "box_squat", "step_up"],
    "goblet_squat": ["leg_press", "split_squat", "box_squat", "step_up"],
    "box_squat": ["goblet_squat", "split_squat", "wall_sit", "glute_bridge"],
    "split_squat": ["goblet_squat", "step_up", "box_squat", "leg_press", "wall_sit"],
    "step_up": ["split_squat", "goblet_squat", "box_squat", "leg_press"],
    "wall_sit": ["box_squat", "glute_bridge"],
    "leg_extension": ["split_squat", "wall_sit", "goblet_squat", "box_squat"],
    "romanian_deadlift": ["db_rdl", "hip_thrust_db", "glute_bridge", "band_pull_through", "single_leg_bridge"],
    "db_rdl": ["romanian_deadlift", "hip_thrust_db", "band_pull_through", "single_leg_bridge", "glute_bridge"],
    "hip_thrust_db": ["glute_bridge", "single_leg_bridge", "db_rdl", "band_pull_through"],
    "glute_bridge": ["single_leg_bridge", "hamstring_walkout", "band_pull_through"],
    "single_leg_bridge": ["glute_bridge", "hamstring_walkout"],
    "leg_curl": ["db_rdl", "hamstring_walkout", "single_leg_bridge", "glute_bridge"],
    "band_pull_through": ["glute_bridge", "single_leg_bridge"],
    "hamstring_walkout": ["glute_bridge", "single_leg_bridge"],
    "bench_press": ["chest_press", "db_bench", "floor_press", "push_up", "band_chest_press"],
    "db_bench": ["chest_press", "bench_press", "floor_press", "push_up", "band_chest_press"],
    "chest_press": ["db_bench", "floor_press", "bench_press", "push_up", "band_chest_press"],
    "floor_press": ["push_up", "band_chest_press", "incline_push_up"],
    "push_up": ["incline_push_up", "floor_press", "band_chest_press", "chest_press"],
    "incline_push_up": ["push_up", "floor_press", "band_chest_press"],
    "band_chest_press": ["push_up", "incline_push_up", "floor_press"],
    "overhead_press": ["db_shoulder_press", "pike_push_up", "band_lateral_raise"],
    "db_shoulder_press": ["overhead_press", "pike_push_up", "lateral_raise", "band_lateral_raise"],
    "pike_push_up": ["db_shoulder_press", "lateral_raise", "band_lateral_raise", "prone_ytw"],
    "lateral_raise": ["band_lateral_raise", "db_shoulder_press", "pike_push_up", "prone_ytw"],
    "band_lateral_raise": ["lateral_raise", "pike_push_up", "prone_ytw"],
    "seated_row": ["db_row", "band_row", "prone_ytw"],
    "db_row": ["seated_row", "band_row", "prone_ytw"],
    "band_row": ["db_row", "seated_row", "prone_ytw"],
    "lat_pulldown": ["pull_up", "band_pulldown", "db_row", "band_row", "prone_ytw"],
    "pull_up": ["lat_pulldown", "band_pulldown", "db_row", "band_row", "prone_ytw"],
    "band_pulldown": ["lat_pulldown", "pull_up", "db_row", "band_row", "prone_ytw"],
    "face_pull": ["band_face_pull", "prone_ytw"],
    "band_face_pull": ["face_pull", "prone_ytw"],
    "prone_ytw": ["band_face_pull", "face_pull"],
    "biceps_curl": ["band_curl", "towel_curl"],
    "band_curl": ["biceps_curl", "towel_curl"],
    "towel_curl": ["band_curl", "biceps_curl"],
    "triceps_pushdown": ["band_pushdown", "close_push_up", "bench_dip"],
    "band_pushdown": ["triceps_pushdown", "close_push_up", "bench_dip"],
    "close_push_up": ["bench_dip", "band_pushdown", "triceps_pushdown"],
    "bench_dip": ["close_push_up", "band_pushdown", "triceps_pushdown"],
    "plank": ["dead_bug", "bird_dog", "side_plank"],
    "dead_bug": ["bird_dog", "plank", "reverse_crunch"],
    "bird_dog": ["dead_bug", "plank"],
    "side_plank": ["plank", "bird_dog", "dead_bug"],
    "pallof_press": ["band_pallof", "dead_bug", "plank"],
    "band_pallof": ["pallof_press", "dead_bug", "plank"],
    "hanging_knee_raise": ["reverse_crunch", "dead_bug", "plank"],
    "reverse_crunch": ["dead_bug", "plank", "bird_dog"],
    "treadmill": ["brisk_walk", "bike", "elliptical", "step_circuit"],
    "bike": ["elliptical", "treadmill", "brisk_walk", "step_circuit"],
    "rower": ["bike", "elliptical", "treadmill", "brisk_walk", "step_circuit"],
    "elliptical": ["bike", "treadmill", "brisk_walk", "step_circuit"],
    "brisk_walk": ["step_circuit", "treadmill", "bike", "elliptical"],
    "stair_climb": ["brisk_walk", "bike", "step_circuit"],
    "step_circuit": ["brisk_walk", "treadmill", "bike"],
}
PATTERN_FALLBACK = {
    "squat": ["box_squat", "glute_bridge"], "hinge": ["glute_bridge", "single_leg_bridge"],
    "hpush": ["incline_push_up", "floor_press"], "vpush": ["band_lateral_raise", "prone_ytw"],
    "hpull": ["prone_ytw", "band_row"], "vpull": ["prone_ytw", "db_row"], "arms": ["towel_curl", "band_curl"],
    "rear": ["prone_ytw"], "core": ["dead_bug", "bird_dog", "plank"], "delts": ["prone_ytw"],
    "calves": [], "cardio": ["brisk_walk", "step_circuit"],
}
BEGINNER_MAP = {"back_squat": "leg_press", "bench_press": "chest_press", "romanian_deadlift": "db_rdl",
                "overhead_press": "db_shoulder_press", "pull_up": "lat_pulldown"}

SESSIONS = {
    2: [("Full body A", ["back_squat", "bench_press", "seated_row", "romanian_deadlift", "face_pull", "plank"]),
        ("Full body B", ["leg_press", "overhead_press", "lat_pulldown", "hip_thrust_db", "biceps_curl", "dead_bug"])],
    3: [("Full body A", ["back_squat", "bench_press", "seated_row", "romanian_deadlift", "face_pull", "plank"]),
        ("Full body B", ["goblet_squat", "db_shoulder_press", "lat_pulldown", "hip_thrust_db", "biceps_curl", "dead_bug"]),
        ("Full body C", ["split_squat", "push_up", "db_row", "leg_curl", "triceps_pushdown", "side_plank"])],
    4: [("Upper A", ["bench_press", "seated_row", "db_shoulder_press", "lat_pulldown", "biceps_curl", "triceps_pushdown"]),
        ("Lower A", ["back_squat", "romanian_deadlift", "leg_curl", "calf_raise", "plank", "dead_bug"]),
        ("Upper B", ["db_bench", "pull_up", "lateral_raise", "db_row", "face_pull", "close_push_up"]),
        ("Lower B", ["goblet_squat", "hip_thrust_db", "split_squat", "leg_curl", "calf_raise", "side_plank"])],
}
LAYOUT = {2: ["Mon", "Thu"], 3: ["Mon", "Wed", "Fri"], 4: ["Mon", "Tue", "Thu", "Fri"]}
CARDIO_DAYS = {2: ["Tue", "Sat"], 3: ["Tue", "Sat"], 4: ["Wed", "Sat"]}
CARDIO_PREF = ["bike", "treadmill", "elliptical", "brisk_walk", "step_circuit"]
WARMUP = ["hip_flexor_stretch", "thoracic_rotation", "cat_cow", "glute_bridge", "chin_tuck"]
COOLDOWN = ["doorway_chest_stretch", "hip_flexor_stretch", "wall_angel"]
COMPOUND = {"squat", "hinge", "hpush", "vpush", "hpull", "vpull"}


def usable(key, equip, injuries):
    ex = EX[key]
    return all(n in equip for n in ex["needs"]) and not (set(ex["stress"]) & set(injuries))


def chain(key):
    """All alternatives reachable from key, in order of preference."""
    seen, order, queue = {key}, [], [key]
    while queue:
        cur = queue.pop(0)
        for a in ALTS.get(cur, []):
            if a not in seen:
                seen.add(a)
                order.append(a)
                queue.append(a)
    for a in PATTERN_FALLBACK.get(EX[key]["pattern"], []):
        if a not in seen:
            seen.add(a)
            order.append(a)
    return order


def resolve(key, equip, injuries, taken=()):
    """Best usable exercise for `key`. Returns (resolved_key | None, swapped)."""
    if usable(key, equip, injuries) and key not in taken:
        return key, False
    for a in chain(key):
        if usable(a, equip, injuries) and a not in taken:
            return a, True
    return None, True


def alternatives(key, equip, injuries, limit=4):
    """Alternatives for an exercise whose equipment is unavailable right now."""
    ex = EX[key]
    out = []
    for a in chain(key):
        if not usable(a, equip, injuries):
            continue
        if set(EX[a]["needs"]) & set(ex["needs"]):
            continue
        out.append(a)
        if len(out) >= limit:
            break
    return out


def prescribe(key, goal, level, light):
    ex = EX[key]
    p = ex["pattern"]
    if ex["kind"] == "cardio":
        return {}
    if ex["timed"]:
        return dict(sets=2 if (level == "beginner" or light) else 3, reps="30–45 s", rest=45)
    if p in COMPOUND:
        if light:
            return dict(sets=2, reps="12–15", rest=60)
        if goal == "lean_gain":
            return dict(sets=3 if level == "beginner" else 4, reps="8–12" if level == "beginner" else "6–10", rest=120)
        if goal == "fat_loss":
            return dict(sets=3, reps="10–12", rest=75)
        return dict(sets=3, reps="8–12", rest=90)
    if p == "core":
        return dict(sets=2, reps="8–12 / side" if key in ("dead_bug", "bird_dog") else "12–15", rest=45)
    return dict(sets=2 if (level == "beginner" or light) else 3, reps="12–15", rest=60)


def cardio_minutes(goal, level, light):
    base = {"fat_loss": 35, "recomp": 30, "lean_gain": 25, "general": 20}[goal]
    if level == "beginner" or light:
        return "20 min, add 5 min each week up to %d" % (base if not light else 30)
    return f"{base} min"


def card(key, equip, injuries, goal, level, light, swapped_from=None, equip_all=None, injuries_all=None):
    ex = EX[key]
    alts = alternatives(key, equip_all if equip_all is not None else equip, injuries)
    d = dict(key=key, name=ex["name"], muscles=ex["muscles"], cue=ex["cue"], kind=ex["kind"], timed=ex["timed"],
             swapped_from=EX[swapped_from]["name"] if swapped_from else None,
             alts=[dict(key=a, name=EX[a]["name"]) for a in alts])
    d.update(prescribe(key, goal, level, light))
    return d


def build_program(goal, level, strength_days, equip, injuries, light_only=False, missing=()):
    """Weekly program. `missing` = equipment unavailable right now (e.g. machine busy / broken)."""
    equip_eff = set(equip) - set(missing)
    injuries = set(injuries)
    strength_days = strength_days if strength_days in SESSIONS else 3
    if light_only:
        strength_days = min(strength_days, 3)
    templates = SESSIONS[strength_days]
    s_days = LAYOUT[strength_days]
    n_cardio = 1 if light_only else {"fat_loss": 2, "recomp": 2, "lean_gain": 1, "general": 1}[goal]
    c_days = CARDIO_DAYS[strength_days][:n_cardio]
    cmin = cardio_minutes(goal, level, light_only)
    days = []
    for i, dow in enumerate(DOW):
        entry = dict(dow=dow, index=i, full=DOW_FULL[i])
        if dow in s_days:
            title, keys = templates[s_days.index(dow)]
            exercises, taken = [], set()
            for k in keys:
                if level == "beginner":
                    k = BEGINNER_MAP.get(k, k)
                r, swapped = resolve(k, equip_eff, injuries, taken)
                if r is None:
                    continue
                taken.add(r)
                exercises.append(card(r, equip_eff, injuries, goal, level, light_only,
                                      swapped_from=k if swapped else None, equip_all=equip_eff))
            entry.update(type="strength", title=title, exercises=exercises, session_key=f"s{i}")
        elif dow in c_days:
            pick = next((c for c in CARDIO_PREF if usable(c, equip_eff, injuries)), None) or "brisk_walk"
            if not usable(pick, equip_eff, injuries):
                pick = "step_circuit"
            c = card(pick, equip_eff, injuries, goal, level, light_only, equip_all=equip_eff)
            c.update(minutes=cmin)
            entry.update(type="cardio", title="Zone 2 cardio", exercises=[c], session_key=f"c{i}")
        elif dow == "Sun":
            entry.update(type="rest", title="Rest & easy walk", exercises=[], session_key=f"r{i}")
        else:
            entry.update(type="recovery", title="Active recovery", exercises=[], session_key=f"a{i}")
        days.append(entry)

    def mob(keys):
        out = []
        for k in keys:
            if set(EX[k]["stress"]) & injuries:
                continue
            out.append(dict(key=k, name=EX[k]["name"], cue=EX[k]["cue"]))
        return out

    return dict(days=days, warmup=mob(WARMUP), cooldown=mob(COOLDOWN), cardio_minutes=cmin)


def parse_top_reps(reps_text):
    """Upper bound from a prescription such as '8–12' or '12–15'."""
    import re
    nums = [int(x) for x in re.findall(r"\d+", reps_text or "")]
    return max(nums[:2]) if nums else None


def progression_hint(last_reps, last_weight, rep_range):
    import re
    top = parse_top_reps(rep_range)
    reps = [int(x) for x in re.findall(r"\d+", last_reps or "")]
    if not top or not reps:
        return None
    if min(reps) >= top:
        if last_weight:
            return f"You hit {top} reps on every set. Try {last_weight + 2.5:g} kg today."
        return "You hit the top of the rep range on every set. Make it harder (slower tempo or a harder variation)."
    return f"Aim for {top} reps on every set at the same load before adding weight."
