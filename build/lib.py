"""Shared helpers: fonts (subset + embed), images (crop + embed), ransom lettering, keyframes."""
import base64, io, os, random
from xml.sax.saxutils import escape
from fontTools.ttLib import TTFont
from fontTools import subset
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
PORT = os.path.join(os.path.expanduser('~'), 'Downloads', 'ryan-panda-portfolio', 'img')

RED, DEEP, GOLD, INK, PAPER, WHITE = '#E8291C', '#A80D14', '#F4B400', '#070707', '#F6F1E4', '#FFFFFF'

FONT_FILES = {
    'Anton': 'Anton-Regular.ttf',
    'Bowlby': 'BowlbyOne-Regular.ttf',
    'Archivo': 'ArchivoBlack-Regular.ttf',
    'Abril': 'AbrilFatface-Regular.ttf',
    'Mono': 'SpaceMono-Bold.ttf',
}
_fonts = {}


def font(name):
    if name not in _fonts:
        tt = TTFont(os.path.join(HERE, 'fonts', FONT_FILES[name]))
        upm = tt['head'].unitsPerEm
        cap = getattr(tt['OS/2'], 'sCapHeight', 0) or int(upm * 0.7)
        _fonts[name] = dict(tt=tt, cmap=tt.getBestCmap(), hmtx=tt['hmtx'], upm=upm, cap=cap / upm)
    return _fonts[name]


def measure(text, fname, size, ls=0.0):
    f = font(fname)
    w = 0
    for ch in text:
        g = f['cmap'].get(ord(ch))
        w += (f['hmtx'][g][0] / f['upm']) if g else 0.55
    return w * size + ls * size * len(text)


def cap(fname):
    return font(fname)['cap']


def _subset_b64(fname, chars):
    opts = subset.Options()
    opts.flavor = 'woff2'
    opts.layout_features = ['kern']
    opts.name_IDs = []
    opts.notdef_outline = True
    f = subset.load_font(os.path.join(HERE, 'fonts', FONT_FILES[fname]), opts)
    s = subset.Subsetter(opts)
    s.populate(text=chars)
    s.subset(f)
    buf = io.BytesIO()
    subset.save_font(f, buf, opts)
    return base64.b64encode(buf.getvalue()).decode()


# ---------------- images ----------------
def _uri(im, fmt, q):
    buf = io.BytesIO()
    if fmt == 'jpeg':
        im.convert('RGB').save(buf, 'JPEG', quality=q, optimize=True, progressive=True)
        return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()
    im.save(buf, 'WEBP', quality=q, method=6)
    return 'data:image/webp;base64,' + base64.b64encode(buf.getvalue()).decode()


def cover(path, w, h, pos=(0.5, 0.5), scale=1.5, q=74):
    """Crop like CSS background-size:cover with background-position, return data URI."""
    im = Image.open(os.path.join(PORT, path)).convert('RGB')
    W, H = int(w * scale), int(h * scale)
    r = max(W / im.width, H / im.height)
    im = im.resize((max(W, round(im.width * r)), max(H, round(im.height * r))), Image.LANCZOS)
    x = round((im.width - W) * pos[0])
    y = round((im.height - H) * pos[1])
    return _uri(im.crop((x, y, x + W, y + H)), 'jpeg', q)


def cutout(path, h, q=80, recolor=None, scale=1.4):
    """Alpha image scaled to display height h (webp keeps transparency)."""
    im = Image.open(os.path.join(PORT, path)).convert('RGBA')
    H = int(h * scale)
    im = im.resize((round(im.width * H / im.height), H), Image.LANCZOS)
    if recolor:
        a = im.split()[3]
        im = Image.new('RGBA', im.size, recolor)
        im.putalpha(a)
    return _uri(im, 'webp', q), im.width / im.height


def lummask(path, h, scale=1.2):
    """White-on-black luminance mask built from an alpha silhouette."""
    im = Image.open(os.path.join(PORT, path)).convert('RGBA')
    H = int(h * scale)
    im = im.resize((round(im.width * H / im.height), H), Image.LANCZOS)
    a = im.split()[3]
    out = Image.new('RGB', im.size, (0, 0, 0))
    out.paste((255, 255, 255), mask=a)
    return _uri(out, 'webp', 85), im.width / im.height


# ---------------- svg document ----------------
class Doc:
    def __init__(self, w, h, title):
        self.w, self.h, self.title = w, h, title
        self.chars = {}
        self.css = []
        self.defs = []
        self.body = []
        self._kf = 0

    def use(self, fname, text):
        self.chars.setdefault(fname, set()).update(text)
        return escape(text, {"'": '&#39;', '"': '&quot;'})

    def text(self, x, y, s, fname, size, fill=WHITE, anchor='start', ls=0, extra=''):
        t = self.use(fname, s)
        lsa = f' letter-spacing="{ls * size:.2f}"' if ls else ''
        return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{fname}" font-size="{size:.1f}" '
                f'fill="{fill}" text-anchor="{anchor}"{lsa} {extra}>{t}</text>')

    def kf(self, body, prefix='k'):
        self._kf += 1
        name = f'{prefix}{self._kf}'
        self.css.append(f'@keyframes {name}{{{body}}}')
        return name

    def timeline(self, L, frames, prefix='t'):
        """frames: list of (seconds, 'css props', optional timing-fn). Returns keyframe name."""
        out = []
        for f in frames:
            t, props = f[0], f[1]
            tf = f'animation-timing-function:{f[2]};' if len(f) > 2 else ''
            pct = max(0.0, min(100.0, t / L * 100))
            out.append(f'{pct:.3f}%{{{props};{tf}}}')
        return self.kf(''.join(out), prefix)

    def add(self, s):
        self.body.append(s)

    def render(self):
        faces = []
        for fname, chars in sorted(self.chars.items()):
            chars = ''.join(sorted(chars | {' '}))
            faces.append(f"@font-face{{font-family:'{fname}';src:url(data:font/woff2;base64,{_subset_b64(fname, chars)}) format('woff2')}}")
        css = '\n'.join(faces + [BASE_CSS] + self.css)
        return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
                f'width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}" role="img" aria-label="{escape(self.title)}">\n'
                f'<title>{escape(self.title)}</title>\n<style>\n{css}\n</style>\n<defs>{"".join(self.defs)}</defs>\n'
                + '\n'.join(self.body) + '\n</svg>\n')

    def save(self, name):
        p = os.path.join(HERE, '..', 'assets', name)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        data = self.render()
        with open(p, 'w', encoding='utf-8') as fh:
            fh.write(data)
        print(f'{name}: {len(data) / 1024:.0f} KB')


BASE_CSS = """
.c{transform-box:fill-box;transform-origin:center}
.bl{transform-box:fill-box;transform-origin:0% 50%}
.bb{transform-box:fill-box;transform-origin:50% 100%}
@keyframes bob6{50%{transform:translateY(-6px)}}
@keyframes bob10{50%{transform:translateY(-10px)}}
@keyframes bob4{50%{transform:translateY(-4px)}}
@keyframes drift{to{transform:translateX(186px)}}
@keyframes spin{to{transform:rotate(360deg)}}
@keyframes spinr{to{transform:rotate(-360deg)}}
@keyframes beat{0%{transform:scale(1.07)}35%{transform:scale(1)}100%{transform:scale(1)}}
@keyframes breathe{50%{transform:translateY(-8px)}}
@keyframes blink{0%,49.9%{opacity:1}50%,100%{opacity:0}}
@keyframes shake{0%,88%,100%{transform:translate(0,0)}90%{transform:translate(-4px,2px)}92%{transform:translate(3px,-3px)}94%{transform:translate(-2px,-2px)}96%{transform:translate(3px,1px)}}
@keyframes glint{0%,70%{transform:translateX(-700px) skewX(-20deg)}85%,100%{transform:translateX(900px) skewX(-20deg)}}
@keyframes wob{0%,100%{transform:rotate(-2deg)}50%{transform:rotate(2deg) scale(1.05)}}
@media (prefers-reduced-motion:reduce){*{animation-duration:.001s!important;animation-iteration-count:1!important;animation-delay:0s!important}}
"""

# ---------------- ransom lettering (same seeding as the portfolio's JS) ----------------
R_FONTS = ['Anton', 'Bowlby', 'Archivo', 'Abril']
R_STY = [(WHITE, INK), (INK, WHITE), (RED, WHITE), (GOLD, INK), (WHITE, RED)]


def ransom(doc, text, size, bob=6, delay0=0.0):
    """Returns (svg_group, width, height). Group origin = top-left of the word block."""
    seed = sum(ord(c) * (i + 3) for i, c in enumerate(text))
    words, cur = [], []
    for j, ch in enumerate(text):
        if ch == ' ':
            if cur:
                words.append(cur)
            cur = []
            continue
        f = R_FONTS[(seed + j * 5) % 4]
        bg, fg = R_STY[(seed + j * 7) % 5]
        fs = size * (0.86 + ((seed + j) % 4) * 0.08)
        rot = ((seed * j) % 15) - 7
        adv = measure(ch, f, fs)
        w = adv + 0.24 * fs + 0.1 * fs
        cur.append(dict(j=j, ch=ch, f=f, bg=bg, fg=fg, fs=fs, rot=rot, w=w, adv=adv))
    if cur:
        words.append(cur)
    out, x, H = [], 0.0, 0.0
    for wi, word in enumerate(words):
        wh = max(t['fs'] * (cap(t['f']) + 0.42) for t in word)
        H = max(H, wh)
        for t in word:
            cx, cy = x + t['w'] / 2, wh / 2
            ch_ = cap(t['f']) * t['fs']
            base = ch_ / 2
            anim = f' style="animation:bob{bob} 1.1s ease-in-out {delay0 + t["j"] * 0.07:.2f}s infinite"' if bob else ''
            out.append(
                f'<g{anim}><g transform="translate({cx:.1f},{cy:.1f}) rotate({t["rot"]})">'
                f'<rect x="{-t["w"] / 2:.1f}" y="{-wh / 2:.1f}" width="{t["w"]:.1f}" height="{wh:.1f}" fill="{t["bg"]}" stroke="{INK}" stroke-width="{0.05 * t["fs"]:.1f}"/>'
                + doc.text(0, base, t['ch'], t['f'], t['fs'], t['fg'], 'middle') + '</g></g>')
            x += t['w'] + 0.06 * size
        x += 0.3 * size - 0.06 * size
    width = x - 0.3 * size
    return '<g>' + ''.join(out) + '</g>', width, H


# ---------------- shared scenery ----------------
STAR = '50,0 61,35 98,35 68,57 79,91 50,70 21,91 32,57 2,35 39,35'


def star(cx, cy, s, fill):
    pts = ' '.join(f'{cx + (float(a) - 50) / 100 * s:.1f},{cy + (float(b) - 50) / 100 * s:.1f}'
                   for a, b in (p.split(',') for p in STAR.split()))
    return f'<polygon points="{pts}" fill="{fill}"/>'


def stripes(doc, w, h, opacity=0.5, angle=-32):
    pid = f'st{len(doc.defs)}'
    doc.defs.append(
        f'<pattern id="{pid}" width="186" height="40" patternUnits="userSpaceOnUse">'
        f'<rect x="90" width="60" height="40" fill="{INK}" fill-opacity=".92"/>'
        f'<rect x="175" width="11" height="40" fill="{INK}" fill-opacity=".92"/></pattern>')
    big = max(w, h) * 2
    return (f'<g opacity="{opacity}"><g transform="rotate({angle} {w / 2} {h / 2})">'
            f'<rect x="{-big}" y="{-big}" width="{big * 3}" height="{big * 3}" fill="url(#{pid})" style="animation:drift 9s linear infinite"/></g></g>')


def dots(doc, w, h, opacity=0.22, size=14):
    pid = f'dt{len(doc.defs)}'
    doc.defs.append(f'<pattern id="{pid}" width="{size}" height="{size}" patternUnits="userSpaceOnUse">'
                    f'<circle cx="{size / 2}" cy="{size / 2}" r="{size * 0.3:.1f}" fill="{INK}"/></pattern>')
    return f'<rect width="{w}" height="{h}" fill="url(#{pid})" opacity="{opacity}"/>'


def crt(doc, w, h):
    if 'crtp' not in ''.join(doc.defs):
        doc.defs.append('<pattern id="crtp" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="2" fill="#000" fill-opacity=".16"/></pattern>'
                        '<radialGradient id="vig" cx="50%" cy="50%" r="70%"><stop offset=".6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".55"/></radialGradient>')
    return f'<rect width="{w}" height="{h}" fill="url(#vig)" pointer-events="none"/><rect width="{w}" height="{h}" fill="url(#crtp)" pointer-events="none"/>'


def embers(w, h, n=40, rng=None, drops=0):
    rng = rng or random.Random(7)
    out = []
    for _ in range(n):
        x = rng.uniform(0, w)
        r = rng.uniform(1, 3.4)
        d = rng.uniform(4, 9)
        dx = rng.uniform(-40, 40)
        name = f'em{int(h)}'
        out.append(f'<circle cx="{x:.0f}" cy="{h + 10}" r="{r:.1f}" fill="{GOLD}" '
                   f'style="animation:{name} {d:.1f}s linear {-rng.uniform(0, d):.1f}s infinite;--dx:{dx:.0f}px"/>')
    for _ in range(drops):
        x = rng.uniform(0, w)
        l = rng.uniform(20, 70)
        d = rng.uniform(1.2, 2.6)
        out.append(f'<rect x="{x:.0f}" y="{-l:.0f}" width="{rng.uniform(2, 5):.1f}" height="{l:.0f}" rx="2" fill="url(#lava)" '
                   f'style="animation:fall{int(h)} {d:.1f}s cubic-bezier(.5,0,1,1) {-rng.uniform(0, d * 3):.1f}s infinite"/>')
    return '<g style="mix-blend-mode:screen">' + ''.join(out) + '</g>'


def ember_css(doc, h):
    doc.css.append(f'@keyframes em{int(h)}{{0%{{transform:translate(0,0);opacity:.95}}100%{{transform:translate(var(--dx),-{h + 40}px);opacity:0}}}}')
    doc.css.append(f'@keyframes fall{int(h)}{{0%{{transform:translateY(0)}}100%{{transform:translateY({h + 100}px)}}}}')
    if 'id="lava"' not in ''.join(doc.defs):
        doc.defs.append(f'<linearGradient id="lava" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{RED}" stop-opacity="0"/>'
                        f'<stop offset=".7" stop-color="{RED}" stop-opacity=".85"/><stop offset="1" stop-color="#ffd65a"/></linearGradient>')


def panel_bg(doc, w, h):
    """Portfolio panel look: lit red world + stripes behind a near-black wash."""
    doc.defs.append(f'<linearGradient id="wash" x1="0" y1="0" x2="1" y2=".5"><stop offset=".55" stop-color="{INK}" stop-opacity=".95"/>'
                    f'<stop offset="1" stop-color="{INK}" stop-opacity=".84"/></linearGradient>')
    return (f'<rect width="{w}" height="{h}" fill="{RED}"/>' + stripes(doc, w, h, 0.5) + dots(doc, w, h)
            + f'<rect width="{w}" height="{h}" fill="url(#wash)"/>')


def bars(doc, w, y_base, maxh, n=44, rng=None, opacity=1.0):
    """Mirrored skewed spectrum bars with peak caps, beat-synced (0.5s = the song's beat)."""
    rng = rng or random.Random(3)
    half, bw = w / 2, (w / 2) / n
    out = [f'<g opacity="{opacity}">']
    for b in range(n):
        lvl = max(0.15, 1 - b / n * 0.75) * rng.uniform(0.55, 1)
        hgt = maxh * lvl
        dur = rng.choice([0.5, 0.5, 1.0, 0.25])
        delay = -rng.uniform(0, dur)
        col = GOLD if b % 3 == 0 else RED
        for side in (-1, 1):
            x = half + side * (b * bw) + (-bw if side < 0 else 0) + 1
            out.append(f'<g transform="translate({x:.1f},{y_base}) skewX(-14)">'
                       f'<rect class="bb" x="0" y="{-hgt:.1f}" width="{bw - 3:.1f}" height="{hgt:.1f}" fill="{col}" '
                       f'style="animation:eq {dur}s ease-out {delay:.2f}s infinite"/>'
                       f'<rect x="0" y="{-hgt - 8:.1f}" width="{bw - 3:.1f}" height="4" fill="#fff" '
                       f'style="animation:cap {dur}s ease-out {delay:.2f}s infinite;--h:{hgt:.0f}px"/></g>')
    out.append('</g>')
    if '@keyframes eq' not in ''.join(doc.css):
        doc.css.append('@keyframes eq{0%{transform:scaleY(1)}60%{transform:scaleY(.25)}100%{transform:scaleY(1)}}')
        doc.css.append('@keyframes cap{0%{transform:translateY(0)}70%{transform:translateY(calc(var(--h) * .6))}100%{transform:translateY(0)}}')
    return ''.join(out)


def outline_filter(doc, fid='ol', r=5, color='#fff'):
    doc.defs.append(f'<filter id="{fid}" x="-10%" y="-10%" width="120%" height="120%"><feMorphology in="SourceAlpha" operator="dilate" radius="{r}" result="d"/>'
                    f'<feFlood flood-color="{color}"/><feComposite in2="d" operator="in" result="w"/>'
                    f'<feMerge><feMergeNode in="w"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')


def chroma_filter(doc, fid='ca', d=6):
    doc.defs.append(f'<filter id="{fid}" x="-20%" y="-20%" width="140%" height="140%">'
                    f'<feOffset in="SourceAlpha" dx="-{d}" result="a"/><feFlood flood-color="#00ffff" flood-opacity=".55"/><feComposite in2="a" operator="in" result="c"/>'
                    f'<feOffset in="SourceAlpha" dx="{d}" result="b"/><feFlood flood-color="#ff003c" flood-opacity=".6"/><feComposite in2="b" operator="in" result="r"/>'
                    f'<feMerge><feMergeNode in="c"/><feMergeNode in="r"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')


def skewbox(x, y, w, h, skew, fill, stroke=None, sw=0, shadow=None, sdx=0, sdy=0):
    """Parallelogram (CSS skewX) as polygon, optional hard shadow."""
    import math
    o = math.tan(math.radians(-skew)) * h / 2
    pts = lambda dx, dy: f'{x - o + dx:.1f},{y + h + dy:.1f} {x + w - o + dx:.1f},{y + h + dy:.1f} {x + w + o + dx:.1f},{y + dy:.1f} {x + o + dx:.1f},{y + dy:.1f}'
    s = ''
    if shadow:
        s += f'<polygon points="{pts(sdx, sdy)}" fill="{shadow}"/>'
    st = f' stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="miter"' if stroke else ''
    return s + f'<polygon points="{pts(0, 0)}" fill="{fill}"{st}/>'
