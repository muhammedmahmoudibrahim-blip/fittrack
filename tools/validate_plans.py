"""Check coach-plans.json before publishing it: python3 tools/validate_plans.py"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "py"))
import workouts  # noqa: E402

DAYS = set(workouts.DOW)
TYPES = {"strength", "cardio", "recovery", "rest"}


def check(path):
    errs = []
    data = json.load(open(path, encoding="utf-8"))
    if not isinstance(data.get("plans"), dict):
        return ["top level needs a 'plans' object"]
    for who, plan in data["plans"].items():
        t = f"[{who}]"
        for f in ("id", "title", "valid_to"):
            if not plan.get(f):
                errs.append(f"{t} missing '{f}'")
        for f in ("valid_from", "valid_to"):
            if plan.get(f) and not re.fullmatch(r"\d{4}-\d\d-\d\d", plan[f]):
                errs.append(f"{t} {f} must look like 2026-11-30")
        days = plan.get("days")
        if not isinstance(days, dict) or not days:
            errs.append(f"{t} needs a 'days' object")
            continue
        for d, pd in days.items():
            if d not in DAYS:
                errs.append(f"{t} day '{d}' must be one of {sorted(DAYS)}")
                continue
            typ = pd.get("type", "strength")
            if typ not in TYPES:
                errs.append(f"{t} {d}: type must be one of {sorted(TYPES)}")
            for i, ex in enumerate(pd.get("exercises") or []):
                k = ex.get("key")
                if k not in workouts.EX:
                    errs.append(f"{t} {d} #{i + 1}: unknown exercise key '{k}'")
                    continue
                if typ == "strength":
                    if not isinstance(ex.get("sets"), int) or not ex.get("reps"):
                        errs.append(f"{t} {d} {k}: strength exercises need integer 'sets' and a 'reps' string")
                    w = ex.get("weight_kg")
                    if w is not None and not isinstance(w, (int, float)):
                        errs.append(f"{t} {d} {k}: weight_kg must be a number")
            if typ in ("strength", "cardio") and not pd.get("exercises"):
                errs.append(f"{t} {d}: {typ} day has no exercises")
    return errs


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "coach-plans.json")
    e = check(path)
    print("OK" if not e else "\n".join(e))
    sys.exit(1 if e else 0)
