"""Builds every animated SVG in ../assets and the profile README from the portfolio's assets."""
import math, os, random
from lib import *

W = 1000


# =====================================================================
# 1. INTRO: gate -> beat-synced identity montage -> LET'S GO (loops)
# =====================================================================
def intro():
    H = 560
    d = Doc(W, H, 'Ryan Panda: they call me Agency. Looping intro montage.')
    G = 2.6           # gate screen length; montage cue times from the site are offset by this
    L = G + 17.2      # full loop
    T = lambda t: t + G
    outline_filter(d, 'ol6', 6)
    chroma_filter(d)
    ember_css(d, H)
    d.css.append('.win{opacity:0;visibility:hidden}')
    d.css.append('@media (prefers-reduced-motion:reduce){.win{opacity:0!important;visibility:hidden!important}.gate{opacity:1!important;visibility:visible!important}}')

    def win(t0, t1, extra_from=None):
        """opacity window [t0,t1) in loop seconds; returns style string."""
        e = 0.001
        H_, V_ = 'opacity:0;visibility:hidden', 'opacity:1;visibility:visible'
        fr = [(0, H_), (max(0, t0 - e), H_), (t0, V_), (t1, V_), (min(L, t1 + e), H_), (L, H_)]
        if t0 <= 0:
            fr = [(0, V_), (t1, V_), (t1 + e, H_), (L, H_)]
        return f'animation:{d.timeline(L, fr, "w")} {L}s linear infinite'

    def enter(t0, t1, frm, dur=0.42, ease='cubic-bezier(.2,1.7,.35,1)', to='none'):
        """Element hidden, then animates from `frm` transform to `to` at t0, visible until t1."""
        e = 0.001
        h_, v_ = 'opacity:0;visibility:hidden', 'opacity:1;visibility:visible'
        fr = [(0, f'{h_};transform:{frm}'), (max(0, t0 - e), f'{h_};transform:{frm}'),
              (t0, f'{v_};transform:{frm}', ease), (t0 + dur, f'{v_};transform:{to}'),
              (t1, f'{v_};transform:{to}'), (t1 + e, f'{h_};transform:{to}'), (L, f'{h_};transform:{to}')]
        return f'animation:{d.timeline(L, fr, "e")} {L}s linear infinite'

    def slam(text, x, y, size, rot, t0, t1, anchor='start', maxw=880):
        g, w, h = ransom(d, text, size, bob=0)
        if w > maxw and ' ' in text:  # stack words instead of shrinking them
            parts = [ransom(d, p, size, bob=0) for p in text.split(' ')]
            w = max(p[1] for p in parts)
            al = {'start': 0, 'middle': .5, 'end': 1}[anchor]
            g, yy = '<g>', 0
            for pg, pw, ph in parts:
                g += f'<g transform="translate({(w - pw) * al:.1f},{yy:.1f})">{pg}</g>'
                yy += ph + size * .12
            g += '</g>'
            h = yy
            y -= h / 2 - size / 2
        k = min(1, maxw / w)
        ox = {'start': 0, 'middle': -w * k / 2, 'end': -w * k}[anchor]
        return (f'<g transform="translate({x + ox:.1f},{y:.1f}) rotate({rot} {w * k / 2:.0f} {h * k / 2:.0f}) scale({k:.3f})">'
                f'<g class="c win" filter="url(#ca)" style="{enter(t0, t1, "scale(3.4) rotate(14deg)")}">{g}</g></g>')

    # ---- backgrounds: ink, then lit red world with stripes during montage
    d.add(f'<rect width="{W}" height="{H}" fill="{INK}"/>')
    lit = [(T(3.40), T(13.39)), (T(15.13), L)]
    d.add(f'<g class="win" style="{win(T(3.40), L - 0.01)}"><rect width="{W}" height="{H}" fill="{RED}"/>{stripes(d, W, H, .5)}{dots(d, W, H)}</g>')

    # speed lines (repeating conic gradient)
    wedges = ''.join(f'<polygon points="0,0 {math.cos(math.radians(a)) * 900:.0f},{math.sin(math.radians(a)) * 900:.0f} '
                     f'{math.cos(math.radians(a + 2)) * 900:.0f},{math.sin(math.radians(a + 2)) * 900:.0f}" fill="#fff" fill-opacity=".16"/>'
                     for a in range(0, 360, 9))
    d.add(f'<g class="win" style="{win(T(3.40), L - 0.01)}"><g transform="translate(500,280)"><g style="animation:spin 6s linear infinite">{wedges}</g></g></g>')

    stage = []  # everything that shakes

    # ---- GATE (0 .. G)
    sf, sfa = lummask('sil-front.webp', 500)
    d.defs.append(f'<mask id="sfm"><image href="{sf}" x="{W - 30 - 500 * sfa:.0f}" y="{H - 500}" width="{500 * sfa:.0f}" height="500"/></mask>')
    d.defs.append(f'<linearGradient id="burn" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#ffb000"/><stop offset=".35" stop-color="{RED}"/>'
                  f'<stop offset=".7" stop-color="#3a0003"/><stop offset="1" stop-color="{INK}"/></linearGradient>')
    d.css.append('@keyframes burn{0%{transform:translateY(0)}100%{transform:translateY(-260px)}}')
    gname, gw, gh = ransom(d, 'RYAN PANDA', 92)
    tag = (f'<g transform="translate(500,{150 + gh + 40}) rotate(-6) skewX(-12)">'
           f'<rect x="-95" y="-22" width="190" height="44" fill="{INK}" stroke="#fff" stroke-width="3"/>'
           + d.text(0, 13, 'PORTFOLIO', 'Anton', 26, '#fff', 'middle', .12) + '</g>')
    enter_btn = (f'<g transform="translate(500,{150 + gh + 120}) rotate(-6)">'
                 f'<polygon points="-110,-34 110,-30 102,34 -110,28" fill="#fff" stroke="{INK}" stroke-width="5"/>'
                 f'<g style="animation:blink 1s linear infinite"><polygon points="-110,-34 110,-30 102,34 -110,28" fill="{INK}" stroke="#fff" stroke-width="5"/>'
                 + d.text(0, 12, 'ENTER', 'Anton', 34, '#fff', 'middle', .1) + '</g>'
                 + f'<g style="animation:blink 1s linear -.5s infinite">' + d.text(0, 12, 'ENTER', 'Anton', 34, INK, 'middle', .1) + '</g></g>')
    gate = (f'<g class="win gate" style="{win(0, G)}">'
            f'<g transform="rotate(-8 500 280)"><g style="{enter(0, G, "translateX(-1200px)", .5, "cubic-bezier(.2,1.6,.4,1)")}" class="win">'
            f'<rect x="-100" y="224" width="1200" height="180" fill="{RED}"/>'
            f'<rect x="-70" y="204" width="1200" height="6" fill="#fff"/><rect x="-70" y="418" width="1200" height="6" fill="#fff"/></g></g>'
            f'<g mask="url(#sfm)"><rect x="0" y="0" width="{W}" height="{H + 300}" fill="url(#burn)" style="animation:burn 3s ease-in-out infinite alternate"/></g>'
            f'<g transform="translate({500 - gw / 2:.0f},120) rotate(-6 {gw / 2:.0f} {gh / 2:.0f})">{gname}</g>'
            f'{tag}{enter_btn}'
            + d.text(500, H - 26, 'CLICK  ▸  SCROLL  ▸  PLAY', 'Mono', 12, '#bbb', 'middle', .25) + '</g>')
    stage.append(gate)

    # ---- 0.00 eyes, 1.66 THEY / 2.15 CALL / 2.65 ME
    eyes = cover('eyes.jpg', W, H, (0.5, 0.35), 1.0, 70)
    stage.append(f'<g class="win" style="{win(T(0), T(3.40))}"><image class="c" href="{eyes}" width="{W}" height="{H}" preserveAspectRatio="xMidYMid slice" '
                 f'style="{enter(T(0), T(3.40), "scale(1.8)", 3.2, "ease-out", "scale(1.15)")};filter:contrast(1.3) saturate(1.4)"/></g>')
    stage.append(slam('THEY', 60, 40, 150, -8, T(1.66), T(3.40)))
    stage.append(slam('CALL', 160, 200, 150, 5, T(2.15), T(3.40)))
    stage.append(slam('ME', 940, 340, 190, -4, T(2.65), T(3.40), 'end'))

    # ---- 3.40 AGENCY with front silhouette
    sil_ink, sila = cutout('sil-front.webp', 540, recolor=INK)
    stage.append(f'<g class="win" style="{win(T(3.40), T(5.40))}"><g transform="translate({500 - 270 * sila:.0f},{H - 530})">'
                 f'<image class="c" href="{sil_ink}" width="{540 * sila:.0f}" height="540" filter="url(#ol6)" '
                 f'style="{enter(T(3.40), T(5.40), "translateY(540px) scale(1.3)", .45, "cubic-bezier(.2,1.6,.4,1)")}"/></g></g>')
    stage.append(slam('AGENCY', 500, 180, 210, -6, T(3.40), T(5.40), 'middle'))

    # ---- 5.40 .. 11.39 ID cards
    hero_cut, heroa = cutout('hero.webp', 380)
    cards = [
        (5.40, 6.64, 'UW INFORMATICS', 'STUDENT · SEATTLE', 'left', 'cut', INK),
        (6.64, 7.65, 'MOBILE DEV', 'CRUSYN · 521+ DRIVERS', 'right', ('fav/crusyn_app.webp', (0.5, 0.25)), GOLD),
        (7.65, 8.39, 'FULL-STACK DEV', 'AERO DOCK · 74★', 'left', ('aerodock-previews.jpg', (0.5, 0.5)), '#fff'),
        (8.39, 9.14, 'ML RESEARCHER', 'FIREGUARD AI · TOP 10/900+', 'right', ('fireguard.webp', (0.5, 0.5)), INK),
        (9.14, 9.89, 'UI/UX DESIGNER', 'COUCHTOP', 'left', ('couchtop.jpg', (0.5, 0.5)), GOLD),
        (9.89, 11.39, 'HACKATHON CHAMP', '51 HACKATHONS · 6 WINS', 'right', ('hack/artemis.webp', (0.5, 0.5)), INK),
    ]
    PW, PH, PY = 640, 358, 56
    for t0, t1, title, sub, side, img, barc in cards:
        a, b = T(t0), T(t1)
        px = -20 if side == 'left' else W - PW + 20
        poly = ('0,0 1,.08 .88,1 0,1' if side == 'left' else '0,.08 1,0 1,1 .12,1')
        pts = ' '.join(f'{float(p.split(",")[0]) * PW:.0f},{float(p.split(",")[1]) * PH:.0f}' for p in poly.split())
        cid = f'cp{int(t0 * 100)}'
        d.defs.append(f'<clipPath id="{cid}"><polygon points="{pts}"/></clipPath>')
        frm = 'translateX(-1200px) skewX(20deg)' if side == 'left' else 'translateX(1200px) skewX(-20deg)'
        if img == 'cut':
            plate = (f'<image href="{hero_cut}" x="{PW / 2 - 190 * heroa:.0f}" y="{PH - 380}" width="{380 * heroa:.0f}" height="380" filter="url(#ol6)"/>')
        else:
            src, pos = img
            imgs = [src] + (['hack/clixel.webp', 'hack/teenthrive.webp', 'hack/artemis.webp'] if title == 'HACKATHON CHAMP' else [])
            swaps = [t0, 10.39, 10.65, 10.89] if len(imgs) > 1 else [t0]
            layers = ''
            for i, s in enumerate(imgs):
                st = win(T(swaps[i]), T(swaps[i + 1]) if i + 1 < len(swaps) else b)
                layers += f'<image class="win" href="{cover(s, PW, PH, pos, 1.0, 66)}" width="{PW}" height="{PH}" style="{st}"/>'
            plate = (f'<polygon points="{pts}" fill="#000" transform="translate(16,16)"/>'
                     f'<g clip-path="url(#{cid})"><rect width="{PW}" height="{PH}" fill="#000"/>{layers}</g>'
                     f'<polygon points="{pts}" fill="none" stroke="#fff" stroke-width="6"/>')
            plate = f'<polygon points="{pts}" fill="{INK}" transform="translate(16,16)"/>' + plate
        bar = (f'<g transform="rotate(-7 500 437)"><rect class="win" x="-100" y="364" width="1200" height="146" fill="{barc}" '
               f'style="{enter(a, b, "translateX(1200px) skewX(-20deg)", .28)}"/></g>')
        subw = measure(sub, 'Anton', 26, .12) + 32
        sx = (W * 0.96 - subw) if side == 'left' else W * 0.04
        subg = (f'<g transform="translate({sx:.0f},84) rotate(-7) skewX(-12)"><g class="win" style="{enter(a + .12, b, "translateX(1200px)", .3)}">'
                f'<rect width="{subw:.0f}" height="42" fill="{INK}"/>' + d.text(16, 32, sub, 'Anton', 26, GOLD, 'start', .12) + '</g></g>')
        stage.append(f'<g class="win" style="{win(a, b)}"><g transform="translate({px},{PY})"><g class="win" style="{enter(a, b, frm, .34, "cubic-bezier(.2,1.6,.4,1)")}">{plate}</g></g>'
                     f'{bar}{subg}</g>')
        tx = W * 0.96 if side == 'left' else W * 0.04
        stage.append(slam(title, tx, 350, 84, -7, a, b, 'end' if side == 'left' else 'start', 600))

    # ---- 11.39 RYAN / PANDA with side silhouette -> 12.89 swap to side photo, 14.14 READY?
    sil_side, ssa = cutout('sil-side.webp', 540, recolor=INK)
    side_img, _ = cutout('side.webp', 540)
    for href, t0, t1 in ((sil_side, 11.39, 12.89), (side_img, 12.89, 15.13)):
        stage.append(f'<g class="win" style="{win(T(t0), T(t1))}"><g transform="translate({500 - 270 * ssa:.0f},{H - 530})">'
                     f'<image class="c" href="{href}" width="{540 * ssa:.0f}" height="540" filter="url(#ol6)" '
                     f'style="{enter(T(t0), T(t1), "translateY(540px) scale(1.3)" if t0 == 11.39 else "scale(1.06)", .45 if t0 == 11.39 else .2, "cubic-bezier(.2,1.6,.4,1)")}"/></g></g>')
    stage.append(slam('RYAN', 40, 60, 200, -8, T(11.39), T(14.14)))
    stage.append(slam('PANDA', 970, 300, 200, -5, T(12.39), T(14.14), 'end'))
    stage.append(slam('READY?', 500, 200, 170, -4, T(14.14), T(15.13), 'middle'))

    # ---- 15.13 DROP: hero + LET'S GO!
    hero_big, hba = cutout('hero.webp', 540)
    stage.append(f'<g class="win" style="{win(T(15.13), L)}"><g transform="translate({500 - 270 * hba:.0f},{H - 520})">'
                 f'<image class="c" href="{hero_big}" width="{540 * hba:.0f}" height="540" filter="url(#ol6)" '
                 f'style="{enter(T(15.13), L, "translateY(540px) scale(1.3)", .45, "cubic-bezier(.2,1.6,.4,1)")}"/></g></g>')
    stage.append(slam("LET'S GO!", 500, 30, 160, -5, T(15.13), L, 'middle'))

    # ---- stage shake + zoom pulse on cues
    hits = [1.66, 2.15, 2.65, 3.40, 5.40, 6.64, 7.65, 8.39, 9.14, 9.89, 10.39, 10.65, 10.89, 11.39, 12.39, 15.13, 15.39, 15.65, 15.89]
    hits += [13.39 + i * 0.25 for i in range(7)]
    fr = [(0, 'transform:none')]
    for h in sorted(hits):
        t = T(h)
        s = 22 if h in (3.40, 15.13) else 10
        fr += [(t - .001, 'transform:none'), (t + .04, f'transform:translate({s}px,{-s}px) rotate(1deg)'),
               (t + .09, f'transform:translate({-s}px,{s}px) rotate(-1deg)'), (t + .16, 'transform:none')]
    fr.append((L, 'transform:none'))
    shake = d.timeline(L, fr, 'sh')
    d.add(f'<g class="c" style="animation:{shake} {L}s linear infinite">{"".join(stage)}</g>')

    d.add(embers(W, H, 26, drops=10))

    # ---- flashes
    fl = [(0, 'opacity:0')]
    flashes = [(G - .3, .9, .3), (T(0.38), .35, .3)] + [(T(h), .85 if h in (3.40, 15.13) else .35, .22) for h in hits] + [(L - .5, 1, .5)]
    for t, o, dd in sorted(flashes):
        fr_t = max(fl[-1][0] + .002, t)
        fl += [(fr_t - .001, 'opacity:0'), (fr_t, f'opacity:{o}'), (min(L, fr_t + dd), 'opacity:0')]
    fl.append((L, 'opacity:0'))
    d.add(f'<rect width="{W}" height="{H}" fill="#fff" opacity="0" style="animation:{d.timeline(L, fl, "fl")} {L}s linear infinite"/>')

    # ---- end shatter shards
    rng = random.Random(16)
    cols = ['#fff', RED, INK, GOLD]
    for i in range(16):
        cx, cy = rng.uniform(0, W), rng.uniform(0, H)
        p = f'{cx:.0f},{cy:.0f} {cx + rng.uniform(200, 500):.0f},{cy + rng.uniform(-80, 80):.0f} {cx + rng.uniform(-150, 150):.0f},{cy + rng.uniform(110, 280):.0f}'
        a = rng.uniform(0, math.tau)
        dist = rng.uniform(600, 1000)
        t0 = L - 0.75
        fr = [(0, 'opacity:0;visibility:hidden;transform:none'), (t0 - .001, 'opacity:0;visibility:hidden;transform:none'), (t0, 'opacity:1;visibility:visible;transform:none', 'cubic-bezier(.3,.8,.4,1)'),
              (L - .02, f'opacity:0;transform:translate({math.cos(a) * dist:.0f}px,{math.sin(a) * dist:.0f}px) rotate({rng.uniform(-360, 360):.0f}deg) scale(.4)'), (L, 'opacity:0')]
        d.add(f'<polygon class="c win" points="{p}" fill="{cols[i % 4]}" style="animation:{d.timeline(L, fr, "sd")} {L}s linear infinite"/>')

    d.add(crt(d, W, H))
    d.save('intro.svg')


# =====================================================================
# 2. MENU: Persona-style main menu with the hero, burst, bars, HUD
# =====================================================================
def menu():
    H = 640
    d = Doc(W, H, 'Ryan Panda, codename Agency. Main menu: Work, Experience, Skills, Profile, Contact.')
    outline_filter(d, 'ol', 5)
    ember_css(d, H)
    d.add(f'<rect width="{W}" height="{H}" fill="{RED}"/>' + stripes(d, W, H, .5) + dots(d, W, H))

    # spectrum starburst behind hero
    hx, hy, R0 = 790, 250, 205
    rng = random.Random(5)
    n = 48
    def burst(r_in, r_out, var, off=0):
        pts = []
        for i in range(n * 2):
            a = off + i / (n * 2) * math.tau
            r = r_in if i % 2 else r_out + rng.uniform(0, var)
            pts.append(f'{math.cos(a) * r:.0f},{math.sin(a) * r:.0f}')
        return ' '.join(pts)
    d.add(f'<g transform="translate({hx},{hy})"><g class="c" style="animation:beat .5s ease-out infinite">'
          f'<g style="animation:spin 40s linear infinite"><polygon points="{burst(R0 * .92, R0 * 1.05, R0 * 1.0)}" fill="#fff"/></g>'
          f'<g style="animation:spinr 55s linear infinite"><polygon points="{burst(R0 * .8, R0 * .95, R0 * .8, .03)}" fill="{INK}"/></g>'
          f'<circle r="{R0 * .62:.0f}" fill="none" stroke="{RED}" stroke-width="10"/></g></g>')

    # hero: glow, shadow, art with white outline, breathing + beat bounce
    HH = 560
    sm, sa = lummask('sil-front.webp', HH)
    hw = HH * sa
    hx0 = W - 30 - hw
    d.defs.append(f'<mask id="hm"><image href="{sm}" x="{hx0:.0f}" y="{H - HH}" width="{hw:.0f}" height="{HH}"/></mask>'
                  f'<linearGradient id="hg" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#ffd24a"/><stop offset=".6" stop-color="{RED}"/><stop offset="1" stop-color="{RED}" stop-opacity="0"/></linearGradient>')
    art, _ = cutout('hero.webp', HH)
    d.css.append('@keyframes glowp{0%{opacity:1}40%{opacity:.4}100%{opacity:.4}}')
    d.css.append('@keyframes heroIn{from{transform:translateX(70%) rotate(8deg)}}')
    d.add(f'<g class="bb" style="animation:heroIn .55s cubic-bezier(.2,1.6,.4,1) both">'
          f'<g class="bb" style="animation:beat .5s ease-out infinite">'
          f'<g transform="translate({hx0 + hw / 2:.0f},{H}) scale(1.05) translate({-hx0 - hw / 2:.0f},{-H})"><rect width="{W}" height="{H}" fill="url(#hg)" mask="url(#hm)" style="animation:glowp .5s ease-out infinite"/></g>'
          f'<g transform="translate(24,14)"><rect width="{W}" height="{H}" fill="{INK}" mask="url(#hm)"/></g>'
          f'<image href="{art}" x="{hx0:.0f}" y="{H - HH}" width="{hw:.0f}" height="{HH}" filter="url(#ol)" style="animation:breathe 3.2s ease-in-out infinite"/></g></g>')

    # sparks bursting from hero on the beat
    sp = []
    for i in range(12):
        a = rng.uniform(0, math.tau)
        dist = rng.uniform(140, 300)
        name = d.kf(f'0%{{transform:translate(0,0) scale(0) rotate(0);opacity:1}}60%{{opacity:1}}100%{{transform:translate({math.cos(a) * dist:.0f}px,{math.sin(a) * dist:.0f}px) scale({rng.uniform(.6, 1.6):.1f}) rotate(220deg);opacity:0}}', 'sp')
        sp.append(f'<g style="animation:{name} {rng.choice([1, 1.5, 2])}s cubic-bezier(.2,.9,.3,1) {-rng.uniform(0, 2):.2f}s infinite" class="c">{star(hx, hy - 30, 30, "#fff" if i % 3 == 0 else GOLD)}</g>')
    d.add(''.join(sp))

    # name + codename
    nm, nw, nh = ransom(d, 'RYAN PANDA', 62)
    d.add(f'<g transform="translate(40,34) rotate(-5)">{nm}</g>')
    d.add(f'<g transform="translate(46,{34 + nh + 26}) rotate(-5) skewX(-12)"><rect width="250" height="30" fill="{INK}"/><rect width="6" height="30" fill="{GOLD}"/>'
          + d.text(18, 23, 'CODENAME: AGENCY', 'Anton', 18, '#fff', 'start', .3) + '</g>')

    # menu list with cycling selection (each item highlighted for 1.5s)
    items = ['WORK', 'EXPERIENCE', 'SKILLS', 'PROFILE', 'CONTACT']
    L, per = 7.5, 1.5
    jag = '0,.18 .08,0 .62,.1 1,0 .94,.52 1,1 .40,.88 .06,1'
    out = ['<g transform="translate(64,250) rotate(-9)">']
    for i, it in enumerate(items):
        fs = 60
        y = i * 62
        x = i * 26
        tw = measure(it, 'Anton', fs, .02)
        bx, by, bw, bh = x - .10 * tw, y - fs * .95, tw * 1.24, fs * 1.02
        pts = lambda ox, oy, w_, h_: ' '.join(f'{ox + float(p.split(",")[0]) * w_:.0f},{oy + float(p.split(",")[1]) * h_:.0f}' for p in jag.split())
        a0, a1 = i * per / L * 100, (i + 1) * per / L * 100
        e = .05
        plate = d.kf(f'0%{{transform:scaleX(0)}}{max(0, a0 - e):.2f}%{{transform:scaleX(0)}}{a0 + 1.6:.2f}%{{transform:scaleX(1)}}{a1 - e:.2f}%{{transform:scaleX(1)}}{a1:.2f}%{{transform:scaleX(0)}}100%{{transform:scaleX(0)}}', 'pl')
        col = d.kf(f'0%{{fill:#fff}}{max(0, a0 - e):.2f}%{{fill:#fff}}{a0:.2f}%{{fill:{RED}}}{a1 - e:.2f}%{{fill:{RED}}}{a1:.2f}%{{fill:#fff}}100%{{fill:#fff}}', 'cl')
        shd = d.kf(f'0%{{opacity:1}}{max(0, a0 - e):.2f}%{{opacity:1}}{a0:.2f}%{{opacity:0}}{a1 - e:.2f}%{{opacity:0}}{a1:.2f}%{{opacity:1}}100%{{opacity:1}}', 'sh')
        wob = d.kf(f'0%,{max(0, a0 - e):.2f}%,{a1:.2f}%,100%{{transform:none}}{a0 + (a1 - a0) * .25:.2f}%{{transform:rotate(-2deg)}}{a0 + (a1 - a0) * .5:.2f}%{{transform:rotate(2deg) scale(1.05)}}{a0 + (a1 - a0) * .75:.2f}%{{transform:rotate(-2deg)}}', 'wb')
        stagger = f'animation:miIn .4s cubic-bezier(.2,1.6,.4,1) {.06 + i * .06:.2f}s both'
        out.append(f'<g style="{stagger}">'
                   f'<polygon class="bl" points="{pts(bx + .06 * tw, by + .16 * fs, bw * 1.04, bh)}" fill="{INK}" style="animation:{plate} {L}s steps(3,end) infinite"/>'
                   f'<polygon class="bl" points="{pts(bx, by, bw, bh)}" fill="#fff" style="animation:{plate} {L}s steps(3,end) infinite"/>'
                   f'<g class="c" style="animation:{wob} {L}s linear infinite">'
                   f'<g style="animation:{shd} {L}s linear infinite">' + d.text(x + 6, y + 6, it, 'Anton', fs, INK, 'start', .02) + '</g>'
                   + d.text(x, y, it, 'Anton', fs, '#fff', 'start', .02, f'style="animation:{col} {L}s linear infinite"') + '</g></g>')
    out.append('</g>')
    d.css.append('@keyframes miIn{from{transform:translateX(-700px) skewX(30deg)}}')
    d.add(''.join(out))

    # HUD: combo counter that ticks on every beat + XP bar
    hud = [f'<g transform="translate(968,40) rotate(4)">' + d.text(0, 0, 'COMBO', 'Anton', 14, GOLD, 'end', .2)]
    N = 32
    for i in range(N):
        a0, a1 = i / N * 100, (i + 1) / N * 100
        k = d.kf(f'0%{{opacity:0}}{a0:.3f}%{{opacity:1;transform:scale(1.7) rotate(-10deg)}}{a0 + 1.3:.3f}%{{transform:scale(1)}}{a1:.3f}%{{opacity:1}}{a1 + .001:.3f}%{{opacity:0}}100%{{opacity:0}}', 'cb')
        hud.append(f'<g class="c" style="opacity:0;animation:{k} {N * .5}s linear infinite">' + d.text(0, 48, str(i + 1), 'Anton', 48, GOLD if i % 4 == 3 else '#fff', 'end', 0, f'stroke="{INK}" stroke-width="2" paint-order="stroke"') + '</g>')
    hud.append('</g>')
    d.css.append(f'@keyframes xp{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}')
    hud.append(f'<g transform="translate(846,104) skewX(-14)"><rect width="120" height="12" fill="{INK}" stroke="#fff" stroke-width="3"/>'
               f'<rect class="bl" x="1.5" y="1.5" width="117" height="9" fill="{GOLD}" style="animation:xp {N * .5}s linear infinite"/></g>')
    d.add(''.join(hud))

    # now playing
    np1, np2 = '♫ NOW PLAYING', 'THEY CALL ME AGENCY'
    d.add(f'<g transform="translate(44,{H - 176})">' + skewbox(0, 0, measure(np1, 'Anton', 15, .08) + 24, 26, -12, GOLD, '#fff', 3)
          + d.text(12, 19, np1, 'Anton', 15, INK, 'start', .08) + skewbox(0, 34, measure(np2, 'Anton', 15, .08) + 24, 26, -12, INK, '#fff', 3)
          + d.text(12, 53, np2, 'Anton', 15, '#fff', 'start', .08) + '</g>')

    d.add(embers(W, H, 40, drops=14))
    d.add(f'<rect y="{H - 150}" width="{W}" height="150" fill="url(#bglow)"/>')
    d.defs.append(f'<linearGradient id="bglow" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{RED}" stop-opacity="0"/><stop offset="1" stop-color="#ff6e14" stop-opacity=".55"/></linearGradient>')
    d.add(bars(d, W, H, 80))
    # oscilloscope ribbon
    pts = ' '.join(f'{x},{H - 130 + math.sin(x / 14) * 14 * math.sin(x / 140):.1f}' for x in range(0, W + 1, 8))
    d.css.append('@keyframes scope{to{transform:translateX(-176px)}}')
    pts2 = ' '.join(f'{x},{H - 104 + math.sin(x / 14) * 12:.1f}' for x in range(0, W + 200, 4))
    d.add(f'<g style="animation:scope 1s linear infinite"><polyline points="{pts2}" transform="translate(3,3)" fill="none" stroke="{INK}" stroke-opacity=".8" stroke-width="3"/>'
          f'<polyline points="{pts2}" fill="none" stroke="#fff" stroke-width="3"/></g>')
    d.add(crt(d, W, H))
    d.save('menu.svg')


# =====================================================================
# 3. Section title banners
# =====================================================================
def title_banner(word, sub, fname):
    H = 190
    d = Doc(W, H, word)
    d.add(panel_bg(d, W, H))
    d.css.append('@keyframes wipe{from{clip-path:polygon(100% 0,100% 0,100% 100%,100% 100%)}to{clip-path:polygon(0 0,100% 0,100% 100%,0 100%)}}')
    g, w, h = ransom(d, word, 100, bob=10)
    d.add(f'<g style="animation:wipe .3s steps(5,end) both"><g transform="translate(46,{H / 2 - h / 2 + 6:.0f}) rotate(-5 {w / 2:.0f} {h / 2:.0f})">{g}</g></g>')
    # kicker
    kw = measure(sub, 'Anton', 22, .2) + 36
    d.add(f'<g transform="translate({min(W - kw - 30, 90 + w):.0f},{H / 2 + 20:.0f}) skewX(-12)" style="animation:slidein .4s .2s cubic-bezier(.2,1.6,.4,1) both">'
          f'<rect width="{kw:.0f}" height="38" fill="{RED}"/>' + d.text(18, 29, sub, 'Anton', 22, '#fff', 'start', .2) + '</g>')
    d.css.append('@keyframes slidein{from{transform:translateX(1100px) skewX(-12deg)}}')
    # gold arcana star spinning at right
    d.add(f'<g transform="translate({W - 70},{H / 2})"><g style="animation:spin 6s linear infinite">{star(0, 0, 70, GOLD)}</g></g>')
    d.add(crt(d, W, H))
    d.save(fname)


# =====================================================================
# 4. WORK cards (one SVG each so every card links somewhere)
# =====================================================================
WORK = [
    ('AERO DOCK', '74★ · XDA', 'aerodock-previews.jpg', (0.5, 0.5), 'https://github.com/TheAgencyMGE/aero-dock'),
    ('CRUSYN', '521+ DRIVERS', 'fav/crusyn_app.webp', (0.5, 0.2), 'https://www.crusyn.app'),
    ('COUCHTOP', '28★', 'couchtop.jpg', (0.5, 0.5), 'https://github.com/TheAgencyMGE/couchtop'),
    ('PC RECAP', '19★', 'pcrecap.jpg', (0.5, 0.5), 'https://pcrecap.online'),
    ('FIREGUARD AI', 'TOP 10 / 900+', 'fireguard.webp', (0.5, 0.5), 'https://github.com/TheAgencyMGE/FireGuard-AI'),
    ('NEXTUP PNW', 'SEATTLE OPPS', 'nextup.webp', (0.5, 0.5), 'https://github.com/TheAgencyMGE/nextup-pnw'),
]


def work_card(i, title, stat, img, pos):
    CW, SH, MH = 440, 262, 70
    VW, VH = 500, 380
    d = Doc(VW, VH, f'{title}: {stat}')
    rot = -1.5 if i % 2 == 0 else 1.5
    sh = RED if i % 2 == 0 else GOLD
    ch = SH + MH + 5
    shot = cover(img, CW - 10, SH, pos, 1.6, 76)
    d.defs.append(f'<clipPath id="sc"><rect x="5" y="5" width="{CW - 10}" height="{SH}"/></clipPath>')
    d.css.append(f'@keyframes pop{{0%{{transform:scale(0) rotate(-25deg)}}100%{{transform:none}}}}')
    sw = measure(stat, 'Anton', 17) + 22
    body = (f'<rect x="12" y="12" width="{CW}" height="{ch}" fill="{sh}"/>'
            f'<rect width="{CW}" height="{ch}" fill="{PAPER}" stroke="{INK}" stroke-width="10"/>'
            f'<g clip-path="url(#sc)"><image href="{shot}" x="5" y="5" width="{CW - 10}" height="{SH}" style="filter:contrast(1.08) saturate(1.1)"/>'
            f'<rect x="0" y="0" width="120" height="{SH + 10}" fill="#fff" opacity=".35" style="animation:glint 5s ease-in-out {i * .7:.1f}s infinite"/></g>'
            f'<rect x="0" y="{SH + 5}" width="{CW}" height="5" fill="{INK}"/>'
            + d.text(18, SH + 55, title, 'Anton', 34, INK)
            + f'<g transform="translate({CW - sw - 16:.0f},{SH + 22})">' + skewbox(0, 0, sw, 30, -10, INK) + d.text(sw / 2, 22, stat, 'Anton', 17, GOLD, 'middle') + '</g>')
    d.add(f'<g transform="translate({(VW - CW) / 2 - 6:.0f},{(VH - ch) / 2 - 6:.0f}) rotate({rot} {CW / 2} {ch / 2})">'
          f'<g class="c" style="animation:pop .5s cubic-bezier(.2,1.8,.4,1) {.06 + i * .07:.2f}s both">'
          f'<g style="animation:shake {3.2 + i * .37:.2f}s steps(1) {i * .5:.1f}s infinite">{body}</g></g></g>')
    d.save(f'work-{i + 1}.svg')


def chips():
    data = [('30 REPOS', False), ('24 DEVPOST PROJECTS', True), ('51 HACKATHONS', False), ('$2,000+ WON', True)]
    for i, (txt, dark) in enumerate(data):
        tw = measure(txt, 'Anton', 22, .06)
        w, h = tw + 60, 64
        d = Doc(int(w), h, txt)
        bg, fg, bd, sh = (INK, GOLD, GOLD, GOLD) if dark else ('#fff', INK, INK, RED)
        d.css.append('@keyframes popi{from{transform:scale(0)}}')
        d.add(f'<g class="c" style="animation:popi .35s cubic-bezier(.2,1.8,.4,1) {.1 + i * .08:.2f}s both">'
              + skewbox(14, 8, tw + 32, 40, -12, bg, bd, 3, sh, 6, 6)
              + d.text(30, 37, txt, 'Anton', 22, fg, 'start', .06) + '</g>')
        d.save(f'chip-{i + 1}.svg')


# =====================================================================
# 5. EXPERIENCE: confidant rows + trophies
# =====================================================================
def experience():
    rows = [('VII', 'CHARIOT', 'SDE INTERN', 'REMIT2ANY', "DEC '25 – MAR '26"),
            ('IV', 'EMPEROR', 'CO-PRESIDENT & BOARD', 'LUMA CODING', "JAN – DEC '25"),
            ('V', 'HIEROPHANT', 'AI & CODING INSTRUCTOR', 'CODING MIND ACADEMY', "AUG '25 – NOW"),
            ('II', 'PRIESTESS', 'INSTRUCTOR', 'iCODE REDMOND', "JUN '26 – NOW")]
    trophies = ['1ST · HACKABYTE CA', '2ND · RECESSHACKS 5.0', 'TOP 10 / 900+ · FUSIONHACKS 2',
                'BEST IN TRACK · STELLARNET', '3RD · WA STATE TSA', 'XDA FEATURE · AERO DOCK']
    H = 760
    d = Doc(W, H, 'Experience and trophies')
    d.add(panel_bg(d, W, H))
    g, w, h = ransom(d, 'EXPERIENCE', 88, bob=6)
    d.add(f'<g transform="translate(40,40) rotate(-5 {w / 2:.0f} {h / 2:.0f})">{g}</g>')
    d.css.append('@keyframes slide{from{transform:translateX(-1300px)}}')
    y0 = 170
    for i, (num, arc, role, org, when) in enumerate(rows):
        y = y0 + i * 104
        sh = RED if i % 2 == 0 else GOLD
        rw = 900
        ww = measure(when, 'Anton', 17) + 20
        row = (skewbox(0, 0, rw, 92, -8, INK, '#fff', 4, sh, 9, 9)
               + f'<g transform="translate(18,7)"><rect width="52" height="78" fill="#111" stroke="{GOLD}" stroke-width="3"/>'
               + d.text(26, 17, num, 'Anton', 13, GOLD, 'middle', .05)
               + f'<g transform="translate(26,39)"><g style="animation:spin {4 + i}s linear infinite">{star(0, 0, 24, RED)}</g></g>'
               + d.text(26, 72, arc, 'Anton', 8, GOLD, 'middle', .08) + '</g>'
               + d.text(92, 44, role, 'Anton', 30, '#fff')
               + d.text(92, 73, org, 'Anton', 18, GOLD, 'start', .06)
               + f'<rect x="{rw - ww - 26:.0f}" y="32" width="{ww:.0f}" height="28" fill="#fff"/>'
               + d.text(rw - 26 - ww / 2, 53, when, 'Anton', 17, INK, 'middle'))
        d.add(f'<g transform="translate(46,{y})"><g style="animation:slide .35s cubic-bezier(.2,1.6,.4,1) {.15 + i * .08:.2f}s both">{row}</g></g>')
    ky = y0 + 4 * 104 + 18
    d.add(f'<g transform="translate(46,{ky})">' + skewbox(0, 0, 150, 34, -12, RED) + d.text(75, 26, 'TROPHIES', 'Anton', 22, '#fff', 'middle', .2) + '</g>')
    tw, th = 290, 54
    for i, t in enumerate(trophies):
        x = 46 + (i % 3) * (tw + 14)
        y = ky + 56 + (i // 3) * (th + 16)
        fs = 18 if measure(t, 'Anton', 18) < tw - 70 else 15.5
        d.add(f'<g transform="translate({x},{y})"><g style="animation:slide .35s cubic-bezier(.2,1.6,.4,1) {.5 + i * .07:.2f}s both">'
              + skewbox(0, 0, tw, th, -10, GOLD, INK, 3, INK, 6, 6)
              + f'<g transform="translate(30,{th / 2})"><g style="animation:beat 1s ease-out {i * .17:.2f}s infinite" class="c">{star(0, 0, 30, INK)}</g></g>'
              + d.text(56, th / 2 + fs * .38, t, 'Anton', fs, INK) + '</g></g>')
    d.add(crt(d, W, H))
    d.save('experience.svg')


# =====================================================================
# 6. SKILLS: animated radar + inventory
# =====================================================================
def skills():
    AX = [('ENGINEERING', .95, 'LV MAX'), ('DESIGN', .82, 'LV 4'), ('AI / ML', .76, 'LV 4'), ('LEADERSHIP', .86, 'LV 4'), ('GROWTH', .8, 'LV 4')]
    INV = [('CODE', ['PYTHON', 'TYPESCRIPT', 'JAVASCRIPT', 'RUST', 'C#', 'JAVA', 'DART', 'SQL']),
           ('BUILD', ['REACT', 'REACT NATIVE', 'TAURI', 'ELECTRON', 'FLUTTER', 'ANGULAR', 'NODE.JS', 'WPF', 'FIREBASE', 'SQLITE']),
           ('AI / DATA', ['SCIKIT-LEARN', 'PANDAS', 'TENSORFLOW', 'HUGGING FACE', 'LLM APIS']),
           ('DESIGN & CRAFT', ['FIGMA', 'PHOTOSHOP', 'ILLUSTRATOR', 'GIT', 'GITHUB ACTIONS']),
           ('SPEAKS', ['ENGLISH', 'BENGALI', 'SPANISH'])]
    H = 700
    d = Doc(W, H, 'Skills: radar stats and inventory')
    d.add(panel_bg(d, W, H))
    g, w, h = ransom(d, 'SKILLS', 96, bob=6)
    d.add(f'<g transform="translate(40,36) rotate(-5 {w / 2:.0f} {h / 2:.0f})">{g}</g>')
    # radar
    RR = 140
    cx, cy = 240, 400
    out = [f'<g transform="translate({cx},{cy}) rotate(-4)">']
    for ring in range(1, 5):
        pts = ' '.join(f'{math.cos(-math.pi / 2 + i * math.tau / 5) * RR * ring / 4:.1f},{math.sin(-math.pi / 2 + i * math.tau / 5) * RR * ring / 4:.1f}' for i in range(5))
        out.append(f'<polygon points="{pts}" fill="{INK if ring == 4 else "none"}" stroke="{"#fff" if ring == 4 else "rgba(255,255,255,.35)"}" stroke-width="{5 if ring == 4 else 2}"/>')
    for i, (lab, v, lv) in enumerate(AX):
        a = -math.pi / 2 + i * math.tau / 5
        x, y = math.cos(a) * (RR + 28), math.sin(a) * (RR + 28)
        anc = 'middle' if abs(x) < 10 else ('start' if x > 0 else 'end')
        out.append(f'<line x1="0" y1="0" x2="{math.cos(a) * RR:.1f}" y2="{math.sin(a) * RR:.1f}" stroke="rgba(255,255,255,.35)" stroke-width="2"/>')
        out.append(d.text(x, y + 4, lab, 'Anton', 16, '#fff', anc, .06) + d.text(x, y + 22, lv, 'Anton', 13, GOLD, anc, .06))
    pts = ' '.join(f'{math.cos(-math.pi / 2 + i * math.tau / 5) * RR * v:.1f},{math.sin(-math.pi / 2 + i * math.tau / 5) * RR * v:.1f}' for i, (_, v, _) in enumerate(AX))
    d.css.append('@keyframes radar{0%{transform:scale(0)}60%{transform:scale(1.12)}80%{transform:scale(.96)}100%{transform:scale(1)}}')
    d.css.append('@keyframes rpulse{0%{transform:scale(1.05)}30%,100%{transform:scale(1)}}')
    out.append(f'<g style="animation:radar .8s cubic-bezier(.2,1.2,.4,1) .2s both"><g style="animation:rpulse .5s ease-out 1s infinite">'
               f'<polygon points="{pts}" fill="rgba(232,41,28,.85)" stroke="#fff" stroke-width="4" stroke-linejoin="round"/>'
               + ''.join(f'<circle cx="{math.cos(-math.pi / 2 + i * math.tau / 5) * RR * v:.1f}" cy="{math.sin(-math.pi / 2 + i * math.tau / 5) * RR * v:.1f}" r="6" fill="{GOLD}" stroke="{INK}" stroke-width="2"/>' for i, (_, v, _) in enumerate(AX))
               + '</g></g></g>')
    d.add(''.join(out))
    # inventory
    x0, y = 500, 160
    k = 0
    d.css.append('@keyframes popi{from{transform:scale(0)}}')
    for head, items in INV:
        d.add(d.text(x0, y, head, 'Anton', 20, GOLD, 'start', .16))
        y += 14
        x = x0
        for it in items:
            iw = measure(it, 'Anton', 17) + 26
            if x + iw > W - 30:
                x, y = x0, y + 44
            n = k + 1
            bg, fg, shc = ('#fff', INK, RED)
            if n % 3 == 0:
                bg, fg, shc = RED, '#fff', INK
            if n % 4 == 0:
                bg, fg, shc = GOLD, INK, RED
            d.add(f'<g class="c" style="animation:popi .35s cubic-bezier(.2,1.8,.4,1) {.3 + k * .025:.3f}s both">'
                  + skewbox(x, y, iw, 32, -10, bg, INK, 3, shc, 4, 4) + d.text(x + iw / 2, y + 23, it, 'Anton', 17, fg, 'middle') + '</g>')
            x += iw + 12
            k += 1
        y += 74
    d.add(crt(d, W, H))
    d.save('skills.svg')


# =====================================================================
# 7. PROFILE: ID box + favourites
# =====================================================================
def profile():
    H = 690
    d = Doc(W, H, 'Profile: Ryan Panda, codename Agency, UW Informatics 2030, Seattle WA')
    d.add(panel_bg(d, W, H))
    g, w, h = ransom(d, 'PROFILE', 96, bob=6)
    d.add(f'<g transform="translate(40,36) rotate(-5 {w / 2:.0f} {h / 2:.0f})">{g}</g>')
    # id box
    BW, BH = 430, 470
    side, sa = cutout('side.webp', BH * 1.12)
    d.defs.append(f'<clipPath id="idc"><rect width="{BW}" height="{BH}"/></clipPath>')
    rows = [('NAME', 'RYAN PANDA'), ('CODENAME', 'AGENCY'), ('CLASS', "UW INFORMATICS '30"), ('BASE', 'SEATTLE, WA'), ('SPEAKS', 'ENGLISH · BENGALI · SPANISH')]
    body = [f'<rect x="14" y="14" width="{BW}" height="{BH}" fill="{RED}"/><rect width="{BW}" height="{BH}" fill="{PAPER}"/>'
            f'<g clip-path="url(#idc)"><image href="{side}" x="{BW - BH * 1.12 * sa * .78:.0f}" y="{BH - BH * 1.12 + 30:.0f}" width="{BH * 1.12 * sa:.0f}" height="{BH * 1.12:.0f}" opacity=".95" style="animation:breathe 3.2s ease-in-out infinite"/></g>'
            f'<rect width="{BW}" height="{BH}" fill="none" stroke="{INK}" stroke-width="10"/>']
    yy = 46
    for lab, val in rows:
        fs = 26 if measure(val, 'Anton', 26) < 250 else 18
        body.append(d.text(22, yy, lab, 'Anton', 13, RED, 'start', .2) + d.text(22, yy + fs + 2, val, 'Anton', fs, INK))
        yy += fs + 40
    q = '"I WATCH ANIME AND GAME. OH I CODE TOO."'
    body.append(f'<g transform="translate(22,{yy})"><polygon points="0,0 270,4 262,74 10,68" fill="{INK}"/>'
                + d.text(16, 30, '"I WATCH ANIME AND GAME.', 'Anton', 18, '#fff') + d.text(16, 56, 'OH I CODE TOO."', 'Anton', 18, GOLD) + '</g>')
    d.css.append('@keyframes popr{0%{transform:scale(0) rotate(-25deg)}}')
    d.add(f'<g transform="translate(44,170) rotate(-2 {BW / 2} {BH / 2})"><g class="c" style="animation:popr .5s cubic-bezier(.2,1.8,.4,1) .1s both">{"".join(body)}</g></g>')
    # favourites
    favs = [('FAV GAME', 'DESTINY 2', 'fav/destiny.webp', (0.5, 0.5), GOLD), ('FAV SHOW', 'ATTACK ON TITAN', 'fav/aot.webp', (0.5, 0.35), RED),
            ('FAV MOVIE', 'PACIFIC RIM', 'fav/pacificrim.webp', (0.5, 0.3), GOLD)]
    FW, FH = 430, 140
    d.defs.append(f'<linearGradient id="fg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{INK}" stop-opacity=".85"/><stop offset=".6" stop-color="{INK}" stop-opacity="0"/></linearGradient>')
    d.css.append('@keyframes favIn{from{transform:translateX(900px)}}')
    for i, (small, big, img, pos, shc) in enumerate(favs):
        x, y = 520 + i * 18, 170 + i * 166
        im = cover(img, FW, FH, pos, 1.5, 72)
        o = math.tan(math.radians(8)) * FH / 2
        pts = f'{-o:.1f},{FH} {FW - o:.1f},{FH} {FW + o:.1f},0 {o:.1f},0'
        d.defs.append(f'<clipPath id="fc{i}"><polygon points="{pts}"/></clipPath>')
        sw = measure(small, 'Anton', 13, .2) + 20
        bfs = 40 if measure(big, 'Anton', 40) < FW - 40 else 34
        d.add(f'<g transform="translate({x},{y})"><g style="animation:favIn .45s cubic-bezier(.2,1.6,.4,1) {.2 + i * .1:.2f}s both">'
              f'<g style="animation:shake {3.6 + i * .5:.1f}s steps(1) {i * .8:.1f}s infinite">'
              f'<polygon points="{pts}" fill="{shc}" transform="translate(12,12)"/>'
              f'<g clip-path="url(#fc{i})"><image href="{im}" x="{-o:.0f}" width="{FW + 2 * o:.0f}" height="{FH}" preserveAspectRatio="xMidYMid slice"/>'
              f'<rect x="{-o:.0f}" width="{FW + 2 * o:.0f}" height="{FH}" fill="url(#fg)"/>'
              f'<rect x="0" y="0" width="90" height="{FH}" fill="#fff" opacity=".25" style="animation:glint 6s ease-in-out {i * 1.1:.1f}s infinite"/></g>'
              f'<polygon points="{pts}" fill="none" stroke="{INK}" stroke-width="5"/>'
              f'<rect x="16" y="{FH - 66}" width="{sw:.0f}" height="20" fill="{GOLD}"/>' + d.text(26, FH - 51, small, 'Anton', 13, INK, 'start', .2)
              + d.text(16, FH - 12, big, 'Anton', bfs, '#fff', 'start', 0, f'stroke="{INK}" stroke-width="6" paint-order="stroke"') + '</g></g></g>')
    d.add(crt(d, W, H))
    d.save('profile.svg')


# =====================================================================
# 8. CONTACT: calling card + link buttons
# =====================================================================
def contact():
    H = 380
    d = Doc(W, H, "Calling card: let's build something. Agency.")
    d.add(f'<rect width="{W}" height="{H}" fill="{INK}"/>' + stripes(d, W, H, .25))
    CW, CH = 820, 290
    sil, sa = cutout('sil-front.webp', CH * .78)
    d.defs.append(f'<pattern id="cs" width="16" height="16" patternUnits="userSpaceOnUse" patternTransform="rotate(-45)"><rect width="8" height="16" fill="#000" fill-opacity=".12"/></pattern>')
    g, w, h = ransom(d, "LET'S BUILD SOMETHING", 54, bob=6)
    k = min(1, (CW * .66) / w)
    d.css.append('@keyframes flip{from{transform:perspective(1200px) rotateY(95deg) scale(.6)}}')
    d.css.append('@keyframes flipx{0%{transform:scaleX(.05) scale(.6)}100%{transform:none}}')
    card = (f'<rect x="18" y="18" width="{CW}" height="{CH}" fill="#fff"/><rect x="18" y="18" width="{CW}" height="{CH}" fill="{INK}" transform="translate(-6,-6)"/>'
            f'<rect width="{CW}" height="{CH}" fill="{RED}" stroke="{INK}" stroke-width="12"/><rect x="6" y="6" width="{CW - 12}" height="{CH - 12}" fill="url(#cs)"/>'
            f'<image href="{sil}" x="{CW - 40 - CH * .78 * sa:.0f}" y="24" width="{CH * .78 * sa:.0f}" height="{CH * .78:.0f}" style="animation:breathe 3.2s ease-in-out infinite"/>'
            f'<g transform="translate(34,40) scale({k:.3f})">{g}</g>'
            + d.text(34, CH - 70, 'GITHUB · LINKEDIN · DEVPOST · EMAIL', 'Anton', 22, INK, 'start', .1)
            + d.text(34, CH - 40, 'ryanpanda78@gmail.com', 'Mono', 18, '#fff')
            + d.text(CW - 34, CH - 26, '— AGENCY', 'Anton', 16, '#fff', 'end', .3))
    d.add(f'<g transform="translate({(W - CW) / 2:.0f},{(H - CH) / 2 - 8:.0f}) rotate(-3 {CW / 2} {CH / 2})"><g class="c" style="animation:flipx .6s cubic-bezier(.2,1.5,.4,1) both">{card}</g></g>')
    d.save('contact.svg')

    links = [('GITHUB', 'TheAgencyMGE'), ('LINKEDIN', 'ryan-panda'), ('DEVPOST', '51 hackathons'), ('EMAIL', 'ryanpanda78@gmail.com')]
    for i, (big, small) in enumerate(links):
        BW_, BH_ = 480, 96
        d = Doc(BW_, BH_, f'{big}: {small}')
        d.css.append('@keyframes slidebtn{from{transform:translateX(-600px)}}')
        d.css.append('@keyframes nudge{0%,80%,100%{transform:translate(0,0)}85%{transform:translate(-4px,-4px)}}')
        d.add(f'<g style="animation:slidebtn .35s cubic-bezier(.2,1.6,.4,1) {.1 + i * .08:.2f}s both"><g style="animation:nudge 3s ease-out {i * .75:.2f}s infinite">'
              + skewbox(22, 14, BW_ - 54, 60, -10, '#fff', INK, 4, RED if i % 2 == 0 else GOLD, 8, 8)
              + d.text(40, 59, big, 'Anton', 38, INK)
              + d.text(BW_ - 46, 52, small, 'Mono', 15 if len(small) < 18 else 12.5, INK, 'end') + '</g></g>')
        d.save(f'link-{big.lower()}.svg')


# =====================================================================
# 9. FOOTER: visualizer + continue
# =====================================================================
def footer():
    H = 200
    d = Doc(W, H, 'Thanks for playing. Agency.')
    ember_css(d, H)
    d.add(f'<rect width="{W}" height="{H}" fill="{RED}"/>' + stripes(d, W, H, .5) + dots(d, W, H))
    d.defs.append(f'<linearGradient id="bglow2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{RED}" stop-opacity="0"/><stop offset="1" stop-color="#ff6e14" stop-opacity=".6"/></linearGradient>')
    d.add(f'<rect width="{W}" height="{H}" fill="url(#bglow2)"/>')
    d.add(embers(W, H, 20, drops=6))
    d.add(bars(d, W, H, 90, rng=random.Random(11)))
    g, w, h = ransom(d, 'THANKS FOR PLAYING', 44, bob=6)
    d.add(f'<g transform="translate({W / 2 - w / 2:.0f},30) rotate(-4 {w / 2:.0f} {h / 2:.0f})">{g}</g>')
    d.add(f'<g transform="translate(500,{50 + h + 18}) rotate(-4) skewX(-12)"><rect x="-90" y="-18" width="180" height="32" fill="{INK}"/>'
          + d.text(0, 7, '— AGENCY', 'Anton', 18, GOLD, 'middle', .3) + '</g>')
    d.add(crt(d, W, H))
    d.save('footer.svg')


# =====================================================================
README = """<!-- RYAN PANDA // CODENAME: AGENCY -->

<p align="center">
  <img src="assets/intro.svg" width="100%" alt="RYAN PANDA. They call me Agency.">
</p>

<p align="center">
  <img src="assets/menu.svg" width="100%" alt="Main menu: Ryan Panda, codename Agency">
</p>

<p align="center">
  <img src="assets/title-work.svg" width="100%" alt="WORK">
</p>

<p align="center">
{cards}
</p>

<p align="center">
  <a href="https://github.com/TheAgencyMGE?tab=repositories"><img src="assets/chip-1.svg" height="64" alt="30 repos"></a>
  <a href="https://devpost.com/TheAgencyMGE"><img src="assets/chip-2.svg" height="64" alt="24 Devpost projects"></a>
  <a href="https://devpost.com/TheAgencyMGE"><img src="assets/chip-3.svg" height="64" alt="51 hackathons"></a>
  <img src="assets/chip-4.svg" height="64" alt="$2,000+ won">
</p>

<p align="center">
  <img src="assets/experience.svg" width="100%" alt="Experience: SDE Intern at Remit2Any, Co-President at Luma Coding, AI and Coding Instructor at Coding Mind Academy, Instructor at iCode Redmond. Trophies: 1st HackaByte CA, 2nd RecessHacks 5.0, Top 10 of 900+ FusionHacks 2, Best in Track StellarNet, 3rd WA State TSA, XDA feature for Aero Dock.">
</p>

<p align="center">
  <img src="assets/skills.svg" width="100%" alt="Skills: Python, TypeScript, JavaScript, Rust, C#, Java, Dart, SQL, React, React Native, Tauri, Electron, Flutter, Angular, Node.js, WPF, Firebase, SQLite, scikit-learn, pandas, TensorFlow, Hugging Face, LLM APIs, Figma, Photoshop, Illustrator, Git, GitHub Actions">
</p>

<p align="center">
  <img src="assets/profile.svg" width="100%" alt="Profile: Ryan Panda, UW Informatics '30, Seattle WA. Fav game Destiny 2, fav show Attack on Titan, fav movie Pacific Rim.">
</p>

<p align="center">
  <img src="assets/contact.svg" width="100%" alt="Calling card: Let's build something">
</p>

<p align="center">
  <a href="https://github.com/TheAgencyMGE"><img src="assets/link-github.svg" width="48%" alt="GitHub: TheAgencyMGE"></a>
  <a href="https://linkedin.com/in/ryan-panda-5b021a352"><img src="assets/link-linkedin.svg" width="48%" alt="LinkedIn: ryan-panda"></a>
  <a href="https://devpost.com/TheAgencyMGE"><img src="assets/link-devpost.svg" width="48%" alt="Devpost: 51 hackathons"></a>
  <a href="mailto:ryanpanda78@gmail.com"><img src="assets/link-email.svg" width="48%" alt="Email: ryanpanda78@gmail.com"></a>
</p>

<p align="center">
  <img src="assets/footer.svg" width="100%" alt="Thanks for playing">
</p>
"""


def readme():
    cards = '\n'.join(f'  <a href="{url}"><img src="assets/work-{i + 1}.svg" width="32%" alt="{t}: {s}"></a>'
                      for i, (t, s, _, _, url) in enumerate(WORK))
    with open(os.path.join(HERE, '..', 'README.md'), 'w', encoding='utf-8') as fh:
        fh.write(README.replace('{cards}', cards))


if __name__ == '__main__':
    import sys
    only = sys.argv[1:]
    jobs = {
        'intro': intro, 'menu': menu,
        'titles': lambda: title_banner('WORK', 'SELECTED PROJECTS', 'title-work.svg'),
        'work': lambda: [work_card(i, t, s, img, pos) for i, (t, s, img, pos, _) in enumerate(WORK)],
        'chips': chips, 'experience': experience, 'skills': skills, 'profile': profile,
        'contact': contact, 'footer': footer, 'readme': readme,
    }
    for k, f in jobs.items():
        if not only or k in only:
            f()
