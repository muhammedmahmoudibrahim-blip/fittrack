"""Rules-based weekly review: compares what you did with what was planned and suggests one adjustment."""
from datetime import timedelta


def slope_per_week(points):
    """points: [(date, kg)]. Least-squares slope in kg/week, or None if there is not enough spread."""
    pts = sorted(points)
    if len(pts) < 3:
        return None
    x0 = pts[0][0]
    xs = [(d - x0).days for d, _ in pts]
    if max(xs) < 6:
        return None
    ys = [v for _, v in pts]
    n = len(pts)
    mx, my = sum(xs) / n, sum(ys) / n
    den = sum((x - mx) ** 2 for x in xs)
    if den == 0:
        return None
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / den * 7


def avg(vals):
    vals = [v for v in vals if v is not None]
    return sum(vals) / len(vals) if vals else None


def weekly_review(goal_key, targets, weight_points, steps, water, sleep, workouts_done, workouts_planned,
                  meals_ticked, meals_possible, latest_report_date, today):
    msgs = []
    slope = slope_per_week(weight_points)
    weight_now = sorted(weight_points)[-1][1] if weight_points else None
    adherence_ok = (workouts_planned and workouts_done >= max(1, workouts_planned - 1)) or \
                   (meals_possible and meals_ticked / meals_possible >= 0.7)

    if slope is not None and weight_now:
        pct = slope / weight_now * 100
        txt = f"Your weight is changing by about {slope:+.2f} kg per week ({pct:+.1f}% of body weight)."
        if goal_key == "fat_loss":
            if pct > -0.1 and adherence_ok:
                msgs.append(dict(level="warn", title="Weight loss has stalled", text=txt +
                                 " You have followed the plan, so make one small change: eat about 100 kcal less or "
                                 "add ~1,500 steps a day (not both).", adjust=-100))
            elif pct < -1.0:
                msgs.append(dict(level="warn", title="Losing weight too fast", text=txt +
                                 " Losing faster than 1% per week risks muscle loss. Eat about 150 kcal more.",
                                 adjust=150))
            else:
                msgs.append(dict(level="good", title="Weight trend is on track", text=txt))
        elif goal_key == "lean_gain":
            if pct < 0:
                msgs.append(dict(level="warn", title="Not gaining yet", text=txt +
                                 " Add about 150 kcal a day (an extra snack).", adjust=150))
            elif pct > 0.5:
                msgs.append(dict(level="warn", title="Gaining a little fast", text=txt +
                                 " Reduce about 100 kcal a day to limit fat gain.", adjust=-100))
            else:
                msgs.append(dict(level="good", title="Weight trend is on track", text=txt))
        else:
            msgs.append(dict(level="info", title="Weight trend",
                             text=txt + " For recomposition, the scale matters less than your next body scan."))
    else:
        msgs.append(dict(level="info", title="Log your weight",
                         text="Add your weight on at least 3 different days over a week (same time of day) so I can "
                              "see the trend."))

    if workouts_planned:
        lvl = "good" if workouts_done >= workouts_planned else "warn" if workouts_done else "warn"
        msgs.append(dict(level=lvl, title=f"Workouts: {workouts_done} of {workouts_planned} this week",
                         text="Consistency beats intensity. If time is short, do the first three exercises of each session."
                         if workouts_done < workouts_planned else "You completed every planned session."))
    sa = avg(steps)
    if sa is not None and targets:
        if sa >= targets["steps_target"]:
            msgs.append(dict(level="good", title=f"Steps: {sa:,.0f} a day",
                             text="You are reaching your step target. Daily movement matters a lot with a desk job."))
        else:
            msgs.append(dict(level="warn", title=f"Steps: {sa:,.0f} a day (target {targets['steps_target']:,})",
                             text="Stand up every 60 minutes, take a 10-minute walk after lunch and dinner, and use "
                                  "calls as walking time."))
    wa = avg(water)
    if wa is not None and targets and wa < targets["water_ml"] * 0.8:
        msgs.append(dict(level="warn", title=f"Water: {wa / 1000:.1f} L a day",
                         text=f"Aim for about {targets['water_ml'] / 1000:.1f} L, more in hot weather."))
    sl = avg(sleep)
    if sl is not None and sl < 7:
        msgs.append(dict(level="warn", title=f"Sleep: {sl:.1f} h a night",
                         text="Under 7 hours raises hunger and slows recovery. Fixing sleep often helps more than "
                              "cutting calories."))
    if latest_report_date and (today - latest_report_date) > timedelta(days=28):
        msgs.append(dict(level="info", title="Time for a new body scan",
                         text="Your last body-composition report is over 4 weeks old. Add a new one and your goal, "
                              "calories and plan are recalculated automatically."))
    return msgs
