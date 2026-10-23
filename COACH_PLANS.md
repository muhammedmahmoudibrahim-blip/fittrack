# Monthly coach plans

Claude writes each month's plan into `coach-plans.json`. The app fetches that file whenever it is opened online,
keeps a copy for offline use, and shows the plan under **Train**, **Home** and **Coach** for the matching person.

The key under `plans` must match the person's name in the app (top-right selector, case-insensitive).
Days that are not listed become rest days. Exercise `key`s must exist in `py/workouts.py`.

```json
{
  "version": 1,
  "plans": {
    "Me": {
      "id": "2026-11",
      "title": "November block 1",
      "valid_from": "2026-11-01",
      "valid_to": "2026-11-28",
      "notes": "Free text shown on the Train and Coach tabs.",
      "days": {
        "Mon": {"type": "strength", "title": "Lower A", "exercises": [
          {"key": "leg_press", "sets": 4, "reps": "8-10", "rest": 100, "weight_kg": 80, "note": "3 s down"}
        ]},
        "Tue": {"type": "cardio", "title": "Zone 2", "exercises": [{"key": "bike", "minutes": "30 min"}]},
        "Wed": {"type": "recovery"}
      }
    }
  }
}
```

Run `python3 tools/validate_plans.py` before publishing.
