"""Meal-plan generator: picks recipes per slot and scales portions to hit calorie and macro targets."""
import hashlib
import json
import random

from foods import (AISLE_ORDER, ALLERGENS, BY_ID, DIET_RANK, FOODS, LAYOUTS, RECIPES, fmt_item)


class PlanError(Exception):
    pass


def parse_exclusions(text):
    tokens, words = set(), []
    for part in (text or "").split(","):
        part = part.strip().lower()
        if not part:
            continue
        if part in ALLERGENS:
            tokens.add(part)
        elif len(part) >= 3:
            words.append(part)
    return tokens, words


def pool_for(cat, diet, tokens, words):
    rank = DIET_RANK.get(diet, 3)
    return [r for r in RECIPES
            if r["cat"] == cat and r["rank"] <= rank and not (r["alg"] & tokens)
            and not any(w in r["text"] for w in words)]


def _scaled(recipe, s):
    items = []
    for key, g in recipe["items"]:
        st = FOODS[key]["step"]
        items.append((key, max(st, int(round(g * s / st)) * st)))
    return items


def _macros(items):
    t = dict(kcal=0.0, p=0.0, c=0.0, f=0.0, fib=0.0)
    for key, g in items:
        fd = FOODS[key]
        t["kcal"] += fd["kcal"] * g / 100
        t["p"] += fd["p"] * g / 100
        t["c"] += fd["c"] * g / 100
        t["f"] += fd["f"] * g / 100
        t["fib"] += fd["fib"] * g / 100
    return t


def _clip(x, lo, hi):
    return max(lo, min(hi, x))


def _meal(slot, label, recipe, s):
    items = _scaled(recipe, s)
    m = _macros(items)
    return dict(slot=slot, label=label, recipe_id=recipe["id"], name=recipe["name"], note=recipe["note"],
                scale=round(s, 3), items=[fmt_item(k, g) for k, g in items], raw_items=items,
                kcal=round(m["kcal"]), p=round(m["p"]), c=round(m["c"]), f=round(m["f"]), fib=round(m["fib"]))


def _totals(meals):
    return {k: sum(m[k] for m in meals) for k in ("kcal", "p", "c", "f", "fib")}


def build_day(targets, meals_per_day, diet, exclusions, rng, recent=None, avoid=None, trials=90):
    layout = LAYOUTS[meals_per_day]
    tokens, words = parse_exclusions(exclusions)
    pools = {}
    for _, _, _, cat in layout:
        if cat not in pools:
            pools[cat] = pool_for(cat, diet, tokens, words)
            if not pools[cat]:
                raise PlanError(f"No {cat} recipes match your diet and exclusions. Please relax them in your profile.")
    recent = recent or set()
    avoid = avoid or set()
    kt, pt, ct, ft = targets["kcal"], targets["protein"], targets["carbs"], targets["fat"]

    best, best_score = None, 1e9
    for _ in range(trials):
        picks, used = [], set()
        for slot, label, share, cat in layout:
            cands = [r for r in pools[cat] if r["id"] not in used and r["id"] not in avoid] or \
                    [r for r in pools[cat] if r["id"] not in used] or pools[cat]
            r = rng.choice(cands)
            used.add(r["id"])
            picks.append((slot, label, share, r))
        meals = [_meal(slot, label, r, _clip(kt * share / r["m"]["kcal"], 0.55, 1.75))
                 for slot, label, share, r in picks]
        tot = _totals(meals)
        score = (abs(tot["kcal"] - kt) / kt * 3 + max(0, pt - tot["p"]) / pt * 2.5
                 + max(0, tot["p"] - pt * 1.25) / pt * 0.5 + abs(tot["f"] - ft) / ft * 0.8
                 + abs(tot["c"] - ct) / ct * 0.6
                 + 0.15 * sum(1 for _, _, _, r in picks if r["id"] in recent))
        if score < best_score:
            best, best_score = (picks, meals), score
    picks, meals = best

    # protein top-up (up to two shakes / snacks) if clearly short
    boosts = []
    for _ in range(2):
        tot = _totals(meals)
        if tot["p"] >= 0.92 * pt:
            break
        taken = {p_[3]["id"] for p_ in picks} | {b["recipe_id"] for b in boosts}
        snack_pool = sorted(pool_for("snack", diet, tokens, words), key=lambda r: -r["m"]["p"] / r["m"]["kcal"])
        snack_pool = [r for r in snack_pool if r["id"] not in taken]
        if not snack_pool:
            break
        r = snack_pool[0]
        sb = _clip((pt - tot["p"]) / max(r["m"]["p"], 1), 0.5, 1.5)
        new_boost = _meal("boost%d" % (len(boosts) + 1), "Protein top-up", r, sb)
        boost_kcal = sum(b["kcal"] for b in boosts) + new_boost["kcal"]
        base_kcal = sum(_meal(slot, label, r2, _clip(kt * share / r2["m"]["kcal"], 0.55, 1.75))["kcal"]
                        for slot, label, share, r2 in picks)
        k = (kt - boost_kcal) / base_kcal if base_kcal else 1
        if not 0.7 <= k <= 1.1:
            break
        boosts.append(new_boost)
        meals = [_meal(slot, label, r2, _clip(kt * share / r2["m"]["kcal"], 0.55, 1.75) * k)
                 for slot, label, share, r2 in picks] + boosts
    return dict(meals=meals, totals=_totals(meals))


def _strip(day):
    for m in day["meals"]:
        m.pop("raw_items", None)
    return day


def plan_signature(targets, profile, report_id):
    blob = json.dumps([targets["kcal"], targets["protein"], targets["carbs"], targets["fat"],
                       profile.get("diet"), profile.get("exclusions"), profile.get("meals_per_day"), report_id],
                      sort_keys=True)
    return hashlib.sha1(blob.encode()).hexdigest()[:12]


def build_week(targets, meals_per_day, diet, exclusions, seed):
    rng = random.Random(seed)
    days, recent = [], []
    for d in range(7):
        rset = {rid for prev in recent[-2:] for rid in prev}
        day = build_day(targets, meals_per_day, diet, exclusions, rng, recent=rset)
        recent.append({m["recipe_id"] for m in day["meals"]})
        days.append(_strip(day))
    return days


def rebuild_day(plan, day_index, targets, meals_per_day, diet, exclusions):
    rng = random.Random(random.SystemRandom().randrange(1 << 30))
    avoid = {m["recipe_id"] for m in plan["days"][day_index]["meals"]}
    plan["days"][day_index] = _strip(build_day(targets, meals_per_day, diet, exclusions, rng, avoid=avoid))
    return plan


def shopping_list(plan):
    agg = {}
    for day in plan["days"]:
        for m in day["meals"]:
            for it in m["items"]:
                agg[it["key"]] = agg.get(it["key"], 0) + it["grams"]
    groups = {a: [] for a in AISLE_ORDER}
    for key, grams in agg.items():
        fd = FOODS[key]
        raw = grams * fd["buy"]
        if fd["unit"] and fd["uname"] in ("egg", "egg white"):
            text = f"{round(grams / fd['unit'])} {fd['uname']}s"
        elif raw < 100:
            text = f"{int(round(raw / 5) * 5)} g"
        elif raw < 1000:
            text = f"{int(-(-raw // 50) * 50)} g"
        else:
            text = f"{raw / 1000:.2f} kg"
        note = ""
        if fd["buy"] != 1.0:
            note = "dry / raw weight" if fd["buy"] < 1 else "raw weight"
        groups[fd["aisle"]].append(dict(name=fd["name"], text=text, note=note))
    for a in groups:
        groups[a].sort(key=lambda x: x["name"])
    return [(a, groups[a]) for a in AISLE_ORDER if groups[a]]
