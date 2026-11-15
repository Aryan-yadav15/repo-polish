"""Restyle a finished Archify diagram in the repo-polish card style, then (optionally) capture light/dark PNGs.

Archify draws every colour from CSS variables and marks elements with classes and data attributes, so the theme is
pure CSS injected after Archify's own styles. Layout, validation and interactivity are untouched — run Archify's
`finalize` first, theme the HTML it produced, and keep the candidate JSON as the source of truth.

Run:
  uv run --with fonttools --with brotli python tools/archify-theme/theme.py <in.html> <out.html> \
      --accent '#6d28d9,#a78bfa' [--security …] [--async …] [--png <out-prefix>]

Colour rule: one project accent for the main path and core logic; meaning colours only where the diagram declares
them (security/policy = red, async = indigo, both overridable); everything else neutral.
"""
import argparse
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "cards"))
from fonts import font_css  # noqa: E402

PALETTE = {
    "light": dict(bg="#f5f5f7", card="#ffffff", fg="#1d1d1f", sub="#6e6e73", dim="#8e8e93", rule="#d2d2d7", rule2="#c7c7cc"),
    "dark": dict(bg="#1c1c1e", card="#2c2c2e", fg="#f5f5f7", sub="#98989d", dim="#8e8e93", rule="#3a3a3c", rule2="#48484a"),
}


def hexa(color, alpha):
    c = color.lstrip("#")
    r, g, b = (int(c[i:i + 2], 16) for i in (0, 2, 4))
    return f"rgba({r}, {g}, {b}, {alpha})"


def variables(p, accent, security, asynch):
    """Archify's variables, mapped onto the card palette. !important beats presets injected at runtime."""
    v = {
        "--bg": p["bg"], "--grid": "transparent", "--canvas-dot": "transparent",
        "--panel": p["bg"], "--panel-border": p["rule"],
        "--text": p["fg"], "--text-muted": p["sub"], "--text-dim": p["dim"], "--text-faint": p["dim"],
        "--lane-fill": "transparent", "--lane-stroke": p["rule"],
        "--arrow": p["dim"], "--arrow-emphasis": accent,
        "--mask": p["bg"],  # label backgrounds sit on the page colour; nodes are opaque cards anyway
        # neutral surfaces with hairlines; the accent marks logic and gates
        "--frontend-fill": p["card"], "--frontend-stroke": p["rule2"],
        "--backend-fill": p["card"], "--backend-stroke": hexa(accent, .55),
        "--database-fill": p["card"], "--database-stroke": p["rule2"],
        "--cloud-fill": p["card"], "--cloud-stroke": p["rule2"],
        "--messagebus-fill": p["card"], "--messagebus-stroke": p["rule2"],
        "--external-fill": p["bg"], "--external-stroke": p["rule2"],
        # meaning colours: used only where the diagram says security/policy or async
        "--security-fill": hexa(security, .10), "--security-stroke": security,
        "--polish-async": asynch,
        "--toolbar-bg": p["card"], "--toolbar-border": p["rule"], "--toolbar-text": p["fg"],
        "--toolbar-hover": p["bg"], "--toolbar-menu-bg": p["card"],
    }
    return "".join(f"{k}: {val} !important;" for k, val in v.items())


def css(accent_light, accent_dark, sec=("#d70015", "#ff453a"), asy=("#5856d6", "#7d7aff")):
    fonts = font_css("PolishSans", "Inter", "wght@100..900") + font_css("PolishDisplay", "Bricolage Grotesque", "wght@200..800")
    sans = "'PolishSans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
    return f"""
{fonts}
:root {{ --archify-sans: {sans} !important; }}
:root:not([data-theme="dark"]), [data-theme="light"] {{ {variables(PALETTE["light"], accent_light, sec[0], asy[0])} }}
[data-theme="dark"] {{ {variables(PALETTE["dark"], accent_dark, sec[1], asy[1])} }}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ {variables(PALETTE["dark"], accent_dark, sec[1], asy[1])} }} }}

body, svg text, .toolbar, .card {{ font-family: {sans} !important; }}
h1, .title, header h1 {{ font-family: 'PolishDisplay', {sans} !important; letter-spacing: -0.02em; }}
svg text {{ font-feature-settings: "tnum", "cv11"; }}

/* boxes: solid hairline cards with softer corners */
g[data-node-id] > rect {{ rx: 12px; ry: 12px; }}
g[data-node-id] > rect[class^="c-"]:not(.c-mask) {{ stroke-width: 1.25px; }}
g[data-node-kind="security"] > rect.c-security {{ stroke-width: 1.5px; }}
.semantic-sigil {{ opacity: .45 !important; }}
/* no glows: Archify adds drop-shadow filters (strongest on sequence participants) */
svg [filter], svg g[data-node-id] *, svg rect {{ filter: none !important; }}

/* lanes: quiet solid frames, small-caps labels */
.c-lane {{ stroke-dasharray: none !important; fill: transparent !important; }}
/* never change glyph widths: Archify measures text to place label backgrounds and avoid collisions */
svg text.t-dim {{ font-weight: 700 !important; }}
rect[fill="url(#grid)"] {{ display: none; }}

/* "dashed" edges are Archify's async / secondary paths (it colours them with the database purple): give them the
   async meaning colour so they stay distinct from plain returns */
path.a-dashed, line.a-dashed {{ stroke: var(--polish-async) !important; }}
.t-edge-dashed {{ fill: var(--polish-async) !important; }}
marker[id*="dashed"] path, marker[id*="dashed"] polygon {{ fill: var(--polish-async) !important; stroke: var(--polish-async) !important; }}

/* phase headers: muted small caps; the emphasised phase takes the accent */
.t-messagebus, .t-frontend, .t-cloud, .t-database, .t-external {{ fill: var(--text-muted) !important; }}
.t-backend {{ fill: var(--arrow-emphasis) !important; }}

/* groups: solid accent hairline instead of dashes */
rect[data-composition-frame-kind="group"] {{ stroke-dasharray: none !important; stroke-opacity: .5; }}

/* legend title, muted */
g[data-legend] > text.t-primary {{ fill: var(--text-muted) !important; }}

/* arrows a touch finer; labels sit on the page colour */
path.a-default, path.a-dashed {{ stroke-width: 1.2px; }}
path.a-emphasis, path.a-security {{ stroke-width: 1.6px; }}
"""


# extra rules used only while capturing static images: hide the interactive chrome
STATIC = """
.toolbar, .no-print, [class*="rail-control"], .source-evidence-beacon, [data-source-evidence-beacon] { display: none !important; }
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("out")
    ap.add_argument("--accent", default="#0071e3,#2997ff", help="light,dark accent colours")
    ap.add_argument("--security", default="#d70015,#ff453a", help="light,dark colour for security/policy paths and gates")
    ap.add_argument("--async", dest="asynch", default="#5856d6,#7d7aff", help="light,dark colour for async/secondary paths")
    ap.add_argument("--png", help="prefix for <prefix>-light.png / <prefix>-dark.png")
    a = ap.parse_args()
    light, dark = a.accent.split(",")
    html = Path(a.src).read_text()
    style = f'<style id="repo-polish-theme">{css(light, dark, tuple(a.security.split(",")), tuple(a.asynch.split(",")))}</style>'
    if 'id="repo-polish-theme"' in html:
        raise SystemExit("already themed; theme the original Archify output instead")
    themed = html.replace("</head>", style + "\n</head>", 1)
    Path(a.out).write_text(themed)
    print(f"themed → {a.out}")
    if a.png:
        static = Path(a.out).with_suffix(".static.html")
        static.write_text(themed.replace("</head>", f'<style>{STATIC}</style>\n</head>', 1))
        try:
            subprocess.run(["node", str(HERE / "capture.mjs"), str(static.resolve()), a.png], check=True)
        finally:
            static.unlink(missing_ok=True)


main()
