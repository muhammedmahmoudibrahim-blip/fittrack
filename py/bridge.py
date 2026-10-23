"""Thin JSON bridge so the browser UI can call the unchanged FitTrack logic (runs in Pyodide)."""
import json
import random
from datetime import date, datetime

import coach
import engine
import planner
import workouts


def _d(s):
    return datetime.strptime(s, "%Y-%m-%d").date()


def context(profile_json, report_json, steps_avg=None):
    prof = json.loads(profile_json)
    rep = json.loads(report_json) if report_json else None
    age = engine.age_from(prof.get("birth_date"))
    safety = engine.safety_flags(prof)
    complete = bool(prof.get("sex") and prof.get("birth_date") and prof.get("height_cm"))
    out = dict(age=age, safety=safety, complete=complete, goal=None, targets=None)
    if complete and rep:
        out["goal"] = engine.decide_goal(prof, rep, safety, age)
        out["targets"] = engine.compute_targets(prof, rep, out["goal"], safety, steps_avg=steps_avg,
                                                kcal_adjust=prof.get("kcal_adjust") or 0)
    return json.dumps(out)


def constants():
    return json.dumps(dict(equipment=list(workouts.EQUIPMENT.items()), presets=workouts.PRESETS,
                           injuries=list(workouts.INJURIES.items()), conditions=engine.CONDITIONS,
                           activity={k: v[1] for k, v in engine.ACTIVITY.items()},
                           diets=list(planner.DIET_RANK.keys()) if hasattr(planner, "DIET_RANK") else [],
                           allergens=planner.ALLERGENS, dow=workouts.DOW))


def _overlay(prog, plan_json, p, goal_key, light_only, equip, inj):
    if not plan_json:
        return prog
    return workouts.apply_plan(prog, json.loads(plan_json), equip, inj, goal_key, p.get("level") or "beginner",
                               bool(light_only))


def program(profile_json, goal_key, light_only, missing_json, swaps_json, dow, plan_json=""):
    p = json.loads(profile_json)
    missing = [m for m in json.loads(missing_json) if m in workouts.EQUIPMENT]
    equip_all = engine.csv(p.get("equipment"))
    inj = engine.csv(p.get("injuries"))
    level = p.get("level") or "beginner"
    prog = workouts.build_program(goal_key, level, int(p.get("strength_days") or 3), equip_all, inj,
                                  light_only=bool(light_only), missing=missing)
    equip = set(equip_all) - set(missing)
    prog = _overlay(prog, plan_json, p, goal_key, light_only, equip, inj)
    day = prog["days"][int(dow)]
    for sw in json.loads(swaps_json):
        if ">" in sw:
            o, a = sw.split(">", 1)
            if o in workouts.EX and a in workouts.EX:
                for i, ex in enumerate(day["exercises"]):
                    if ex["key"] == o:
                        c = workouts.card(a, equip, set(inj), goal_key, level, bool(light_only), swapped_from=o)
                        if ex.get("minutes"):
                            c["minutes"] = ex["minutes"]
                        day["exercises"][i] = c
    return json.dumps(dict(prog=prog, day=day))


def week_summary(profile_json, goal_key, light_only, plan_json=""):
    p = json.loads(profile_json)
    equip, inj = engine.csv(p.get("equipment")), engine.csv(p.get("injuries"))
    prog = workouts.build_program(goal_key, p.get("level") or "beginner", int(p.get("strength_days") or 3),
                                  equip, inj, light_only=bool(light_only))
    prog = _overlay(prog, plan_json, p, goal_key, light_only, equip, inj)
    return json.dumps(prog)


def hint(last_reps, last_weight, rep_range):
    return workouts.progression_hint(last_reps, last_weight, rep_range)


def build_plan(targets_json, profile_json, seed):
    t, p = json.loads(targets_json), json.loads(profile_json)
    try:
        days = planner.build_week(t, int(p.get("meals_per_day") or 4), p.get("diet") or "omnivore",
                                  p.get("exclusions") or "", seed=int(seed))
    except planner.PlanError as e:
        return json.dumps(dict(error=str(e)))
    return json.dumps(dict(days=days, targets=t))


def rebuild_day(plan_json, day_index, targets_json, profile_json):
    plan, t, p = json.loads(plan_json), json.loads(targets_json), json.loads(profile_json)
    try:
        planner.rebuild_day(plan, int(day_index), t, int(p.get("meals_per_day") or 4), p.get("diet") or "omnivore",
                            p.get("exclusions") or "")
    except planner.PlanError as e:
        return json.dumps(dict(error=str(e)))
    return json.dumps(plan)


def plan_sig(targets_json, profile_json, report_id):
    return planner.plan_signature(json.loads(targets_json), json.loads(profile_json), report_id)


def shopping(plan_json):
    return json.dumps(planner.shopping_list(json.loads(plan_json)))


def review(goal_key, targets_json, weights_json, steps_json, water_json, sleep_json, done, planned, ticked, possible,
           report_date, today):
    t = json.loads(targets_json) if targets_json else None
    wp = [(_d(d), v) for d, v in json.loads(weights_json)]
    return json.dumps(coach.weekly_review(goal_key, t, wp, json.loads(steps_json), json.loads(water_json),
                                          json.loads(sleep_json), int(done), int(planned), int(ticked), int(possible),
                                          _d(report_date), _d(today)))
