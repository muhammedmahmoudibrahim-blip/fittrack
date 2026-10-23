// FitTrack (static edition): UI in JS, all trainer logic = the original Python running in Pyodide. Data stays on this phone.
const PYFILES=['engine','workouts','foods','planner','coach','bridge'];
const KEY='fittrack.static.v1';
const $=s=>document.querySelector(s), app=$('#app');
const esc=s=>String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const iso=d=>{const x=d||new Date();return x.getFullYear()+'-'+String(x.getMonth()+1).padStart(2,'0')+'-'+String(x.getDate()).padStart(2,'0')};
const addDays=(s,n)=>{const d=new Date(s+'T12:00:00');d.setDate(d.getDate()+n);return iso(d)};
const dowToday=()=>(new Date().getDay()+6)%7;
const yt=n=>'https://www.youtube.com/results?search_query='+encodeURIComponent(n.replace(/\s*\(.*?\)/g,'').trim()+' proper form tutorial');
const ANIM=new Set(["back_squat", "band_face_pull", "bench_dip", "bench_press", "biceps_curl", "box_squat", "calf_raise", "cat_cow", "chest_press", "close_push_up", "db_bench", "db_rdl", "db_row", "db_shoulder_press", "dead_bug", "face_pull", "floor_press", "glute_bridge", "goblet_squat", "hanging_knee_raise", "hip_flexor_stretch", "hip_thrust_db", "incline_push_up", "lat_pulldown", "lateral_raise", "leg_curl", "leg_extension", "leg_press", "overhead_press", "pallof_press", "plank", "pull_up", "push_up", "reverse_crunch", "romanian_deadlift", "seated_row", "side_plank", "single_leg_bridge", "split_squat", "step_up", "triceps_pushdown"]);
const demo=ex=>ANIM.has(ex.key)?`<img class="demo" src="anim/${ex.key}.gif" alt="How to do ${esc(ex.name)}" loading="lazy" width="360"><div class="small muted">Animation alternates the start and end position.</div>`:`<div class="small"><a href="${yt(ex.name)}" target="_blank" rel="noopener">▶ Watch how to do it (video)</a></div>`;
let py,B,K,S,flash='';
const call=(fn,...a)=>{const r=B[fn](...a);return r};
const J=(fn,...a)=>JSON.parse(call(fn,...a));

// ---------- state ----------
const blank=()=>({profile:{activity:'sedentary',diet:'omnivore',meals_per_day:4,strength_days:3,level:'beginner',kcal_adjust:0,conditions:'',injuries:'',equipment:'',exclusions:''},
  reports:[],checkins:{},logs:[],meal_checks:{},plan:null});
function load(){try{S=JSON.parse(localStorage.getItem(KEY))}catch(e){}
  if(!S||!S.users)S={cur:'Me',users:{Me:blank()}};}
const save=()=>localStorage.setItem(KEY,JSON.stringify(S));
const U=()=>S.users[S.cur];

// ---------- context ----------
function ctx(){const u=U(),rep=u.reports.length?[...u.reports].sort((a,b)=>a.report_date<b.report_date?-1:1).pop():null;
  const since=addDays(iso(),-7),steps=Object.entries(u.checkins).filter(([d,c])=>d>=since&&c.steps!=null).map(([d,c])=>c.steps);
  const c=JSON.parse(B.context(JSON.stringify(u.profile),rep?JSON.stringify(rep):'',steps.length>=3?steps.reduce((a,b)=>a+b,0)/steps.length:null));
  c.profile=u.profile;c.report=rep;return c}
function ensurePlan(c){if(!c.targets)return null;const u=U();
  const sig=call('plan_sig',JSON.stringify(c.targets),JSON.stringify(u.profile),c.report.id);
  if(u.plan&&u.plan.sig===sig)return u.plan.data;
  const r=J('build_plan',JSON.stringify(c.targets),JSON.stringify(u.profile),Math.floor(Math.random()*1e9));
  if(r.error){flash=r.error;return null}u.plan={sig,data:r};save();return r}

// ---------- helpers ----------
const needSetup=c=>{if(!c.complete)return go('#/me'),flash='Please complete your profile first (sex, date of birth, height).',true;
  if(!c.report)return go('#/report'),flash='Add your latest body-composition report first. Your goal and plan are built from it.',true;return false};
const go=h=>{location.hash=h};
const banners=c=>c.safety.warnings.map(w=>`<div class="banner">${esc(w)}</div>`).join('');
const bar=(v,t,cls)=>`<div class="bar ${cls||''}"><i style="width:${Math.min(100,t?Math.round(v/t*100):0)}%"></i></div>`;
function page(k,html){const f=flash?`<div class="flash warn">${esc(flash)}</div>`:'';flash='';
  app.innerHTML=f+html+'<p class="muted small center" style="margin-top:24px">FitTrack gives general fitness and nutrition guidance, not medical advice.<br>Exercise photos: Free Exercise DB (public domain).</p>';
  $('#tabs').hidden=false;document.querySelectorAll('#tabs a').forEach(a=>a.classList.toggle('on',a.dataset.k===k));
  $('#who').innerHTML=Object.keys(S.users).map(n=>`<option ${n===S.cur?'selected':''}>${esc(n)}</option>`).join('');
  $('#who').innerHTML=`<select id="usel" style="width:auto;padding:4px 8px">${$('#who').innerHTML}</select>`;
  $('#usel').onchange=e=>{S.cur=e.target.value;save();route()};window.scrollTo(0,0)}
function formData(f){const o={};new FormData(f).forEach((v,k)=>{(o[k]=o[k]||[]).push(v)});return o}
const one=(o,k)=>o[k]&&o[k][0]!==''?o[k][0]:null;

// ---------- views ----------
function vHome(){const c=ctx();
  if(!c.complete)return page('home',`<div class="card"><h1>Let's get you set up</h1><p>Step 1: tell me about yourself, health history and equipment.</p><a class="btn" href="#/me">Complete my profile</a></div>`);
  if(!c.report)return page('home',`<div class="card"><h1>Add your body report</h1><p>Your goal, calories and workouts are built from your latest body-composition report.</p><a class="btn" href="#/report">Enter my report</a></div>`);
  const t=c.targets,plan=ensurePlan(c),d=dowToday(),u=U(),today=iso(),ticks=u.meal_checks[today]||[];
  let meals='',eat={kcal:0,p:0};
  if(plan){const day=plan.days[d];day.meals.forEach(m=>{if(ticks.includes(m.slot)){eat.kcal+=m.kcal;eat.p+=m.p}});
    meals=`<div class="card"><div class="row between"><h2>Today's meals</h2><a href="#/food" class="small">Full plan</a></div>`+day.meals.map(m=>
      `<div class="row between meal"><div><b>${esc(m.label)}</b><div>${esc(m.name)}</div><div class="macros">${m.kcal} kcal · ${m.p} g protein</div></div>
      <button class="${ticks.includes(m.slot)?'':'secondary'} small" data-tick="${m.slot}">${ticks.includes(m.slot)?'✓ Eaten':'Mark eaten'}</button></div>`).join('')+'</div>'}
  const prog=J('week_summary',JSON.stringify(u.profile),c.goal.key,c.safety.light_only),td=prog.days[d];
  page('home',banners(c)+`<div class="hero"><div class="muted small">Your goal, from your report of ${esc(c.report.report_date)}</div><h2>${esc(c.goal.label)}</h2><div class="small">${esc(c.goal.reasons[0])}</div></div>`+
   (t?`<div class="card"><h2>Today's targets</h2><div class="grid g3"><div class="stat"><b>${t.kcal}</b><span>kcal</span></div><div class="stat"><b>${t.protein} g</b><span>protein</span></div><div class="stat"><b>${t.steps_target}</b><span>steps</span></div></div>
   <p class="muted small" style="margin:8px 0 0">Eaten so far: ${eat.kcal} kcal, ${eat.p} g protein.</p></div>`:'')+meals+
   `<div class="card"><h2>Today: ${esc(td.title)}</h2><a class="btn" href="#/train/${d}">Open today's session</a></div>
   <div class="card"><a class="btn secondary" href="#/checkin">Log today's weight, steps, water, sleep</a></div>`);
  app.querySelectorAll('[data-tick]').forEach(b=>b.onclick=()=>tick(b.dataset.tick))}
function tick(slot){const u=U(),t=iso(),a=u.meal_checks[t]||(u.meal_checks[t]=[]);const i=a.indexOf(slot);i<0?a.push(slot):a.splice(i,1);save();route()}

function vFood(q){const c=ctx();if(needSetup(c))return route();
  const plan=ensurePlan(c);let d=q.d!=null?+q.d:dowToday();const t=c.targets;
  if(!t)return page('food',banners(c)+'<div class="card"><p>Calorie and meal targets are switched off for your safety settings. Please follow the advice of your doctor or dietitian.</p></div>');
  if(!plan)return page('food',`<div class="card"><p>I couldn't build a plan with your food settings. Relax your exclusions in <a href="#/me">your profile</a>.</p></div>`);
  const day=plan.days[d],tot=day.totals,isToday=d===dowToday(),ticks=isToday?(U().meal_checks[iso()]||[]):[];
  page('food',`<div class="row between"><h1>Nutrition</h1><a class="btn small secondary" href="#/shopping">Shopping list</a></div>`+banners(c)+
  `<div class="card soft"><h2>${esc(c.goal.short)}: ${t.kcal} kcal a day</h2><div class="small">Protein <b>${t.protein} g</b> · Carbs <b>${t.carbs} g</b> · Fat <b>${t.fat} g</b> · Fibre ≥ <b>${t.fiber} g</b> · Water <b>${(t.water_ml/1000).toFixed(1)} L</b></div>
   <p class="small muted" style="margin:.5em 0 0">At rest ${t.bmr} kcal (${esc(t.bmr_src)}), about ${t.tdee} kcal with your activity. Expected change about ${t.weekly_change_kg>=0?'+':''}${t.weekly_change_kg} kg/week.${t.floored?' Calories kept at a safe minimum.':''}${t.kcal_adjust?` Includes coach adjustment of ${t.kcal_adjust>0?'+':''}${t.kcal_adjust} kcal.`:''}</p></div>
   <div class="days">${K.dow.map((n,i)=>`<a href="#/food?d=${i}" class="${i===d?'on':''}">${n}${i===dowToday()?'<small>today</small>':''}</a>`).join('')}</div>
   <div class="card"><h2>${tot.kcal} kcal planned</h2><div class="small">Calories ${tot.kcal} / ${t.kcal}</div>${bar(tot.kcal,t.kcal)}
   <div class="small">Protein ${tot.p} / ${t.protein} g</div>${bar(tot.p,t.protein,'p')}<div class="small">Carbs ${tot.c} / ${t.carbs} g</div>${bar(tot.c,t.carbs,'c')}<div class="small">Fat ${tot.f} / ${t.fat} g</div>${bar(tot.f,t.fat,'f')}
   ${tot.p<t.protein*0.9?'<div class="banner" style="margin-top:8px">Protein is a little under target. A whey or plant protein shake is the easiest fix.</div>':''}</div>
   <div class="card">${day.meals.map(m=>`<div class="meal"><div class="row between"><h3>${esc(m.label)}: ${esc(m.name)}</h3>${isToday?`<button class="${ticks.includes(m.slot)?'':'secondary'} small" data-tick="${m.slot}">${ticks.includes(m.slot)?'✓ Eaten':'Mark eaten'}</button>`:''}</div>
   <ul>${m.items.map(i=>`<li>${i.qty?esc(i.qty)+' · ':''}${esc(i.name)} <span class="muted">(${i.grams} g)</span></li>`).join('')}</ul>${m.note?`<div class="small muted">${esc(m.note)}</div>`:''}
   <div class="macros">${m.kcal} kcal · P ${m.p} g · C ${m.c} g · F ${m.f} g</div></div>`).join('')}<p class="muted small">Weights are cooked / ready-to-eat. All meals are halal.</p></div>
   <div class="row"><button class="secondary small" id="rd">New meals for this day</button><button class="secondary small" id="rw">New week</button></div>`);
  app.querySelectorAll('[data-tick]').forEach(b=>b.onclick=()=>tick(b.dataset.tick));
  $('#rd').onclick=()=>{const r=J('rebuild_day',JSON.stringify(plan),d,JSON.stringify(c.targets),JSON.stringify(U().profile));if(r.error)flash=r.error;else{U().plan.data=r;save()}route()};
  $('#rw').onclick=()=>{if(confirm('Create a completely new week?')){U().plan=null;save();route()}}}
function vShop(){const c=ctx();if(needSetup(c))return route();const plan=ensurePlan(c);
  const g=plan?J('shopping',JSON.stringify(plan)):[];
  page('food',`<div class="row between"><h1>Shopping list</h1><a class="small" href="#/food">Back</a></div>`+g.map(([a,items])=>`<div class="card"><h2>${esc(a)}</h2>${items.map(i=>`<div class="row between"><span>${esc(i.name)}${i.note?` <span class="muted small">(${esc(i.note)})</span>`:''}</span><b>${esc(i.text)}</b></div>`).join('')}</div>`).join('')||'<div class="card">No plan yet.</div>')}

function vTrain(){const c=ctx();if(needSetup(c))return route();const prog=J('week_summary',JSON.stringify(U().profile),c.goal.key,c.safety.light_only);
  const ws=addDays(iso(),-dowToday()),done=new Set(U().logs.filter(l=>l.day>=ws).map(l=>(new Date(l.day+'T12:00:00').getDay()+6)%7));
  page('train',`<h1>This week</h1>`+banners(c)+prog.days.map(d=>`<a href="#/train/${d.index}" style="text-decoration:none;color:inherit"><div class="card"><div class="row between"><div><b>${d.full}${d.index===dowToday()?' · today':''}</b><div>${esc(d.title)}</div>
   ${d.type==='strength'?`<div class="small muted">${d.exercises.map(e=>esc(e.name)).join(' · ')}</div>`:d.type==='cardio'?`<div class="small muted">${esc(d.exercises[0].name)} · ${esc(d.minutes||d.exercises[0].minutes)}</div>`:''}</div>${done.has(d.index)?'<span class="pill">✓ done</span>':''}</div></div></a>`).join(''))}

const MISSING={};let SWAPS={};
function vDay(dow){const c=ctx();if(needSetup(c))return route();const u=U(),miss=MISSING.v||[];
  const r=J('program',JSON.stringify(u.profile),c.goal.key,c.safety.light_only,JSON.stringify(miss),JSON.stringify(SWAPS[dow]||[]),dow),day=r.day,prog=r.prog,today=iso();
  const myEq=(u.profile.equipment||'').split(',').filter(Boolean),eq=Object.fromEntries(K.equipment);
  const last=k=>[...u.logs].filter(l=>l.exercise_key===k&&l.day<today).sort((a,b)=>a.day<b.day?-1:1).pop();
  const logged=Object.fromEntries(u.logs.filter(l=>l.day===today&&l.session_key===day.session_key).map(l=>[l.exercise_key,l]));
  const isToday=dow===dowToday();
  let h=`<div class="row between"><h1>${esc(day.full)}: ${esc(day.title)}</h1><a href="#/train" class="small">All days</a></div>`+banners(c);
  if(day.type==='rest'||day.type==='recovery'){
    h+=`<div class="card"><p>${day.type==='rest'?'Rest day. Take an easy 20–30 minute walk, stretch, and sleep well.':'Active recovery: a 20–30 minute walk plus the desk-reset routine below. No weights today.'}</p></div>
    <div class="card"><h2>Desk reset (5 min)</h2>${prog.warmup.map(x=>`<div class="ex"><div class="nm">${esc(x.name)}</div><div class="small muted">${esc(x.cue)}</div></div>`).join('')}</div>`;return page('train',h)}
  h+=`<div class="card soft"><b class="small">Equipment not available today?</b><div class="checks" style="margin-top:6px">${myEq.map(k=>`<label><input type="checkbox" data-miss="${k}" ${miss.includes(k)?'checked':''}> ${esc(eq[k]||k)}</label>`).join('')}</div>
   ${myEq.length?'':'<p class="small muted">You listed no equipment, so everything is bodyweight.</p>'}<p style="margin:8px 0 0"><button class="secondary small" id="upd">Update exercises</button></p></div>`;
  if(day.type==='strength')h+=`<details class="card"><summary>Warm-up: desk reset (5 min)</summary>${prog.warmup.map(x=>`<div class="ex"><div class="nm">${esc(x.name)}</div><div class="small muted">${esc(x.cue)}</div></div>`).join('')}</details>`;
  h+=`<form id="wf" class="card">`+day.exercises.map((ex,i)=>{const lg=last(ex.key),lo=logged[ex.key],cardio=day.type==='cardio';
    const hint=lg&&ex.reps?B.hint(lg.reps,lg.weight_kg,ex.reps):null;
    return `<div class="ex"><input type="hidden" name="ex" value="${ex.key}"><div class="nm">${i+1}. ${esc(ex.name)}</div><div class="small muted">${esc(ex.muscles)}</div>
    ${cardio?'':demo(ex)}
    ${ex.swapped_from?`<div class="small"><span class="pill warn">Swapped</span> instead of ${esc(ex.swapped_from)}</div>`:''}
    <div class="small">${cardio?`Target: <b>${esc(day.exercises[0].minutes||'')}</b> at a pace where you can still talk.`:`Target: <b>${ex.sets} × ${esc(ex.reps)}</b> · rest ${ex.rest} s`}</div><div class="small">${esc(ex.cue)}</div>
    ${lg?`<div class="small muted">Last time: ${lg.sets||'–'} sets · ${esc(lg.reps||'–')}${lg.weight_kg?` @ ${lg.weight_kg} kg`:''} (${lg.day})</div>`:''}${hint?`<div class="small" style="color:var(--accent)">💡 ${esc(hint)}</div>`:''}
    <div class="fields">${cardio?`<div><label>Minutes done</label><input type="text" name="reps_${ex.key}" inputmode="numeric" value="${esc(lo?lo.reps:'')}"></div>`:
     `<div><label>Sets done</label><input type="number" min="0" max="20" name="sets_${ex.key}" value="${lo&&lo.sets!=null?lo.sets:''}"></div><div><label>Reps (10,10,9)</label><input type="text" name="reps_${ex.key}" value="${esc(lo?lo.reps:'')}"></div>
      <div><label>Weight (kg)</label><input type="number" step="0.5" min="0" name="weight_${ex.key}" inputmode="decimal" value="${lo&&lo.weight_kg?lo.weight_kg:''}"></div>`}
     <div><label>&nbsp;</label><label style="font-weight:500;color:inherit"><input type="checkbox" name="done_${ex.key}" value="1" style="width:auto;max-width:none" ${lo?'checked':''}> Done</label></div></div>
    ${ex.alts.length?`<details><summary>Machine busy or not available? Use instead…</summary><ul style="margin:.3em 0;padding-left:1.1em">${ex.alts.map(a=>`<li><a href="#" data-swap="${ex.key}>${a.key}">${esc(a.name)}</a></li>`).join('')}</ul></details>`:''}</div>`}).join('')+
   (isToday?'<p><button>Save workout</button></p>':'<p class="muted small">You can log a session on the day you do it.</p>')+'</form>';
  if(day.type==='strength')h+=`<details class="card"><summary>Cool-down (3 min)</summary>${prog.cooldown.map(x=>`<div class="ex"><div class="nm">${esc(x.name)}</div><div class="small muted">${esc(x.cue)}</div></div>`).join('')}</details>
   <div class="card soft small"><b>How hard?</b> Finish each set with 2–3 reps left in the tank. Stop any exercise that causes sharp or joint pain. At the top of the rep range on every set, add about 2.5 kg (upper body) or 5 kg (lower body) next time.${(u.profile.level||'beginner')==='beginner'?'<br>First two weeks: do 2 sets of each exercise and focus on technique.':''}</div>`;
  page('train',h);
  $('#upd').onclick=()=>{MISSING.v=[...app.querySelectorAll('[data-miss]:checked')].map(x=>x.dataset.miss);SWAPS[dow]=[];route()};
  app.querySelectorAll('[data-swap]').forEach(a=>a.onclick=e=>{e.preventDefault();(SWAPS[dow]=SWAPS[dow]||[]).push(a.dataset.swap);route()});
  const wf=$('#wf');wf.onsubmit=e=>{e.preventDefault();const f=new FormData(wf),rows=[];
    f.getAll('ex').forEach(k=>{const reps=(f.get('reps_'+k)||'').trim().slice(0,40),w=parseFloat(f.get('weight_'+k))||null,sets=f.get('sets_'+k)===''||f.get('sets_'+k)==null?null:parseInt(f.get('sets_'+k)),dn=f.get('done_'+k)==='1';
      if(reps||w||sets||dn){const nm=wf.querySelector(`[name=ex][value="${k}"]`).parentNode.querySelector('.nm').textContent.replace(/^\d+\.\s*/,'');rows.push({day:today,session_key:day.session_key,exercise_key:k,exercise_name:nm,sets,reps,weight_kg:w})}});
    u.logs=u.logs.filter(l=>!(l.day===today&&l.session_key===day.session_key)).concat(rows);save();flash=rows.length?'Workout saved. Nice work!':'Nothing to save yet.';route()}}

function chart(points,unit){const pts=points.filter(p=>p[1]!=null);if(!pts.length)return'<p class="muted">No data yet.</p>';
  const W=640,H=200,pl=44,pr=14,pt=14,pb=26,w=W-pl-pr,h=H-pt-pb,vals=pts.map(p=>p[1]);let lo=Math.min(...vals),hi=Math.max(...vals);if(hi-lo<1e-9){lo-=1;hi+=1}const m=(hi-lo)*.15;lo-=m;hi+=m;
  const x=i=>pl+(pts.length===1?w/2:w*i/(pts.length-1)),y=v=>pt+h-(v-lo)/(hi-lo)*h;
  let s=`<svg viewBox="0 0 ${W} ${H}" class="chart" role="img" xmlns="http://www.w3.org/2000/svg">`;
  for(let t=0;t<4;t++){const gv=lo+(hi-lo)*t/3,gy=y(gv);s+=`<line x1="${pl}" y1="${gy.toFixed(1)}" x2="${W-pr}" y2="${gy.toFixed(1)}" class="grid"/><text x="${pl-6}" y="${(gy+4).toFixed(1)}" text-anchor="end" font-size="11" fill="currentColor">${gv.toFixed(1)}</text>`}
  s+=`<polyline class="line" fill="none" points="${pts.map((p,i)=>x(i).toFixed(1)+','+y(p[1]).toFixed(1)).join(' ')}"/>`;
  pts.forEach((p,i)=>{s+=`<circle cx="${x(i).toFixed(1)}" cy="${y(p[1]).toFixed(1)}" r="3.5" fill="currentColor"/>`});
  s+=`<text x="${pl}" y="${H-6}" font-size="11" fill="currentColor">${pts[0][0].slice(5)}</text><text x="${W-pr}" y="${H-6}" text-anchor="end" font-size="11" fill="currentColor">${pts[pts.length-1][0].slice(5)}</text></svg>`;return s+(unit?`<div class="muted small">${unit}</div>`:'')}
function vProgress(){const c=ctx(),u=U();
  const wp=[...u.reports.map(r=>[r.report_date,r.weight_kg]),...Object.entries(u.checkins).filter(([d,k])=>k.weight_kg!=null).map(([d,k])=>[d,k.weight_kg])].sort((a,b)=>a[0]<b[0]?-1:1);
  const reps=[...u.reports].sort((a,b)=>a.report_date<b.report_date?-1:1);
  const byEx={};u.logs.forEach(l=>{if(l.weight_kg)(byEx[l.exercise_key+'|'+l.exercise_name]=byEx[l.exercise_key+'|'+l.exercise_name]||[]).push([l.day,l.weight_kg])});
  page('progress',`<div class="row between"><h1>Progress</h1><a class="btn small" href="#/report">+ Body report</a></div>
  <div class="card"><h2>Weight (kg)</h2>${chart(wp)}</div>
  <div class="card"><h2>Body fat (%)</h2>${chart(reps.map(r=>[r.report_date,r.body_fat_pct]))}</div>
  <div class="card"><h2>Skeletal muscle (kg)</h2>${chart(reps.map(r=>[r.report_date,r.muscle_kg]))}</div>
  <div class="card"><h2>Lifting weights</h2>${Object.entries(byEx).map(([k,v])=>`<div class="ex"><div class="nm">${esc(k.split('|')[1])}</div><div class="small muted">${v.sort((a,b)=>a[0]<b[0]?-1:1).slice(-8).map(p=>p[1]).join(' → ')} kg</div></div>`).join('')||'<p class="muted">Log a workout with weights to see progress.</p>'}</div>`)}

function vCheckin(){const t=iso(),c=U().checkins[t]||{};
  page('home',`<h1>Today's check-in</h1><form id="cf" class="card"><div class="grid g2">
  <div><label>Weight (kg)</label><input type="number" step="0.1" name="weight_kg" inputmode="decimal" value="${c.weight_kg??''}"></div><div><label>Steps</label><input type="number" name="steps" value="${c.steps??''}"></div>
  <div><label>Water (ml)</label><input type="number" name="water_ml" step="100" value="${c.water_ml??''}"></div><div><label>Sleep (hours)</label><input type="number" step="0.5" name="sleep_h" value="${c.sleep_h??''}"></div></div>
  <p><button>Save</button></p></form>`);
  $('#cf').onsubmit=e=>{e.preventDefault();const f=new FormData($('#cf')),o={};['weight_kg','steps','water_ml','sleep_h'].forEach(k=>{const v=parseFloat(f.get(k));o[k]=isNaN(v)?null:v});U().checkins[t]=o;save();flash='Saved.';go('#/')}}

function vCoach(){const c=ctx();if(needSetup(c))return route();const u=U(),today=iso(),s21=addDays(today,-21),s7=addDays(today,-7);
  const wp=[...Object.entries(u.checkins).filter(([d,k])=>d>=s21&&k.weight_kg!=null).map(([d,k])=>[d,k.weight_kg]),...u.reports.filter(r=>r.report_date>=s21).map(r=>[r.report_date,r.weight_kg])];
  const l7=Object.entries(u.checkins).filter(([d])=>d>=s7).map(([d,k])=>k),col=k=>l7.map(x=>x[k]).filter(v=>v!=null);
  const done=new Set(u.logs.filter(l=>l.day>=s7).map(l=>l.day)).size,prog=J('week_summary',JSON.stringify(u.profile),c.goal.key,c.safety.light_only),planned=prog.days.filter(d=>d.type==='strength'||d.type==='cardio').length;
  const ticked=Object.entries(u.meal_checks).filter(([d])=>d>=s7).reduce((a,[d,v])=>a+v.length,0),mpd=+u.profile.meals_per_day||4;
  const msgs=J('review',c.goal.key,c.targets?JSON.stringify(c.targets):'',JSON.stringify(wp),JSON.stringify(col('steps')),JSON.stringify(col('water_ml')),JSON.stringify(col('sleep_h')),done,planned,ticked,ticked?mpd*7:0,c.report.report_date,today);
  page('coach',`<h1>Weekly coach</h1>`+banners(c)+msgs.map(m=>`<div class="card"><h2>${m.level==='good'?'✅ ':m.level==='warn'?'⚠️ ':'ℹ️ '}${esc(m.title)}</h2><p>${esc(m.text)}</p>${m.adjust?`<button data-adj="${m.adjust}">Apply ${m.adjust>0?'+':''}${m.adjust} kcal a day</button>`:''}</div>`).join('')+
   `<div class="card soft small">For a deeper monthly review, export your log in Me → Backup and paste it to Claude.</div>`);
  app.querySelectorAll('[data-adj]').forEach(b=>b.onclick=()=>{const p=u.profile;p.kcal_adjust=Math.max(-300,Math.min(300,(p.kcal_adjust||0)+ +b.dataset.adj));save();flash='Calories adjusted. A new meal plan was created.';route()})}

const RF=[['weight_kg','Weight (kg)',30,300,1],['body_fat_pct','Body fat (%)',3,70,1],['muscle_kg','Skeletal muscle mass (kg)',10,80,0],['visceral_level','Visceral fat level',1,30,0],['body_water_pct','Body water (%)',30,80,0],['bmr_kcal','BMR from the scan (kcal)',800,4000,0],['waist_cm','Waist (cm)',40,200,0],['hip_cm','Hip (cm)',50,200,0],['chest_cm','Chest (cm)',50,200,0],['arm_cm','Arm (cm)',15,70,0],['thigh_cm','Thigh (cm)',25,100,0]];
function vReport(){const u=U(),last=[...u.reports].pop()||{};
  page('progress',`<h1>Body-composition report</h1><p class="muted">Enter the numbers from your latest scan (InBody, Tanita, gym scanner…). Your goal, calories and plans are always built from this report. Only weight and body fat are required.</p>
  <form id="rf" class="card"><label>Report date</label><input type="date" name="report_date" value="${iso()}" max="${iso()}" required><div class="grid g2">${RF.map(([k,l,lo,hi,r])=>`<div><label>${l}${r?' *':''}</label><input type="number" step="0.1" min="${lo}" max="${hi}" name="${k}" ${r?'required':''} inputmode="decimal" value="${['weight_kg','body_fat_pct'].includes(k)?'':(last[k]??'')}"></div>`).join('')}</div>
  <p><button>Save report</button></p></form>`);
  $('#rf').onsubmit=e=>{e.preventDefault();const f=new FormData($('#rf')),r={id:Date.now(),report_date:f.get('report_date')};
    RF.forEach(([k])=>{const v=parseFloat(f.get(k));r[k]=isNaN(v)?null:v});
    if(r.muscle_kg&&r.muscle_kg>r.weight_kg){alert('Skeletal muscle cannot be heavier than your total weight.');return}
    u.reports.push(r);u.profile.kcal_adjust=0;u.plan=null;save();flash='Report saved. Your goal, calories and plans were recalculated.';go('#/')}}

function vMe(){const u=U(),p=u.profile,sc=new Set((p.conditions||'').split(',')),si=new Set((p.injuries||'').split(',')),se=new Set((p.equipment||'').split(',')),
  ex=(p.exclusions||'').split(',').map(s=>s.trim()).filter(Boolean),tok=ex.filter(x=>K.allergens.includes(x)),free=ex.filter(x=>!K.allergens.includes(x)).join(', ');
  const sel=(n,opts,cur)=>`<select name="${n}">${opts.map(([v,l])=>`<option value="${v}" ${String(cur)===String(v)?'selected':''}>${esc(l)}</option>`).join('')}</select>`;
  page('me',`<h1>My profile</h1><form id="pf"><div class="card"><h2>About you</h2><div class="grid g2">
  <div><label>Sex</label>${sel('sex',[['','Choose…'],['male','Male'],['female','Female']],p.sex||'')}</div><div><label>Date of birth</label><input type="date" name="birth_date" value="${p.birth_date||''}" required></div></div>
  <div class="grid g2"><div><label>Height (cm)</label><input type="number" name="height_cm" step="0.1" min="120" max="230" value="${p.height_cm||''}" required></div><div><label>Daily activity</label>${sel('activity',Object.entries(K.activity),p.activity||'sedentary')}</div></div></div>
  <div class="card"><h2>Medical history & safety</h2><p class="muted small">Used only to keep your plan safe. It stays on this phone.</p><label>Health conditions</label><div class="checks">${Object.entries(K.conditions).map(([k,v])=>`<label><input type="checkbox" name="conditions" value="${k}" ${sc.has(k)?'checked':''}> ${esc(v)}</label>`).join('')}</div>
  <label>Injuries or painful areas</label><div class="checks">${K.injuries.map(([k,v])=>`<label><input type="checkbox" name="injuries" value="${k}" ${si.has(k)?'checked':''}> ${esc(v)}</label>`).join('')}</div></div>
  <div class="card"><h2>Food preferences</h2><div class="grid g2"><div><label>Eating style</label>${sel('diet',['omnivore','pescatarian','vegetarian','vegan'].map(x=>[x,x]),p.diet||'omnivore')}</div><div><label>Meals per day</label>${sel('meals_per_day',[3,4,5].map(x=>[x,x]),p.meals_per_day||4)}</div></div>
  <label>Allergies / foods to avoid</label><div class="checks">${K.allergens.map(a=>`<label><input type="checkbox" name="excl" value="${a}" ${tok.includes(a)?'checked':''}> ${a}</label>`).join('')}</div>
  <label>Other foods you dislike (comma separated)</label><input type="text" name="excl_free" value="${esc(free)}" placeholder="e.g. mushroom, lamb"><p class="muted small">All meals are halal.</p></div>
  <div class="card"><h2>Training setup</h2><div class="grid g2"><div><label>Strength days per week</label>${sel('strength_days',[2,3,4].map(x=>[x,x]),p.strength_days||3)}</div><div><label>Experience</label>${sel('level',[['beginner','Beginner'],['intermediate','Intermediate']],p.level||'beginner')}</div></div>
  <label>Equipment you have access to</label><div class="row" style="margin-bottom:8px"><button type="button" class="secondary small" data-preset="">Bodyweight only</button><button type="button" class="secondary small" data-preset="${K.presets.home.join(',')}">Home</button><button type="button" class="secondary small" data-preset="${K.presets.gym.join(',')}">Full gym</button></div>
  <div class="checks">${K.equipment.map(([k,v])=>`<label><input type="checkbox" name="equipment" value="${k}" ${se.has(k)?'checked':''}> ${esc(v)}</label>`).join('')}</div></div>
  <p><button>Save profile</button></p></form>
  <div class="card"><h2>People on this phone</h2><div class="row"><input type="text" id="nn" placeholder="Add a person (e.g. Wife)"><button class="secondary small" id="an">Add</button></div>
  <div class="row" style="margin-top:8px"><input type="text" id="rn" placeholder="Rename current person"><button class="secondary small" id="rnb">Rename</button></div></div>
  <div class="card"><h2>Backup</h2><p class="muted small">Data lives only on this phone. Export a backup now and then, or to share your log with Claude.</p><div class="row"><button class="secondary" id="bk">Export backup file</button><button class="secondary" id="cp">Copy training log</button></div><div class="row" style="margin-top:8px"><input type="file" id="im" accept=".json"></div></div>`);
  app.querySelectorAll('[data-preset]').forEach(b=>b.onclick=()=>{const l=b.dataset.preset.split(',').filter(Boolean);app.querySelectorAll('[name=equipment]').forEach(cb=>cb.checked=l.includes(cb.value))});
  $('#pf').onsubmit=e=>{e.preventDefault();const o=formData($('#pf')),g=k=>one(o,k);
    const exc=[...(o.excl||[]),...(g('excl_free')||'').split(',').map(s=>s.trim()).filter(Boolean)].join(',');
    Object.assign(p,{sex:g('sex'),birth_date:g('birth_date'),height_cm:parseFloat(g('height_cm')),activity:g('activity'),diet:g('diet'),meals_per_day:+g('meals_per_day'),strength_days:+g('strength_days'),level:g('level'),
      conditions:(o.conditions||[]).join(','),injuries:(o.injuries||[]).join(','),equipment:(o.equipment||[]).join(','),exclusions:exc});u.plan=null;save();flash='Profile saved.';go('#/')};
  $('#an').onclick=()=>{const n=$('#nn').value.trim();if(n&&!S.users[n]){S.users[n]=blank();S.cur=n;save();route()}};
  $('#rnb').onclick=()=>{const n=$('#rn').value.trim();if(n&&!S.users[n]){S.users[n]=S.users[S.cur];delete S.users[S.cur];S.cur=n;save();route()}};
  $('#bk').onclick=()=>{const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([JSON.stringify(S)],{type:'application/json'}));a.download='fittrack-backup.json';a.click()};
  $('#cp').onclick=()=>{const t=logText();(navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(()=>alert('Copied. Paste it to Claude.'),()=>prompt('Copy this log:',t))};
  $('#im').onchange=e=>{const f=e.target.files[0];if(f)f.text().then(t=>{S=JSON.parse(t);save();route()})}}
function logText(){const u=U(),L=[`Training log for ${S.cur} (exported ${iso()})`];const r=[...u.reports].sort((a,b)=>a.report_date<b.report_date?-1:1).pop();
  if(r)L.push(`Latest body report ${r.report_date}: ${r.weight_kg} kg, ${r.body_fat_pct}% fat${r.muscle_kg?`, muscle ${r.muscle_kg} kg`:''}`);
  const w=Object.entries(u.checkins).filter(([d,k])=>k.weight_kg).sort().slice(-12).map(([d,k])=>`${d}:${k.weight_kg}`);if(w.length)L.push('Weights: '+w.join(', '));
  const byDay={};u.logs.slice(-120).forEach(l=>(byDay[l.day]=byDay[l.day]||[]).push(`${l.exercise_name} ${l.sets||'?'}x[${l.reps||'?'}]@${l.weight_kg||0}kg`));
  Object.keys(byDay).sort().forEach(d=>L.push(d+': '+byDay[d].join(' | ')));return L.join('\n')}

// ---------- router ----------
function route(){if(!B)return;const [path,qs]=(location.hash||'#/').slice(1).split('?'),q=Object.fromEntries(new URLSearchParams(qs||'')),seg=path.split('/').filter(Boolean);
  try{({'':()=>vHome(),food:()=>vFood(q),shopping:()=>vShop(),train:()=>seg[1]!=null?vDay(+seg[1]):vTrain(),progress:()=>vProgress(),checkin:()=>vCheckin(),coach:()=>vCoach(),report:()=>vReport(),me:()=>vMe()}[seg[0]||'']||vHome)()}
  catch(e){app.innerHTML=`<div class="card"><h2>Something went wrong</h2><pre style="white-space:pre-wrap">${esc(e.message||e)}</pre><p class="small muted">Your data is safe. Try Me → Export backup, then reload.</p></div>`;console.error(e)}}
window.addEventListener('hashchange',route);

async function boot(){load();
  try{py=await loadPyodide({indexURL:new URL('pyodide/',location.href).href});py.FS.mkdirTree('/app');
    for(const m of PYFILES){const t=await (await fetch(`py/${m}.py`)).text();py.FS.writeFile(`/app/${m}.py`,t)}
    py.runPython("import sys; sys.path.insert(0,'/app'); import bridge");B=py.pyimport('bridge');K=JSON.parse(B.constants());
    route()}catch(e){app.innerHTML=`<div class="card"><h2>Couldn't start</h2><p>The trainer engine needs an internet connection the first time. Check your connection and reload.</p><pre class="small">${esc(e.message||e)}</pre></div>`}}
boot();
if('serviceWorker' in navigator)navigator.serviceWorker.register('sw.js').catch(()=>{});
