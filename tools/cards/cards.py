"""Generates README cards (hero, architecture, flow, capabilities, decisions, stack,
terminal, editor) as animated SVGs in light and dark variants.

Every card is optional except the hero: a card is drawn only if its section exists in the config.
Fonts are embedded and animation is pure SMIL, so cards render inside GitHub's <img> sandbox.

Run: uv run --with fonttools --with brotli python tools/cards/cards.py <cards.json> <out_dir>
Schema: see templates/cards.example.json
"""
import sys
import textwrap
from pathlib import Path
from xml.sax.saxutils import escape

from fonts import font_css, text_width
import json
import re
import urllib.request

DISPLAY_FAMILY, DISPLAY_SPEC = "Bricolage Grotesque", "wght@200..800"
SANS_FAMILY, SANS_SPEC = "Inter", "wght@100..900"
FONT_CSS = font_css("Display", DISPLAY_FAMILY, DISPLAY_SPEC) + font_css("Sans", SANS_FAMILY, SANS_SPEC)
DISPLAY = "'Display','Segoe UI',Helvetica,Arial,sans-serif"
SF = "'Sans',-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,'SF Mono',Menlo,Consolas,monospace"

BASE = {
    "light": dict(bg="#f5f5f7", card="#ffffff", fg="#1d1d1f", sub="#6e6e73", rule="#d2d2d7"),
    "dark": dict(bg="#1c1c1e", card="#2c2c2e", fg="#f5f5f7", sub="#98989d", rule="#3a3a3c"),
}
EASE = 'calcMode="spline" keyTimes="0;1" keySplines=".2 .8 .2 1"'


def theme(p, mode):
    return {**BASE[mode], "accent": p["accent"][mode]}


def rise(begin, dy=14):
    return (f'<animate attributeName="opacity" from="0" to="1" begin="{begin}s" dur=".9s" fill="freeze" {EASE}/>'
            f'<animateTransform attributeName="transform" type="translate" from="0 {dy}" to="0 0" begin="{begin}s" dur="1.1s" fill="freeze" {EASE}/>')


def grow(attr, to, begin, dur=1.0):
    return f'<animate attributeName="{attr}" from="0" to="{to}" begin="{begin}s" dur="{dur}s" fill="freeze" {EASE}/>'


def svg_open(W, H, label, t):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{escape(label)}">'
            f'<style>{FONT_CSS}</style><rect width="{W}" height="{H}" rx="28" fill="{t["bg"]}"/>')


def masthead(W, t, left, mid, right):
    return f"""<g font-family="{SF}" font-size="12" font-weight="600" letter-spacing="2.2" fill="{t['sub']}" opacity="0">{rise(.1, 0)}
  <text x="40" y="46">{escape(left)}</text>
  <text x="{W / 2}" y="46" text-anchor="middle" fill="{t['fg']}">{escape(mid)}</text>
  <text x="{W - 40}" y="46" text-anchor="end">{escape(right)}</text>
</g>
<rect x="40" y="62" height="1" width="0" fill="{t['fg']}">{grow('width', W - 80, .2, 1.1)}</rect>"""


def section_head(t, kicker, title, y=56):
    return (f'<g opacity="0">{rise(.1, 8)}<text x="40" y="{y}" font-family="{SF}" font-size="12" font-weight="700" letter-spacing="2.2" fill="{t["accent"]}">{escape(kicker)}</text>'
            f'<text x="40" y="{y + 40}" font-family="{DISPLAY}" font-size="34" font-weight="700" letter-spacing="-.8" fill="{t["fg"]}">{escape(title)}</text></g>')


def code_line(line, kw, t):
    """Colour SQL keywords with the accent."""
    out = []
    for tok in line.split(" "):
        out.append(f'<tspan fill="{t["accent"]}" font-weight="600">{escape(tok)}</tspan>' if tok.rstrip(";,") in set(kw) else escape(tok))
    return " ".join(out)


# ---------------------------------------------------------------- hero
def hero(p, mode, out):
    t = theme(p, mode)
    W, H = 1200, 500
    h = p["hero"]
    s = [svg_open(W, H, f'{p["title"]}. {" ".join(h["tagline"])}', t), masthead(W, t, *h["masthead"])]

    # title, sized to fill the left column
    size = min(104, 112 * 540 / text_width(DISPLAY_FAMILY, DISPLAY_SPEC, p["title"], 112, -4))
    s.append(f'<g opacity="0">{rise(.35, 22)}<text x="36" y="214" font-family="{DISPLAY}" font-size="{size:.0f}" font-weight="800" letter-spacing="-4" fill="{t["fg"]}">{escape(p["title"])}<tspan fill="{t["accent"]}">.</tspan></text></g>')
    a, b = h["tagline"]
    s.append(f'<g opacity="0">{rise(.7)}<text x="40" y="270" font-family="{SF}" font-size="30" font-weight="600" letter-spacing="-.6" fill="{t["sub"]}">{escape(a)} <tspan fill="{t["fg"]}">{escape(b)}</tspan></text></g>')
    for i, line in enumerate(textwrap.wrap(h["blurb"], 52)):
        s.append(f'<g opacity="0">{rise(.95 + i * .08, 8)}<text x="40" y="{312 + i * 28}" font-family="{SF}" font-size="19" fill="{t["sub"]}">{escape(line)}</text></g>')

    # demo card: question types in -> SQL appears -> result bars grow
    x0, y0, cw, ch = 680, 88, 480, 326
    d = h["demo"]
    l_ask, l_code, l_out = d.get("labels", ["YOU ASK", "IT WRITES", "YOU GET"])
    s.append(f'<g opacity="0">{rise(.6, 18)}<rect x="{x0}" y="{y0}" width="{cw}" height="{ch}" rx="20" fill="{t["card"]}" stroke="{t["rule"]}"/>')
    lab = f'font-family="{SF}" font-size="11" font-weight="700" letter-spacing="1.8"'
    s.append(f'<text x="{x0 + 24}" y="{y0 + 32}" {lab} fill="{t["sub"]}">{escape(l_ask)}</text>')
    s.append(f'<clipPath id="type-{mode}"><rect x="{x0 + 22}" y="{y0 + 40}" height="30" width="0">{grow("width", cw - 44, 1.2, 1.6)}</rect></clipPath>')
    s.append(f'<text x="{x0 + 24}" y="{y0 + 62}" clip-path="url(#type-{mode})" font-family="{SF}" font-size="19" font-weight="600" fill="{t["fg"]}">{escape(d["question"])}</text>')
    s.append(f'<rect x="{x0 + 24}" y="{y0 + 80}" width="{cw - 48}" height="1" fill="{t["rule"]}"/>')
    s.append(f'<text x="{x0 + 24}" y="{y0 + 106}" {lab} fill="{t["accent"]}">{escape(l_code)}</text></g>')
    for i, line in enumerate(d["code"]):
        s.append(f'<g opacity="0">{rise(3.0 + i * .3, 6)}<text x="{x0 + 24}" y="{y0 + 130 + i * 20}" font-family="{MONO}" font-size="13" fill="{t["fg"]}" xml:space="preserve">{code_line(line, d["keywords"], t)}</text></g>')
    ry = y0 + 130 + len(d["code"]) * 20 + 12
    s.append(f'<g opacity="0">{rise(4.0, 4)}<rect x="{x0 + 24}" y="{ry - 14}" width="{cw - 48}" height="1" fill="{t["rule"]}"/><text x="{x0 + 24}" y="{ry + 10}" {lab} fill="{t["sub"]}">{escape(l_out)}</text></g>')
    top = max(v for _, v in d["rows"])
    for i, (name, v) in enumerate(d["rows"]):
        y = ry + 34 + i * 24
        bw = (cw - 48 - 260) * v / top
        s.append(f'<g opacity="0">{rise(4.3 + i * .15, 4)}<text x="{x0 + 24}" y="{y}" font-family="{SF}" font-size="14" fill="{t["fg"]}">{escape(name)}</text>'
                 f'<rect x="{x0 + 150}" y="{y - 11}" height="12" rx="6" width="0" fill="{t["accent"]}" opacity=".85">{grow("width", f"{bw:.0f}", 4.4 + i * .15, 1.2)}</rect>'
                 f'<text x="{x0 + cw - 24}" y="{y}" text-anchor="end" font-family="{MONO}" font-size="13" fill="{t["sub"]}">{escape(str(v))}</text></g>')

    # facts pill
    py = 432
    s.append(f'<g opacity="0">{rise(1.3, 10)}<rect x="40" y="{py}" width="{W - 80}" height="44" rx="22" fill="{t["fg"]}"/>')
    n = len(h["facts"])
    for i, f in enumerate(h["facts"]):
        cx = 40 + (W - 80) * (i + .5) / n
        s.append(f'<text x="{cx:.0f}" y="{py + 27}" text-anchor="middle" font-family="{SF}" font-size="13" font-weight="600" letter-spacing="1.8" fill="{t["bg"]}">{escape(f.upper())}</text>')
        if i:
            s.append(f'<circle cx="{40 + (W - 80) * i / n:.0f}" cy="{py + 22}" r="2.5" fill="{t["accent"]}"/>')
    s.append("</g></svg>")
    (out / f"hero-{mode}.svg").write_text("\n".join(s))


# ---------------------------------------------------------------- architecture
def box(t, x, y, w, h, title, sub, begin, strong=False):
    fill = t["fg"] if strong else t["card"]
    tc, sc = (t["bg"], t["rule"]) if strong else (t["fg"], t["sub"])
    stroke = "none" if strong else t["rule"]
    return (f'<g opacity="0">{rise(begin, 10)}<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{fill}" stroke="{stroke}"/>'
            f'<text x="{x + 20}" y="{y + 34}" font-family="{SF}" font-size="18" font-weight="700" fill="{tc}">{escape(title)}</text>'
            f'<text x="{x + 20}" y="{y + 58}" font-family="{SF}" font-size="14" fill="{sc}">{escape(sub)}</text></g>')


def wire(t, pid, d, begin, dashed=False, dot=True):
    dash = ' stroke-dasharray="5 6"' if dashed else ""
    col = t["accent"] if dashed else t["sub"]
    w = (f'<path id="{pid}" d="{d}" fill="none" stroke="{col}" stroke-width="1.5"{dash} opacity="0">'
         f'<animate attributeName="opacity" from="0" to=".9" begin="{begin}s" dur=".6s" fill="freeze"/></path>')
    if dot:
        w += (f'<circle r="4" fill="{t["accent"]}" opacity="0"><set attributeName="opacity" to="1" begin="{begin + .4}s"/>'
              f'<animateMotion dur="2.6s" begin="{begin + .4}s" repeatCount="indefinite" {"keyPoints=\"1;0\" keyTimes=\"0;1\" calcMode=\"linear\"" if dashed else ""}><mpath href="#{pid}"/></animateMotion></circle>')
    return w


def architecture(p, mode, out):
    t = theme(p, mode)
    A = p["arch"]
    W, H = 1200, 640
    s = [svg_open(W, H, A["alt"], t), section_head(t, A["kicker"], A["title"])]
    colhead = f'font-family="{SF}" font-size="11" font-weight="700" letter-spacing="1.8" fill="{t["sub"]}"'
    for x, label in [(40, A["cols"][0]), (350, A["cols"][1]), (880, A["cols"][2])]:
        s.append(f'<g opacity="0">{rise(.2, 0)}<text x="{x}" y="144" {colhead}>{escape(label)}</text></g>')

    # client column
    s.append(box(t, 40, 160, 260, 84, *A["client"][0], .3))
    s.append(box(t, 40, 320, 260, 84, *A["client"][1], .4))
    # server column
    s.append(box(t, 350, 160, 480, 84, *A["server"], .5))
    s.append(f'<g opacity="0">{rise(.6, 10)}<rect x="350" y="290" width="480" height="300" rx="16" fill="{t["fg"]}"/>'
             f'<text x="370" y="324" font-family="{SF}" font-size="18" font-weight="700" fill="{t["bg"]}">{escape(A["agent"][0])}</text>'
             f'<text x="370" y="348" font-family="{SF}" font-size="14" fill="{t["rule"]}">{escape(A["agent"][1])}</text></g>')
    tool_y = []
    for i, (name, what) in enumerate(A["tools"]):
        y = 368 + i * 52
        tool_y.append(y + 20)
        s.append(f'<g opacity="0">{rise(.8 + i * .12, 6)}<rect x="370" y="{y}" width="440" height="40" rx="20" fill="{t["bg"]}" opacity=".1"/>'
                 f'<rect x="370" y="{y}" width="440" height="40" rx="20" fill="none" stroke="{t["accent"]}" stroke-opacity=".7"/>'
                 f'<text x="390" y="{y + 25}" font-family="{MONO}" font-size="13" font-weight="600" fill="{t["bg"]}">{escape(name)}</text>'
                 f'<text x="790" y="{y + 25}" text-anchor="end" font-family="{SF}" font-size="13" fill="{t["rule"]}">{escape(what)}</text></g>')
    # data column
    data_y = [160, 290, 420]
    for (title, sub), y in zip(A["data"], data_y):
        s.append(box(t, 880, y, 280, 84, title, sub, 1.0))

    # wires
    s.append(wire(t, f"w1{mode}", "M170 244 L170 320", 1.3))
    s.append(wire(t, f"w2{mode}", "M300 362 C 330 362, 320 210, 350 210", 1.4))
    s.append(wire(t, f"w3{mode}", "M590 244 L590 290", 1.5))
    s.append(wire(t, f"w4{mode}", "M830 320 C 860 320, 850 202, 880 202", 1.6))
    for k, (ti, di) in enumerate(A["links"]):
        s.append(wire(t, f"wl{k}{mode}", f"M810 {tool_y[ti]} C 850 {tool_y[ti]}, 840 {data_y[di] + 42}, 880 {data_y[di] + 42}", 1.7 + k * .1))
    s.append(wire(t, f"sse{mode}", "M350 180 C 330 180, 320 190, 300 190", 1.9, dashed=True))
    s.append(f'<g opacity="0">{rise(2.0, 4)}<text x="325" y="172" text-anchor="middle" font-family="{SF}" font-size="11" font-weight="700" letter-spacing="1.4" fill="{t["accent"]}">SSE</text></g>')
    s.append(f'<g opacity="0">{rise(2.1, 4)}<text x="40" y="{H - 30}" font-family="{SF}" font-size="14" fill="{t["sub"]}">{escape(A["footnote"])}</text></g>')
    s.append("</svg>")
    (out / f"architecture-{mode}.svg").write_text("\n".join(s))


# ---------------------------------------------------------------- flow
def flow(p, mode, out):
    t = theme(p, mode)
    F = p["flow"]
    W, H = 1200, 340
    n = len(F["steps"])
    step_w = (W - 80) / n
    s = [svg_open(W, H, F["alt"], t), section_head(t, F["kicker"], F["title"])]
    s.append(f'<rect x="40" y="150" height="2" width="0" fill="{t["rule"]}">{grow("width", W - 80, .3, 1.4)}</rect>')
    s.append(f'<rect x="40" y="150" height="2" width="0" fill="{t["accent"]}">{grow("width", W - 80, 1.2, 3.2)}</rect>')
    for i, (title, cap) in enumerate(F["steps"]):
        x = 40 + i * step_w
        b = 1.2 + i * 3.2 / n
        s.append(f'<circle cx="{x + 7}" cy="151" r="7" fill="{t["bg"]}" stroke="{t["rule"]}" stroke-width="2"/>'
                 f'<circle cx="{x + 7}" cy="151" r="0" fill="{t["accent"]}">{grow("r", 7, b, .5)}</circle>')
        s.append(f'<g opacity="0">{rise(b, 8)}<text x="{x}" y="206" font-family="{DISPLAY}" font-size="15" font-weight="700" fill="{t["accent"]}">{i + 1:02d}</text>'
                 f'<text x="{x}" y="234" font-family="{SF}" font-size="19" font-weight="700" fill="{t["fg"]}">{escape(title)}</text>')
        for j, line in enumerate(textwrap.wrap(cap, 24)):
            s.append(f'<text x="{x}" y="{262 + j * 22}" font-family="{SF}" font-size="15" fill="{t["sub"]}">{escape(line)}</text>')
        s.append("</g>")
    s.append("</svg>")
    (out / f"flow-{mode}.svg").write_text("\n".join(s))


# ---------------------------------------------------------------- capabilities (replaces the 2×2 table)
def capabilities(p, mode, out):
    t = theme(p, mode)
    C = p["capabilities"]
    tw, th, gap = 550, 220, 20
    W, H = 1200, 130 + 2 * th + gap + 30
    s = [svg_open(W, H, C["alt"], t), section_head(t, C["kicker"], C["title"])]
    for i, c in enumerate(C["items"]):
        x, y = 40 + (i % 2) * (tw + gap), 130 + (i // 2) * (th + gap)
        g = [f'<g opacity="0">{rise(.3 + i * .12, 10)}<rect x="{x}" y="{y}" width="{tw}" height="{th}" rx="18" fill="{t["card"]}" stroke="{t["rule"]}"/>',
             f'<text x="{x + 26}" y="{y + 38}" font-family="{SF}" font-size="11" font-weight="700" letter-spacing="1.8" fill="{t["accent"]}">{i + 1:02d} · {escape(c["kicker"])}</text>',
             f'<text x="{x + 26}" y="{y + 72}" font-family="{DISPLAY}" font-size="24" font-weight="700" letter-spacing="-.4" fill="{t["fg"]}">{escape(c["title"])}</text>',
             f'<text x="{x + 26}" y="{y + 102}" font-family="{SF}" font-size="16" font-style="italic" fill="{t["fg"]}" opacity=".8">“{escape(c["ask"])}”</text>']
        for j, line in enumerate(textwrap.wrap(c["does"], 62)[:2]):
            g.append(f'<text x="{x + 26}" y="{y + 134 + j * 22}" font-family="{SF}" font-size="15" fill="{t["sub"]}">{escape(line)}</text>')
        cw_ = len(c["tool"]) * 7.9 + 24
        g.append(f'<rect x="{x + 26}" y="{y + th - 46}" width="{cw_:.0f}" height="26" rx="13" fill="{t["accent"]}" opacity=".12"/>'
                 f'<text x="{x + 38}" y="{y + th - 28}" font-family="{MONO}" font-size="13" font-weight="600" fill="{t["accent"]}">{escape(c["tool"])}</text></g>')
        s += g
    s.append("</svg>")
    (out / f"capabilities-{mode}.svg").write_text("\n".join(s))


# ---------------------------------------------------------------- decisions (replaces the decisions table)
def decisions(p, mode, out):
    t = theme(p, mode)
    D = p["decisions"]
    rh = 96
    W, H = 1200, 130 + len(D["items"]) * rh + 20
    s = [svg_open(W, H, D["alt"], t), section_head(t, D["kicker"], D["title"])]
    for i, (title, why) in enumerate(D["items"]):
        y = 130 + i * rh
        g = [f'<g opacity="0">{rise(.3 + i * .12, 8)}<rect x="40" y="{y}" width="{W - 80}" height="1" fill="{t["rule"]}"/>',
             f'<text x="40" y="{y + 52}" font-family="{DISPLAY}" font-size="40" font-weight="800" letter-spacing="-1" fill="{t["accent"]}">{i + 1:02d}</text>',
             f'<text x="130" y="{y + 38}" font-family="{SF}" font-size="20" font-weight="700" fill="{t["fg"]}">{escape(title)}</text>']
        for j, line in enumerate(textwrap.wrap(why, 118)[:2]):
            g.append(f'<text x="130" y="{y + 64 + j * 22}" font-family="{SF}" font-size="15" fill="{t["sub"]}">{escape(line)}</text>')
        s += g + ["</g>"]
    s.append("</svg>")
    (out / f"decisions-{mode}.svg").write_text("\n".join(s))


# ---------------------------------------------------------------- stack (replaces the built-with table)
ICONS = Path(__file__).parent / "icons"


def icon(slug, x, y, size, fill):
    """Simple Icons logo by slug (https://simpleicons.org), fetched once and cached; a dot if unavailable."""
    f = ICONS / f"{slug}.svg" if slug else None
    if f and not f.exists():
        try:
            f.write_bytes(urllib.request.urlopen(f"https://cdn.jsdelivr.net/npm/simple-icons@latest/icons/{slug}.svg", timeout=10).read())
        except Exception:
            pass
    if not f or not f.exists():
        return f'<circle cx="{x + size / 2}" cy="{y + size / 2}" r="{size / 5}" fill="{fill}"/>'
    d = re.search(r'<path d="([^"]+)"', f.read_text()).group(1)
    return f'<path transform="translate({x} {y}) scale({size / 24})" d="{d}" fill="{fill}"/>'


def stack(p, mode, out):
    t = theme(p, mode)
    S = p["stack"]
    n = len(S["cols"])
    colw = (1200 - 80) / n
    rows = max(len(items) for _, items in S["cols"])
    W, H = 1200, 150 + rows * 46 + 20
    s = [svg_open(W, H, S["alt"], t), section_head(t, S["kicker"], S["title"])]
    for ci, (label, items) in enumerate(S["cols"]):
        x = 40 + ci * colw
        g = [f'<g opacity="0">{rise(.3 + ci * .12, 8)}<text x="{x}" y="146" font-family="{SF}" font-size="11" font-weight="700" letter-spacing="1.8" fill="{t["sub"]}">{escape(label)}</text>'
             f'<rect x="{x}" y="158" width="{colw - 30:.0f}" height="1" fill="{t["rule"]}"/>']
        for ri, (name, slug) in enumerate(items):
            y = 176 + ri * 46
            g.append(icon(slug, x, y, 22, t["fg"]))
            g.append(f'<text x="{x + 34}" y="{y + 17}" font-family="{SF}" font-size="16" font-weight="{600 if ri == 0 else 500}" fill="{t["fg"]}">{escape(name)}</text>')
        s += g + ["</g>"]
    s.append("</svg>")
    (out / f"stack-{mode}.svg").write_text("\n".join(s))


# ---------------------------------------------------------------- terminal + editor windows
TERM = dict(bg="#161618", bar="#232326", fg="#e6e6e6", dim="#8a8a8e", ok="#32d74b", prompt="#64d2ff",
            kw="#c586c0", fn="#dcdcaa", str="#ce9178", num="#b5cea8", com="#6a9955", gutter="#5a5a5e")


def window(t, x, y, w, h, title, begin):
    dots = "".join(f'<circle cx="{x + 22 + i * 20}" cy="{y + 20}" r="6" fill="{c}"/>' for i, c in enumerate(["#ff5f57", "#febc2e", "#28c840"]))
    return (f'<g opacity="0">{rise(begin, 12)}<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{TERM["bg"]}" stroke="{t["rule"]}"/>'
            f'<path d="M{x} {y + 40} V{y + 14} a14 14 0 0 1 14 -14 H{x + w - 14} a14 14 0 0 1 14 14 V{y + 40} Z" fill="{TERM["bar"]}"/>{dots}'
            f'<text x="{x + w / 2}" y="{y + 25}" text-anchor="middle" font-family="{SF}" font-size="13" font-weight="600" fill="{TERM["dim"]}">{escape(title)}</text></g>')


def terminal(p, mode, out):
    t = theme(p, mode)
    T = p["terminal"]
    lh = 24
    W = 1200
    H = 130 + 40 + len(T["lines"]) * lh + 40 + 30
    s = [svg_open(W, H, T["alt"], t), section_head(t, T["kicker"], T["title"])]
    s.append(window(t, 40, 130, W - 80, H - 160, T["window"], .2))
    clock, y = .8, 130 + 40 + 30
    for i, (kind, text) in enumerate(T["lines"]):
        if kind == "cmd":
            pre = T["prompt"] + " "
            px = 64 + len(pre) * 8.4
            s.append(f'<g opacity="0">{rise(clock, 0)}<text x="64" y="{y}" font-family="{MONO}" font-size="14" fill="{TERM["prompt"]}" xml:space="preserve">{escape(pre)}</text></g>')
            dur = max(.5, len(text) * .03)
            s.append(f'<clipPath id="tc{i}{mode}"><rect x="{px:.0f}" y="{y - 18}" height="26" width="0">{grow("width", len(text) * 8.4 + 10, clock + .2, dur)}</rect></clipPath>'
                     f'<text x="{px:.0f}" y="{y}" clip-path="url(#tc{i}{mode})" font-family="{MONO}" font-size="14" fill="{TERM["fg"]}" xml:space="preserve">{escape(text)}</text>')
            clock += dur + .45
        elif kind == "com":
            s.append(f'<g opacity="0">{rise(clock, 0)}<text x="64" y="{y}" font-family="{MONO}" font-size="14" fill="{TERM["com"]}" xml:space="preserve">{escape(text)}</text></g>')
            clock += .25
        elif kind in ("out", "ok"):
            col = TERM["ok"] if kind == "ok" else TERM["dim"]
            s.append(f'<g opacity="0">{rise(clock, 0)}<text x="64" y="{y}" font-family="{MONO}" font-size="14" fill="{col}" xml:space="preserve">{escape(text)}</text></g>')
            clock += .18
        y += lh
    # blinking cursor after the last line
    s.append(f'<rect x="64" y="{y - 16}" width="9" height="18" fill="{TERM["fg"]}" opacity="0"><animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.1;.6;.7" dur="1.1s" begin="{clock}s" repeatCount="indefinite"/></rect>')
    s.append("</svg>")
    (out / f"terminal-{mode}.svg").write_text("\n".join(s))


def highlight_py(line):
    pat = re.compile(r'(?P<com>#.*$)|(?P<str>f?"(?:[^"\\]|\\.)*")|(?P<kw>\b(?:def|return|class|import|from|True|False|None|async|await)\b)'
                     r'|(?P<num>\b\d+\b)|(?P<fn>\b[A-Za-z_]\w*(?=\())')
    out, i = [], 0
    for m in pat.finditer(line):
        out.append(escape(line[i:m.start()]))
        out.append(f'<tspan fill="{TERM[m.lastgroup]}">{escape(m.group())}</tspan>')
        i = m.end()
    out.append(escape(line[i:]))
    return "".join(out)


def editor(p, mode, out):
    t = theme(p, mode)
    E = p["editor"]
    lh = 24
    W = 1200
    H = 130 + 40 + 36 + len(E["lines"]) * lh + 30 + 30
    s = [svg_open(W, H, E["alt"], t), section_head(t, E["kicker"], E["title"])]
    s.append(window(t, 40, 130, W - 80, H - 160, E["window"], .2))
    # file tab
    s.append(f'<g opacity="0">{rise(.3, 0)}<rect x="40" y="170" width="{W - 80}" height="36" fill="{TERM["bar"]}" opacity=".5"/>'
             f'<rect x="40" y="170" width="240" height="36" fill="{TERM["bg"]}"/><rect x="40" y="170" width="240" height="2" fill="{p["accent"]["dark"]}"/>'
             f'<text x="60" y="193" font-family="{SF}" font-size="13" fill="{TERM["fg"]}">{escape(E["file"])}</text></g>')
    y = 206 + 32
    for i, (num, code) in enumerate(E["lines"]):
        b = .5 + i * .07
        if num in E.get("notes", {}):
            s.append(f'<rect x="41" y="{y - 17}" width="{W - 82}" height="{lh}" fill="{p["accent"]["dark"]}" opacity="0"><animate attributeName="opacity" to=".18" begin="{b + 1.4}s" dur=".6s" fill="freeze"/></rect>')
        s.append(f'<g opacity="0">{rise(b, 0)}<text x="96" y="{y}" text-anchor="end" font-family="{MONO}" font-size="13" fill="{TERM["gutter"]}">{num if isinstance(num, int) else ""}</text>'
                 f'<text x="120" y="{y}" font-family="{MONO}" font-size="14" fill="{TERM["dim"] if num == "fold" else TERM["fg"]}" xml:space="preserve">{escape(code) if num == "fold" else highlight_py(code)}</text></g>')
        if num in E.get("notes", {}):
            s.append(f'<g opacity="0">{rise(b + 1.6, 0)}<text x="{W - 64}" y="{y}" text-anchor="end" font-family="{SF}" font-size="14" font-weight="600" fill="{p["accent"]["dark"]}">{escape(E["notes"][num])}</text></g>')
        y += lh
    s.append("</svg>")
    (out / f"editor-{mode}.svg").write_text("\n".join(s))


def load(path):
    p = json.loads(Path(path).read_text())
    if "editor" in p:  # JSON object keys are strings; line numbers are ints
        p["editor"]["notes"] = {int(k) if k.isdigit() else k: v for k, v in p["editor"].get("notes", {}).items()}
    return p


if __name__ == "__main__":
    out = Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    p = load(sys.argv[1])
    cards = [hero, architecture, flow, capabilities, decisions, stack, terminal, editor]
    for m in BASE:
        for card in cards:
            if {"architecture": "arch"}.get(card.__name__, card.__name__) in p:
                card(p, m, out)
    print(f"wrote {', '.join(c.__name__ for c in cards)} × light/dark → {out}")
