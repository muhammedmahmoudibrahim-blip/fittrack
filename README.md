# FitTrack (phone edition)

A personal trainer and nutrition app that runs entirely in the phone's browser. No server, no VPN, no laptop.
The original FitTrack logic (goals from your body-composition report, calorie/macro targets, 7-day halal meal plan,
equipment-aware workouts, weekly coach) runs unchanged in Python via Pyodide. Exercise videos open as YouTube form demos.

- Data (profile, reports, logs, meal ticks) is stored only in each phone's browser. Use **Me → Export backup** regularly.
- The first load needs internet (about 10 MB for the Python engine). After that it works offline, e.g. in the gym basement.
- Add to Home Screen to install it like an app.
- General fitness guidance, not medical advice.

Local test: `python3 -m http.server` in this folder, then open http://localhost:8000

## Exercise animations
Each exercise shows a looping animation made from the start and end photos in the public-domain
[Free Exercise DB](https://github.com/yuhonas/free-exercise-db) (Unlicense). Exercises without a matching photo keep a video link.
