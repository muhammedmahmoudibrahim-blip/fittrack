// Offline cache. Everything is served from this site (the Python engine is bundled in /pyodide).
const C='fittrack-static-v2';
const SHELL=['./','index.html','app.js','style.css','manifest.json','icon-192.png','icon-512.png',
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
