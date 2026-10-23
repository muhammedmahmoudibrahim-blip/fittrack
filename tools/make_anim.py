"""Original stick-figure exercise animations for FitTrack (drawn with Pillow, no external art).
Usage: python3 make_anim.py OUTDIR [preview]   -> OUTDIR/<key>.gif  (and preview sheet with 'preview')"""
import math, sys, os
from PIL import Image, ImageDraw, ImageFont

W, H, S = 360, 270, 2          # canvas and supersampling
FLOOR = 238
BG, FLOORC, NEAR, FAR, SKIN, BAND, PROP, TXT, ARM = '#f1f5f9', '#cbd5e1', '#0f766e', '#7fbab4', '#fbd5a5', '#f97316', '#64748b', '#334155', '#0b3b37'
L = dict(torso=68, uarm=34, farm=32, thigh=46, shin=44, foot=15, head=12, neck=8)

def P(a, b): return (a[0], a[1])
def pol(o, ang, ln): r = math.radians(ang); return (o[0] + ln * math.cos(r), o[1] + ln * math.sin(r))

def side_fk(p):
    """p: dict of angles (deg, image coords: 0=right, 90=down, -90=up) -> joints."""
    g = lambda k, d=None: p.get(k, d)
    t = g('t', -90)
    hip = (0.0, 0.0)
    neck = pol(hip, t, L['torso'])
    head = pol(neck, t + g('h', 0), L['neck'] + L['head']); head = (head[0] + g('hx', 0), head[1])
    J = dict(hip=hip, neck=neck, head=head)
    for s, suf in (('n', 'n'), ('f', 'f')):
        an = g('a' + s, g('an', 90)); fo = g('f' + s, g('fn', 90))
        el = pol(neck, an, L['uarm']); wr = pol(el, fo, L['farm'])
        th = g('t' + s, g('tn', 90)); sh = g('s' + s, g('sn', 90)); ft = g('o' + s, g('on', 0))
        kn = pol(hip, th, L['thigh']); an_ = pol(kn, sh, L['shin']); to = pol(an_, ft, L['foot'])
        J.update({'elbow_' + suf: el, 'wrist_' + suf: wr, 'knee_' + suf: kn, 'ankle_' + suf: an_, 'toe_' + suf: to})
    return J

def place(J, pin_joint, pin_x, ground):
    dx = pin_x - J[pin_joint][0]
    dy = FLOOR - max(J[j][1] for j in ground)
    return {k: (v[0] + dx, v[1] + dy) for k, v in J.items()}

def line(d, a, b, w, c): d.line([(a[0]*S, a[1]*S), (b[0]*S, b[1]*S)], fill=c, width=int(w*S)); [d.ellipse([(q[0]-w/2)*S, (q[1]-w/2)*S, (q[0]+w/2)*S, (q[1]+w/2)*S], fill=c) for q in (a, b)]
def dot(d, c, r, col, outline=None): d.ellipse([(c[0]-r)*S, (c[1]-r)*S, (c[0]+r)*S, (c[1]+r)*S], fill=col, outline=outline, width=S)
def text(d, xy, s, col=TXT, size=13):
    try: f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', size*S)
    except Exception: f = ImageFont.load_default()
    d.text((xy[0]*S, xy[1]*S), s, fill=col, font=f)

def draw_side(d, J, show=('n', 'f')):
    for s, col, w in (('f', FAR, 8), ('n', NEAR, 9)):
        line(d, J['hip'], J['knee_' + s], w + 1, col); line(d, J['knee_' + s], J['ankle_' + s], w, col); line(d, J['ankle_' + s], J['toe_' + s], 6, col)
        if s == 'f': line(d, J['neck'], J['elbow_f'], w - 1, col); line(d, J['elbow_f'], J['wrist_f'], w - 2, col)
    line(d, J['hip'], J['neck'], 15, NEAR); line(d, J['neck'], J['head'], 7, NEAR)
    dot(d, J['head'], L['head'], SKIN, NEAR)
    if 'hx' in J: pass
    for a_, b_, w_ in ((J['neck'], J['elbow_n'], 8), (J['elbow_n'], J['wrist_n'], 7)): line(d, a_, b_, w_ + 3, 'white')
    for a_, b_, w_ in ((J['neck'], J['elbow_n'], 8), (J['elbow_n'], J['wrist_n'], 7)): line(d, a_, b_, w_, ARM)
    dot(d, J['wrist_n'], 4, SKIN, ARM)

def front_pose(p):
    cx = 180
    hip = (cx, 150); neck = (cx, 150 - 66)
    J = dict(hip=hip, neck=neck, head=(cx, neck[1] - 22))
    for side, sgn in (('r', 1), ('l', -1)):
        ang = lambda a: a if sgn == 1 else 180 - a
        sh = (cx + sgn * 20, neck[1] + 4)
        el = pol(sh, ang(p['a']), L['uarm'] + 2); wr = pol(el, ang(p['f']), L['farm'] + 2)
        hp = (cx + sgn * 10, hip[1]); kn = pol(hp, ang(90 - p.get('leg', 6)), 46); an = pol(kn, ang(90 - p.get('leg', 6)), 44)
        J.update({'sh_' + side: sh, 'el_' + side: el, 'wr_' + side: wr, 'hp_' + side: hp, 'kn_' + side: kn, 'an_' + side: an, 'to_' + side: (an[0] + sgn * 9, an[1] + 1)})
    return J
def draw_front(d, J):
    for s in 'rl':
        line(d, J['hp_' + s], J['kn_' + s], 10, NEAR); line(d, J['kn_' + s], J['an_' + s], 9, NEAR); line(d, J['an_' + s], J['to_' + s], 6, NEAR)
    line(d, (J['sh_l'][0], J['sh_l'][1]), (J['sh_r'][0], J['sh_r'][1]), 9, NEAR)
    line(d, J['neck'], J['hip'], 22, NEAR)
    dot(d, J['head'], 13, SKIN, NEAR)
    for s in 'rl':
        line(d, J['sh_' + s], J['el_' + s], 8, NEAR); line(d, J['el_' + s], J['wr_' + s], 7, NEAR); dot(d, J['wr_' + s], 4, SKIN, NEAR)

def ease(t): return t * t * (3 - 2 * t)
def lerp(a, b, t):
    out = {}
    for k in set(a) | set(b):
        x, y = a.get(k, b.get(k)), b.get(k, a.get(k)); out[k] = x + (y - x) * t
    return out

# ---------- exercise definitions ----------
# each: kind, poseA, poseB, optional pin, ground list, prop(draw, J, t)
def band(d, a, b, w=3): line(d, a, b, w, BAND)
def wallstrip(d, x, w=14): d.rectangle([(x-w)*S, 20*S, x*S, FLOOR*S], fill='#e2e8f0'); d.line([x*S, 20*S, x*S, FLOOR*S], fill=PROP, width=2*S)

EXS = {}
def ex(key, kind='side', **kw): EXS[key] = dict(kind=kind, **kw)

# wall sit
ex('wall_sit', pin=('hip', 118), ground=['ankle_n', 'toe_n'],
   A=dict(t=-90, tn=90, sn=90, an=100, fn=95), B=dict(t=-90, tn=0, sn=90, an=35, fn=0),
   prop=None, wall_x=100)
# bridge walk-out (lying on back, head left)
ex('hamstring_walkout', pin=('neck', 70), ground=['neck', 'toe_n', 'ankle_n'],
   A=dict(t=165, h=-10, tn=-48, sn=62, on=0, an=15, fn=15), B=dict(t=160, h=-10, tn=-22, sn=22, on=0, an=15, fn=15),
   prop=lambda d, J, t: None)
# band chest press
def chest_prop(d, J, t):
    back = (J['neck'][0] - 16, J['neck'][1] + 14)
    band(d, back, J['wrist_n']); band(d, back, J['wrist_f'])
ex('band_chest_press', pin=('ankle_n', 150), ground=['toe_n'],
   A=dict(t=-90, tn=88, sn=92, an=125, fn=-15, af=125, ff=-15), B=dict(t=-90, tn=88, sn=92, an=0, fn=0, af=0, ff=0), prop=chest_prop)
# band row (seated)
def row_prop(d, J, t): band(d, J['toe_n'], J['wrist_n']); band(d, J['toe_f'], J['wrist_f'])
ex('band_row', pin=('hip', 105), ground=['hip', 'toe_n'],
   A=dict(t=-90, tn=-2, sn=-2, on=-80, an=5, fn=5, af=5, ff=5), B=dict(t=-90, tn=-2, sn=-2, on=-80, an=158, fn=8, af=158, ff=8), prop=row_prop)
# band lat pulldown (standing, band from above in front)
def pulldown_prop(d, J, t):
    anc = (J['neck'][0] + 60, 22); dot(d, anc, 5, PROP); band(d, anc, J['wrist_n']); band(d, anc, J['wrist_f'])
ex('band_pulldown', pin=('ankle_n', 150), ground=['toe_n'],
   A=dict(t=-90, tn=88, sn=92, an=-62, fn=-66, af=-62, ff=-66), B=dict(t=-90, tn=88, sn=92, an=100, fn=-72, af=100, ff=-72), prop=pulldown_prop)
# band curl (band under foot)
def curl_prop(d, J, t): band(d, J['toe_n'], J['wrist_n'])
ex('band_curl', pin=('ankle_n', 150), ground=['toe_n'],
   A=dict(t=-90, tn=88, sn=92, an=98, fn=96), B=dict(t=-90, tn=88, sn=92, an=98, fn=-62), prop=curl_prop)
# towel isometric curl
def towel_prop(d, J, t): band(d, J['toe_n'], J['wrist_n'], w=5); d.line([J['toe_n'][0]*S-12*S, J['toe_n'][1]*S+2*S, J['toe_n'][0]*S+10*S, J['toe_n'][1]*S+2*S], fill=BAND, width=5*S)
ex('towel_curl', pin=('ankle_n', 150), ground=['toe_n'],
   A=dict(t=-90, tn=88, sn=92, an=98, fn=60), B=dict(t=-90, tn=88, sn=92, an=98, fn=20), prop=towel_prop, label='HOLD – pull up on the towel, don\'t let it move')
# band triceps pushdown
def push_prop(d, J, t):
    anc = (J['neck'][0] + 22, 22); dot(d, anc, 5, PROP); band(d, anc, J['wrist_n']); band(d, anc, J['wrist_f'])
ex('band_pushdown', pin=('ankle_n', 150), ground=['toe_n'],
   A=dict(t=-90, tn=88, sn=92, an=95, fn=-35, af=95, ff=-35), B=dict(t=-90, tn=88, sn=92, an=95, fn=88, af=95, ff=88), prop=push_prop)
# bird dog (quadruped; head right; near leg + far arm extend)
ex('bird_dog', pin=('wrist_n', 235), ground=['wrist_n', 'wrist_f', 'knee_n', 'knee_f'],
   A=dict(t=-4, h=6, an=90, fn=90, af=90, ff=90, tn=90, sn=180, tf=90, sf=180, on=180, of=180),
   B=dict(t=-4, h=6, an=90, fn=90, af=-3, ff=-3, tn=175, sn=175, tf=90, sf=180, on=180, of=180),
   prop=None, label='Reach opposite arm and leg long, hips level')
# band pull-through
def pt_prop(d, J, t):
    anc = (60, FLOOR - 8); dot(d, anc, 5, PROP); band(d, anc, J['wrist_n']); band(d, anc, J['wrist_f'])
ex('band_pull_through', pin=('ankle_n', 175), ground=['toe_n'],
   A=dict(t=-38, h=-12, tn=70, sn=100, an=112, fn=118, af=112, ff=118), B=dict(t=-90, tn=88, sn=92, an=92, fn=95, af=92, ff=95), prop=pt_prop)
# chin tuck (head/neck close-up)
ex('chin_tuck', pin=('hip', 150), ground=['ankle_n', 'toe_n'],
   A=dict(t=-90, hx=24, an=92, fn=92, tn=90, sn=90), B=dict(t=-90, hx=0, an=92, fn=92, tn=90, sn=90), prop=None, label='Glide the head straight back (make a double chin)')
# wall angels (front)
EXS['wall_angel'] = dict(kind='front', A=dict(a=-2, f=-92, leg=4), B=dict(a=-52, f=-80, leg=4), wall=True, label='Keep elbows, wrists and back on the wall')
EXS['band_lateral_raise'] = dict(kind='front', A=dict(a=78, f=82, leg=8), B=dict(a=2, f=2, leg=8), bandfeet=True)
# top-down: prone Y-T-W
EXS['prone_ytw'] = dict(kind='ytw')

def draw_ytw(d, t):
    cx, y0 = 180, 40
        # body (top view, face down): head at top
    dot(d, (cx, 84), 14, SKIN, NEAR); line(d, (cx, 100), (cx, 168), 28, NEAR); line(d, (cx-9, 168), (cx-9, 232), 13, FAR); line(d, (cx+9, 168), (cx+9, 232), 13, FAR)
    sh = {'l': (cx-17, 108), 'r': (cx+17, 108)}
    shapes = {'Y': [(-70, -70), (-70, -68)], 'T': [(-30, 0), (-30, 0)], 'W': [(-30, 20), (-34, -55)]}
    # arm pose per letter: (upper dir, forearm dir) in degrees, mirrored for left
    pose = {'Y': (-62, -62), 'T': (0, 0), 'W': (38, -78)}
    keys = ['Y', 'T', 'W']; i = int(t * 3) % 3; f = ease((t * 3) % 1)
    a0, a1 = pose[keys[i]], pose[keys[(i+1) % 3]]
    ua = a0[0] + (a1[0] - a0[0]) * f; fa = a0[1] + (a1[1] - a0[1]) * f
    for s, sg in (('r', 1), ('l', -1)):
        ang = lambda a: a if sg == 1 else 180 - a
        el = pol(sh[s], ang(ua), 36); wr = pol(el, ang(fa), 34)
        line(d, sh[s], el, 9, ARM); line(d, el, wr, 8, ARM); dot(d, wr, 4, SKIN, ARM)
    text(d, (250, 120), keys[i] if f < .5 else keys[(i+1) % 3], NEAR, 34)
    text(d, (14, 12), 'Face down, thumbs up. Lift arms into Y, T, W.', TXT, 12)

def draw_rot(d, t):
    # top-down side-lying open book: body horizontal, knees stacked forward
    d.rectangle([0, 0, W*S, H*S], fill=BG)
    text(d, (14, 12), 'Knees stay stacked, top arm opens like a book', TXT, 12)
    base = (150, 150)
    dot(d, (112, 150), 15, SKIN, NEAR)
    line(d, (130, 150), (232, 150), 26, NEAR)               # torso
    line(d, (232, 150), (276, 118), 14, NEAR); line(d, (276, 118), (250, 100), 13, NEAR)   # thighs/shins stacked
    line(d, (232, 156), (278, 126), 12, FAR)
    sh = (140, 150); f = 0.5 - 0.5 * math.cos(2 * math.pi * t)
    line(d, sh, (60, 150), 8, FAR)                              # bottom arm stays forward
    d.arc([(sh[0]-62)*S, (sh[1]-62)*S, (sh[0]+62)*S, (sh[1]+62)*S], 180, 355, fill='#94a3b8', width=2*S)
    tip = pol(sh, 180 + f * 175, 62)                            # top arm opens like a book
    line(d, sh, tip, 11, 'white'); line(d, sh, tip, 8, ARM); dot(d, tip, 4, SKIN, ARM)

def render(key, t):
    e = EXS[key]; im = Image.new('RGB', (W*S, H*S), BG); d = ImageDraw.Draw(im)
    d.rectangle([0, FLOOR*S, W*S, H*S], fill=FLOORC)
    if e['kind'] == 'ytw': draw_ytw(d, t); return im.resize((W, H), Image.LANCZOS)
    if e['kind'] == 'rot': draw_rot(d, t); return im.resize((W, H), Image.LANCZOS)
    if e['kind'] == 'front':
        if e.get('wall'): d.rectangle([110*S, 20*S, 250*S, FLOOR*S], fill='#e2e8f0')
        p = lerp(e['A'], e['B'], ease(t)); J = front_pose(p)
        if e.get('bandfeet'):
            for s in 'rl': band(d, J['to_' + s], J['wr_' + s])
        draw_front(d, J)
    else:
        p = lerp(e['A'], e['B'], ease(t)); J = side_fk(p)
        pj, px = e['pin']; J = place(J, pj, px, e['ground'])
        if key == 'bird_dog':      # lower body so knees/hands rest on the floor
            pass
        if e.get('wall_x'): wallstrip(d, e['wall_x'])
        draw_side(d, J)
        if e.get('prop'): e['prop'](d, J, t)
    if e.get('label'): text(d, (14, 14), e['label'], TXT, 11)
    return im.resize((W, H), Image.LANCZOS)

def frames(key, hold=3, n=8):
    seq = [0.0] * hold + [i / n for i in range(1, n)] + [1.0] * hold + [1 - i / n for i in range(1, n)]
    if EXS[key]['kind'] in ('ytw', 'rot'): seq = [i / 24 for i in range(24)]
    return [render(key, t) for t in seq], (80 if EXS[key]['kind'] in ('ytw', 'rot') else 90)

if __name__ == '__main__':
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    if len(sys.argv) > 2 and sys.argv[2] == 'preview':
        keys = list(EXS); sheet = Image.new('RGB', (W*4, H*((len(keys)*2+3)//4)), 'white')
        for i, k in enumerate(keys):
            for j, t in enumerate((0.0, 1.0 if EXS[k]['kind'] in ('side', 'front') else 0.5)):
                n = i*2 + j; sheet.paste(render(k, t), ((n % 4)*W, (n//4)*H))
                ImageDraw.Draw(sheet).text(((n % 4)*W+6, (n//4)*H+4), f'{k} {"A" if j == 0 else "B"}', fill='black')
        sheet.save(out + '/preview.png'); print('preview', len(keys))
    else:
        for k in EXS:
            fr, dur = frames(k); q = [f.quantize(colors=32, method=Image.MEDIANCUT, dither=Image.Dither.NONE) for f in fr]
            q[0].save(f'{out}/{k}.gif', save_all=True, append_images=q[1:], duration=dur, loop=0, optimize=True, disposal=2)
            print(k, round(os.path.getsize(f'{out}/{k}.gif')/1024), 'KB')
