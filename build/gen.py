"""Builds the animated SVGs in ../assets and the profile README. Live stats come from stats.py."""
import math, os, random
from lib import *

W = 1000
SITE = 'https://theagencymge.xyz'


# =====================================================================
# HEADER: name, codename, typed roles, hero + burst, website tag
# =====================================================================
def header():
    H = 380
    d = Doc(W, H, 'Ryan Panda, codename Agency. Full-stack, mobile and AI developer in Seattle. theagencymge.xyz')
    outline_filter(d, 'ol', 4)
    ember_css(d, H)
    d.add(f'<rect width="{W}" height="{H}" fill="{RED}"/>' + stripes(d, W, H, .5) + dots(d, W, H))

    # starburst + hero
    hx, hy, R0 = 830, 175, 150
    rng = random.Random(5)
    def burst(r_in, r_out, var, off=0, n=44):
        return ' '.join(f'{math.cos(off + i / (n * 2) * math.tau) * (r_in if i % 2 else r_out + rng.uniform(0, var)):.0f},'
                        f'{math.sin(off + i / (n * 2) * math.tau) * (r_in if i % 2 else r_out + rng.uniform(0, var)):.0f}' for i in range(n * 2))
    d.add(f'<g transform="translate({hx},{hy})"><g class="c" style="animation:beat .5s ease-out infinite">'
          f'<g style="animation:spin 40s linear infinite"><polygon points="{burst(R0 * .92, R0 * 1.05, R0)}" fill="#fff"/></g>'
          f'<g style="animation:spinr 55s linear infinite"><polygon points="{burst(R0 * .8, R0 * .95, R0 * .8, .03)}" fill="{INK}"/></g>'
          f'<circle r="{R0 * .62:.0f}" fill="none" stroke="{RED}" stroke-width="9"/></g></g>')
    HH = 360
    art, aspect = cutout('hero.webp', HH)
    hw = HH * aspect
    d.css.append('@keyframes heroIn{from{transform:translateX(70%) rotate(8deg)}}')
    d.add(f'<g class="bb" style="animation:heroIn .55s cubic-bezier(.2,1.6,.4,1) both"><g class="bb" style="animation:beat .5s ease-out infinite">'
          f'<image href="{art}" x="{hx - hw / 2:.0f}" y="{H - HH + 6}" width="{hw:.0f}" height="{HH}" filter="url(#ol)" style="animation:breathe 3.2s ease-in-out infinite"/></g></g>')

    # name + codename
    nm, nw, nh = ransom(d, 'RYAN PANDA', 66)
    d.add(f'<g transform="translate(38,30) rotate(-4)">{nm}</g>')
    d.add(f'<g transform="translate(46,{30 + nh + 22}) rotate(-4) skewX(-12)"><rect width="250" height="30" fill="{INK}"/><rect width="6" height="30" fill="{GOLD}"/>'
          + d.text(18, 23, 'CODENAME: AGENCY', 'Anton', 18, '#fff', 'start', .3) + '</g>')

    # typed role line: per-character visibility so it works everywhere
    roles = ['FULL-STACK DEV', 'MOBILE DEV', 'ML RESEARCHER', 'UI/UX DESIGNER', 'HACKATHON CHAMP']
    per, L = 2.6, 2.6 * len(roles)
    fs, X0, Y0 = 44, 74, 222
    d.add(f'<g transform="translate(40,{Y0 - 42}) skewX(-10)"><rect width="560" height="58" fill="{INK}" stroke="#fff" stroke-width="4"/></g>')
    d.add(d.text(52, Y0, '>', 'Mono', 30, GOLD))
    cur_frames = [(0, 'transform:translateX(0)')]
    for ri, role in enumerate(roles):
        t0 = ri * per
        type_dt, del_dt = .07, .03
        x = X0
        tend = t0 + per - .15
        chars = []
        for j, ch in enumerate(role):
            on = t0 + .1 + j * type_dt
            off = tend - (len(role) - j) * del_dt
            k = d.timeline(L, [(0, 'opacity:0'), (on - .001, 'opacity:0'), (on, 'opacity:1'), (off, 'opacity:1'), (off + .001, 'opacity:0'), (L, 'opacity:0')], 'ty')
            chars.append(d.text(x, Y0, ch, 'Anton', fs, '#fff', 'start', 0, f'style="opacity:0;animation:{k} {L}s linear infinite"'))
            x += measure(ch, 'Anton', fs) + 1
            cur_frames.append((on + .001, f'transform:translateX({x - X0:.0f}px)'))
        for j in range(len(role)):
            off = tend - (len(role) - j) * del_dt
            cur_frames.append((off + .001, f'transform:translateX({sum(measure(c, "Anton", fs) + 1 for c in role[:j]):.0f}px)'))
        d.add(f'<g filter="url(#tsh)">{"".join(chars)}</g>')
    cur_frames.sort(key=lambda f: f[0])
    cur_frames.append((L, 'transform:translateX(0)'))
    ck = d.timeline(L, cur_frames, 'cu')
    d.defs.append(f'<filter id="tsh"><feDropShadow dx="4" dy="4" stdDeviation="0" flood-color="{RED}"/></filter>')
    d.add(f'<g style="animation:{ck} {L}s steps(1,end) infinite"><rect x="{X0 + 4}" y="{Y0 - 36}" width="18" height="40" fill="{GOLD}" style="animation:blink .8s linear infinite"/></g>')

    # tags: base + website
    t1 = "SEATTLE, WA · UW INFORMATICS '30"
    w1 = measure(t1, 'Anton', 18, .08) + 28
    d.add(f'<g transform="translate(46,262)">' + skewbox(0, 0, w1, 32, -12, '#fff', INK, 3, INK, 5, 5) + d.text(14, 23, t1, 'Anton', 18, INK, 'start', .08) + '</g>')
    t2 = '▸ THEAGENCYMGE.XYZ'
    w2 = measure(t2, 'Anton', 22, .1) + 30
    d.css.append('@keyframes nudge{0%,80%,100%{transform:translate(0,0)}85%{transform:translate(-4px,-4px)}}')
    d.add(f'<g transform="translate(46,306)"><g style="animation:nudge 2s ease-out infinite">' + skewbox(0, 0, w2, 38, -12, GOLD, INK, 3, INK, 6, 6)
          + d.text(16, 28, t2, 'Anton', 22, INK, 'start', .1) + '</g></g>')

    d.add(embers(W, H, 30, drops=8))
    d.defs.append(f'<linearGradient id="bglow" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{RED}" stop-opacity="0"/><stop offset="1" stop-color="#ff6e14" stop-opacity=".5"/></linearGradient>')
    d.add(f'<rect y="{H - 70}" width="{W}" height="70" fill="url(#bglow)"/>')
    d.add(bars(d, W, H, 34, opacity=.85))
    d.add(crt(d, W, H))
    d.save('header.svg')


# =====================================================================
# ABOUT: animated terminal showing agency.config.ts
# =====================================================================
ABOUT = [
    [('k', 'const '), ('v', 'agency'), ('p', ' = {')],
    [('p', '  '), ('key', 'name'), ('p', ':       '), ('s', '"Ryan Panda"'), ('p', ',')],
    [('p', '  '), ('key', 'codename'), ('p', ':   '), ('s', '"AGENCY"'), ('p', ',')],
    [('p', '  '), ('key', 'base'), ('p', ':       '), ('s', '"Seattle, WA"'), ('p', ',')],
    [('p', '  '), ('key', 'school'), ('p', ':     '), ('s', '"UW Informatics \'30"'), ('p', ',')],
    [('p', '  '), ('key', 'building'), ('p', ':   ['), ('s', '"full-stack web"'), ('p', ', '), ('s', '"mobile apps"'), ('p', ',')],
    [('p', '               '), ('s', '"AI / ML tools"'), ('p', ', '), ('s', '"desktop UX"'), ('p', '],')],
    [('p', '  '), ('key', 'currently'), ('p', ':  [')],
    [('p', '    '), ('s', '"AI Engineering Intern @ Arogya"'), ('p', ',')],
    [('p', '    '), ('s', '"Instructor @ iCode Redmond"'), ('p', ',')],
    [('p', '  ],')],
    [('p', '  '), ('key', 'previously'), ('p', ': '), ('s', '"SDE Intern @ Remit2Any"'), ('p', ',')],
    [('p', '  '), ('key', 'speaks'), ('p', ':     ['), ('s', '"English"'), ('p', ', '), ('s', '"Bengali"'), ('p', ', '), ('s', '"Spanish"'), ('p', '],')],
    [('p', '  '), ('key', 'offline'), ('p', ':    ['), ('s', '"Destiny 2"'), ('p', ', '), ('s', '"Attack on Titan"'), ('p', ', '), ('s', '"Pacific Rim"'), ('p', '],')],
    [('p', '  '), ('key', 'motto'), ('p', ':      '), ('s', '"Set the bar so low that mediocrity looks impressive."'), ('p', ',')],
    [('p', '};')],
]


def about():
    LH, FS, TOP = 27, 17, 98
    H = TOP + len(ABOUT) * LH + 30
    d = Doc(W, H, 'agency.config.ts')
    d.add(panel_bg(d, W, H))
    cols = {'k': RED, 'v': '#fff', 'p': '#d8d2c4', 'key': '#ff6a5c', 's': GOLD}
    d.add(f'<rect x="40" y="34" width="{W - 70}" height="{H - 54}" fill="{RED}"/>')
    d.add(f'<rect x="30" y="24" width="{W - 70}" height="{H - 54}" fill="{INK}" stroke="#fff" stroke-width="4"/>')
    d.add(f'<rect x="32" y="26" width="{W - 74}" height="38" fill="{RED}"/><rect x="32" y="64" width="{W - 74}" height="4" fill="#fff"/>')
    for i, c in enumerate((GOLD, '#fff', INK)):
        d.add(f'<circle cx="{58 + i * 26}" cy="45" r="8" fill="{c}" stroke="{INK}" stroke-width="2"/>')
    d.add(d.text(W / 2, 53, 'AGENCY.CONFIG.TS', 'Anton', 20, '#fff', 'middle', .2))
    # lines appear one by one, hold, then the loop restarts
    step, L = .16, 14.0
    cw = measure('a', 'Mono', FS)
    for i, line in enumerate(ABOUT):
        t0 = .3 + i * step
        k = d.timeline(L, [(0, 'opacity:0;transform:translateX(-14px)'), (t0, 'opacity:0;transform:translateX(-14px)', 'cubic-bezier(.2,1.6,.4,1)'),
                           (t0 + .2, 'opacity:1;transform:none'), (L - .5, 'opacity:1;transform:none'), (L - .2, 'opacity:0;transform:none'), (L, 'opacity:0')], 'ln')
        y = TOP + i * LH
        spans = ''.join(f'<tspan fill="{cols[c]}">{d.use("Mono", t)}</tspan>' for c, t in line)
        d.add(d.text(66, y, f'{i + 1:>2}', 'Mono', 12, '#6a6a6a', 'end', 0, f'style="opacity:0;animation:{k} {L}s linear infinite"'))
        d.add(f'<text x="82" y="{y}" font-family="Mono" font-size="{FS}" xml:space="preserve" style="opacity:0;animation:{k} {L}s linear infinite">{spans}</text>')
    # cursor rides down with each new line, then blinks at the end
    fr = [(0, 'transform:translate(0px,0px)')]
    for i, line in enumerate(ABOUT):
        n = sum(len(t) for _, t in line)
        fr.append((.3 + i * step + .2, f'transform:translate({n * cw + 4:.0f}px,{i * LH}px)'))
    fr.append((L, fr[-1][1]))
    ck = d.timeline(L, fr, 'cur')
    d.add(f'<g style="animation:{ck} {L}s steps(1,end) infinite"><rect x="82" y="{TOP - 16}" width="10" height="20" fill="{GOLD}" style="animation:blink .8s linear infinite"/></g>')
    d.add(crt(d, W, H))
    d.save('agency-config-v5.svg')


# =====================================================================
# Section banners (thin, animated)
# =====================================================================
def section(word, sub, fname):
    H = 112
    d = Doc(W, H, word)
    d.add(panel_bg(d, W, H))
    d.css.append('@keyframes wipe{from{clip-path:polygon(100% 0,100% 0,100% 100%,100% 100%)}to{clip-path:polygon(0 0,100% 0,100% 100%,0 100%)}}')
    d.css.append('@keyframes slidein{from{transform:translateX(1100px) skewX(-12deg)}}')
    g, w, h = ransom(d, word, 56, bob=6)
    d.add(f'<g style="animation:wipe .3s steps(5,end) both"><g transform="translate(34,{H / 2 - h / 2:.0f}) rotate(-4 {w / 2:.0f} {h / 2:.0f})">{g}</g></g>')
    kw = measure(sub, 'Anton', 18, .2) + 30
    d.add(f'<g transform="translate({60 + w:.0f},{H / 2 - 4:.0f}) skewX(-12)" style="animation:slidein .4s .2s cubic-bezier(.2,1.6,.4,1) both">'
          f'<rect width="{kw:.0f}" height="32" fill="{RED}"/>' + d.text(15, 24, sub, 'Anton', 18, '#fff', 'start', .2) + '</g>')
    d.add(f'<g transform="translate({W - 56},{H / 2})"><g style="animation:spin 6s linear infinite">{star(0, 0, 50, GOLD)}</g></g>')
    d.add(crt(d, W, H))
    d.save(fname)


# =====================================================================
# OPEN TO: quest board with live "accepting" lamps
# =====================================================================
def open_to():
    H = 330
    d = Doc(W, H, 'Open to: internships (software engineering, full-stack, mobile, AI/ML) and contract work (web apps, mobile apps, AI integrations, UI/UX).')
    d.add(panel_bg(d, W, H))
    d.css.append('@keyframes slide{from{transform:translateX(-1100px)}}')
    d.css.append('@keyframes ping{0%{transform:scale(1);opacity:.9}100%{transform:scale(3);opacity:0}}')
    d.css.append('@keyframes stamp{0%{transform:scale(3) rotate(-30deg);opacity:0}100%{transform:rotate(-12deg);opacity:1}}')
    quests = [('INTERNSHIPS', 'MAIN QUEST', ['SOFTWARE ENGINEERING', 'FULL-STACK · MOBILE', 'AI / ML'], RED),
              ('CONTRACT WORK', 'SIDE QUEST', ['WEB & MOBILE APPS', 'AI INTEGRATIONS', 'UI/UX & BRANDING'], GOLD)]
    CW, CH = 440, 236
    for i, (title, kind, lines, sh) in enumerate(quests):
        x, y = 40 + i * (CW + 50), 40
        body = (skewbox(0, 0, CW, CH, -6, INK, '#fff', 4, sh, 10, 10)
                + f'<g transform="translate(26,22) skewX(-12)"><rect width="{measure(kind, "Anton", 15, .2) + 20:.0f}" height="24" fill="{sh}"/></g>'
                + d.text(38, 40, kind, 'Anton', 15, INK if sh == GOLD else '#fff', 'start', .2)
                + d.text(26, 96, title, 'Anton', 46, '#fff', 'start', .02, f'stroke="{INK}" stroke-width="2"'))
        for j, ln in enumerate(lines):
            body += (f'<g transform="translate(36,{128 + j * 30})">{star(0, -7, 16, sh)}</g>'
                     + d.text(54, 134 + j * 30, ln, 'Anton', 19, '#fff', 'start', .06))
        # status lamp + stamp
        lx, ly = CW - 56, 44
        body += (f'<g transform="translate({lx},{ly})"><circle r="9" fill="{GOLD}" class="c" style="animation:ping 1.2s ease-out {i * .6:.1f}s infinite"/>'
                 f'<circle r="9" fill="{GOLD}" stroke="{INK}" stroke-width="2"/></g>'
                 + d.text(lx - 18, ly + 6, 'ACCEPTING', 'Anton', 15, GOLD, 'end', .12))
        body += (f'<g transform="translate({CW - 92},{CH - 64})"><g class="c" style="animation:stamp .45s cubic-bezier(.2,1.6,.4,1) {.8 + i * .2:.1f}s both">'
                 f'<rect x="-62" y="-26" width="124" height="52" fill="none" stroke="{sh}" stroke-width="5"/>'
                 + d.text(0, 14, 'OPEN', 'Bowlby', 34, sh, 'middle') + '</g></g>')
        d.add(f'<g transform="translate({x},{y})"><g style="animation:slide .4s cubic-bezier(.2,1.6,.4,1) {.1 + i * .12:.2f}s both">{body}</g></g>')
    d.add(d.text(W / 2, H - 14, 'PRESS START → RYANPANDA78@GMAIL.COM', 'Anton', 16, '#fff', 'middle', .25, 'style="animation:blink 1.2s linear infinite"'))
    d.add(crt(d, W, H))
    d.save('open-to.svg')


# =====================================================================
# FEATURED WORK cards (one SVG each so every card links somewhere)
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
    d.css.append('@keyframes pop{0%{transform:scale(0) rotate(-25deg)}100%{transform:none}}')
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


# =====================================================================
# TROPHIES: hackathon record
# =====================================================================
def trophies():
    items = ['1ST · HACKABYTE CA', '2ND · RECESSHACKS 5.0', 'TOP 10 / 900+ · FUSIONHACKS 2',
             'BEST IN TRACK · STELLARNET', '3RD · WA STATE TSA', 'XDA FEATURE · AERO DOCK']
    record = [('6X', 'HACKATHON WINNER'), ('$3K+', 'IN PRIZES')]
    H = 300
    d = Doc(W, H, 'Trophies: 6x hackathon winner, $3K+ in prizes. ' + ', '.join(items))
    d.add(panel_bg(d, W, H))
    d.css.append('@keyframes slide{from{transform:translateX(-1100px)}}')
    d.css.append('@keyframes popn{0%{transform:scale(0) rotate(-20deg)}100%{transform:none}}')
    for i, (num, lab) in enumerate(record):
        x = 40 + i * 470
        body = (skewbox(0, 0, 430, 84, -10, '#fff' if i % 2 == 0 else INK, INK if i % 2 == 0 else GOLD, 3, RED if i % 2 == 0 else GOLD, 7, 7)
                + d.text(30, 58, num, 'Bowlby', 38, RED if i % 2 == 0 else GOLD, 'start')
                + d.text(400, 54, lab, 'Anton', 28, INK if i % 2 == 0 else '#fff', 'end', .1))
        d.add(f'<g transform="translate({x},28)"><g class="c" style="animation:popn .45s cubic-bezier(.2,1.8,.4,1) {.1 + i * .08:.2f}s both">{body}</g></g>')
    tw, th = 290, 54
    for i, t in enumerate(items):
        x = 40 + (i % 3) * (tw + 22)
        y = 148 + (i // 3) * (th + 18)
        fs = 18 if measure(t, 'Anton', 18) < tw - 70 else 15.5
        d.add(f'<g transform="translate({x},{y})"><g style="animation:slide .35s cubic-bezier(.2,1.6,.4,1) {.5 + i * .07:.2f}s both">'
              + skewbox(0, 0, tw, th, -10, GOLD, INK, 3, INK, 6, 6)
              + f'<g transform="translate(30,{th / 2})"><g style="animation:beat 1s ease-out {i * .17:.2f}s infinite" class="c">{star(0, 0, 30, INK)}</g></g>'
              + d.text(56, th / 2 + fs * .38, t, 'Anton', fs, INK) + '</g></g>')
    d.add(crt(d, W, H))
    d.save('hackathon-record.svg')


# =====================================================================
# FOOTER
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
def badge(label, msg, color, logo, url, label_color='070707'):
    from urllib.parse import quote
    enc = lambda s: quote(s.replace('-', '--').replace('_', '__'), safe='')
    src = f'https://img.shields.io/badge/{enc(label)}-{enc(msg)}-{color}?style=for-the-badge&logo={logo}&logoColor=white&labelColor={label_color}'
    return f'<a href="{url}"><img src="{src}" alt="{label}: {msg}"></a>'


README = """<!-- RYAN PANDA // CODENAME: AGENCY -->

<p align="center">
  <a href="{site}"><img src="assets/header.svg" width="100%" alt="Ryan Panda, codename Agency. Full-stack, mobile and AI developer. theagencymge.xyz"></a>
</p>

<p align="center">
  {b_site}
</p>

<img src="assets/sec-about.svg" width="100%" alt="About me">

<p align="center">
  <img src="assets/agency-config-v5.svg" width="100%" alt="agency.config.ts: Ryan Panda, codename AGENCY, Seattle WA, UW Informatics 30. Building full-stack web, mobile apps, AI/ML tools, desktop UX. Currently AI Engineering Intern at Arogya and Instructor at iCode Redmond. Previously SDE Intern at Remit2Any. Speaks English, Bengali, Spanish.">
</p>

<img src="assets/sec-open.svg" width="100%" alt="Open to">

<p align="center">
  <img src="assets/open-to.svg" width="100%" alt="Open to internships (software engineering, full-stack, mobile, AI/ML) and contract work (web and mobile apps, AI integrations, UI/UX)">
</p>

> **Hiring for an internship or have a contract project?** Email **[ryanpanda78@gmail.com](mailto:ryanpanda78@gmail.com)**, message me on [LinkedIn](https://linkedin.com/in/ryan-panda-5b021a352), or see more at **[theagencymge.xyz]({site})**.

<img src="assets/sec-stack.svg" width="100%" alt="Tech stack">

<p align="center"><b>LANGUAGES</b><br><br>
  <img src="https://skillicons.dev/icons?i=py,ts,js,rust,cs,java,dart,html,css&perline=9" alt="Python, TypeScript, JavaScript, Rust, C#, Java, Dart, HTML, CSS">
</p>
<p align="center"><b>FRAMEWORKS & PLATFORMS</b><br><br>
  <img src="https://skillicons.dev/icons?i=react,nextjs,nodejs,flutter,angular,tauri,electron,tailwind,firebase,sqlite&perline=10" alt="React, Next.js, Node.js, Flutter, Angular, Tauri, Electron, Tailwind, Firebase, SQLite">
</p>
<p align="center"><b>AI, DESIGN & TOOLING</b><br><br>
  <img src="https://skillicons.dev/icons?i=tensorflow,sklearn,figma,ps,ai,git,githubactions,vercel&perline=8" alt="TensorFlow, scikit-learn, Figma, Photoshop, Illustrator, Git, GitHub Actions, Vercel">
</p>
<p align="center"><sub>also: React Native · WPF · pandas · Hugging Face · LLM APIs · SQL</sub></p>

<img src="assets/sec-stats.svg" width="100%" alt="Stats">

<p align="center">
  <img src="assets/stats.svg" width="100%" alt="Live GitHub stats">
</p>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/TheAgencyMGE/TheAgencyMGE/output/snake-dark.svg">
    <img src="https://raw.githubusercontent.com/TheAgencyMGE/TheAgencyMGE/output/snake-light.svg" width="100%" alt="Contribution graph being eaten by a snake">
  </picture>
</p>

<img src="assets/sec-work.svg" width="100%" alt="Featured work">

<p align="center">
{cards}
</p>

<img src="assets/sec-trophies.svg" width="100%" alt="Trophies">

<p align="center">
  <img src="assets/hackathon-record.svg" width="100%" alt="6x hackathon winner, $3K+ in prizes">
</p>

<img src="assets/sec-connect.svg" width="100%" alt="Connect">

<p align="center">
  {b_site}
  {b_li}
  {b_dev}
  {b_mail}
</p>

<p align="center">
  <img src="assets/footer.svg" width="100%" alt="Thanks for playing">
</p>
"""


def readme():
    cards = '\n'.join(f'  <a href="{url}"><img src="assets/work-{i + 1}.svg" width="32%" alt="{t}: {s}"></a>'
                      for i, (t, s, _, _, url) in enumerate(WORK))
    out = (README.replace('{cards}', cards).replace('{site}', SITE)
           .replace('{b_site}', badge('WEBSITE', 'theagencymge.xyz', 'E8291C', 'googlechrome', SITE))
           .replace('{b_li}', badge('LINKEDIN', 'ryan-panda', 'F4B400', 'linkedin', 'https://linkedin.com/in/ryan-panda-5b021a352'))
           .replace('{b_dev}', badge('DEVPOST', 'TheAgencyMGE', 'E8291C', 'devpost', 'https://devpost.com/TheAgencyMGE'))
           .replace('{b_mail}', badge('EMAIL', 'ryanpanda78@gmail.com', 'F4B400', 'gmail', 'mailto:ryanpanda78@gmail.com')))
    with open(os.path.join(HERE, '..', 'README.md'), 'w', encoding='utf-8') as fh:
        fh.write(out)


if __name__ == '__main__':
    import sys
    only = sys.argv[1:]
    jobs = {
        'header': header, 'about': about,
        'sections': lambda: [section(w, s, f) for w, s, f in [
            ('ABOUT ME', 'PLAYER PROFILE', 'sec-about.svg'), ('OPEN TO', 'NOW ACCEPTING QUESTS', 'sec-open.svg'),
            ('TECH STACK', 'INVENTORY', 'sec-stack.svg'), ('STATS', 'LIVE FROM GITHUB', 'sec-stats.svg'),
            ('WORK', 'FEATURED PROJECTS', 'sec-work.svg'), ('TROPHIES', 'HACKATHON RECORD', 'sec-trophies.svg'),
            ('CONNECT', 'SEND A CALLING CARD', 'sec-connect.svg')]],
        'open': open_to,
        'work': lambda: [work_card(i, t, s, img, pos) for i, (t, s, img, pos, _) in enumerate(WORK)],
        'trophies': trophies, 'footer': footer, 'readme': readme,
    }
    for k, f in jobs.items():
        if not only or k in only:
            f()
