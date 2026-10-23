// Offline cache. Everything is served from this site (the Python engine is bundled in /pyodide).
const C='fittrack-static-v3';
const SHELL=['./','index.html','app.js','style.css','manifest.json','icon-192.png','icon-512.png',
 ...["back_squat", "band_face_pull", "bench_dip", "bench_press", "biceps_curl", "box_squat", "calf_raise", "cat_cow", "chest_press", "close_push_up", "db_bench", "db_rdl", "db_row", "db_shoulder_press", "dead_bug", "face_pull", "floor_press", "glute_bridge", "goblet_squat", "hanging_knee_raise", "hip_flexor_stretch", "hip_thrust_db", "incline_push_up", "lat_pulldown", "lateral_raise", "leg_curl", "leg_extension", "leg_press", "overhead_press", "pallof_press", "plank", "pull_up", "push_up", "reverse_crunch", "romanian_deadlift", "seated_row", "side_plank", "single_leg_bridge", "split_squat", "step_up", "triceps_pushdown"].map(k=>'anim/'+k+'.gif'),
 'py/engine.py','py/workouts.py','py/foods.py','py/planner.py','py/coach.py','py/bridge.py'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(C).then(c=>c.addAll(SHELL)));self.skipWaiting()});
self.addEventListener('activate',e=>e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==C).map(k=>caches.delete(k)))).then(()=>clients.claim())));
self.addEventListener('fetch',e=>{
  const r=e.request,u=new URL(r.url);
  if(r.method!=='GET'||u.origin!==location.origin)return; // YouTube and anything else: straight to the network
  e.respondWith(caches.match(r).then(hit=>hit||fetch(r).then(res=>{
    if(res.ok&&res.type==='basic'){const cp=res.clone();caches.open(C).then(c=>c.put(r,cp))}return res})
    .catch(()=>r.mode==='navigate'?caches.match('index.html'):Response.error())));
});
