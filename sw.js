// Offline cache: app shell + Python modules, plus the Pyodide runtime the first time it is downloaded.
const C='fittrack-static-v1';
const SHELL=['./','index.html','app.js','style.css','manifest.json','icon-192.png','icon-512.png',
 'py/engine.py','py/workouts.py','py/foods.py','py/planner.py','py/coach.py','py/bridge.py'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(C).then(c=>c.addAll(SHELL)));self.skipWaiting()});
self.addEventListener('activate',e=>e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==C).map(k=>caches.delete(k)))).then(()=>clients.claim())));
self.addEventListener('fetch',e=>{
  const u=new URL(e.request.url);
  if(e.request.method!=='GET')return;
  const ours=u.origin===location.origin, pyo=u.hostname==='cdn.jsdelivr.net'&&u.pathname.startsWith('/pyodide/');
  if(!ours&&!pyo)return; // YouTube etc. go straight to the network
  e.respondWith(caches.match(e.request).then(r=>r||fetch(e.request).then(res=>{
    if(res.ok){const cp=res.clone();caches.open(C).then(c=>c.put(e.request,cp))}return res}).catch(()=>caches.match('index.html'))));
});
