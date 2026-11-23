#!/usr/bin/env python3
"""Generate assets/banner.svg: a terminal-style profile card with dot-matrix art.

Usage (from the repo root):
    python scripts/make_banner.py                 # monogram art (no photo needed)
    python scripts/make_banner.py --photo me.jpg  # your photo as 1-bit dot art

Needs: pip install Pillow numpy
"""
import argparse
import html
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps, ImageEnhance

OUT = Path(__file__).resolve().parents[1] / "assets" / "banner.svg"

W, H = 1180, 610
ACCENT = "#7dd3fc"      # dots + panel titles
DOTS = "#a5b4fc"
BG, PANEL, LINE = "#0d1117", "#111826", "#1f2a3d"
MUTED, TEXT = "#7d8aa5", "#e6edf3"

ROWS = [
    ("Subject",       "Yash"),
    ("Role",          "Developer · Competitive Programmer"),
    ("Origin",        "Uttar Pradesh, India"),
    ("Education",     "B.Tech · PSIT Kanpur"),
    ("Status",        "Building + Solving + Shipping"),
    ("Core.Lang",     "Java"),
    ("Core.Focus",    "Data Structures & Algorithms"),
    ("ToolChain",     "VS Code · Git · GitHub"),
    ("Grid.GitHub",   "porwalyash438"),
]

GRID_W, GRID_H = 150, 170   # dot grid for the left panel


def monogram():
    """White-on-black 'YA / SH' bitmap, dithered to dots."""
    img = Image.new("L", (GRID_W * 4, GRID_H * 4), 0)
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 330)
    for i, ch in enumerate("YASH"):
        x = (i % 2) * (GRID_W * 2) + GRID_W // 2 - 30
        y = (i // 2) * (GRID_H * 2) + 40
        d.text((x, y), ch, fill=255, font=font)
    img = img.filter(ImageFilter.GaussianBlur(7))
    # soft vertical fade so the dither reads like a halftone photo
    fade = np.linspace(1.0, 0.45, img.height)[:, None]
    return Image.fromarray((np.array(img) * fade).astype("uint8"))


def photo(path):
    img = ImageOps.exif_transpose(Image.open(path)).convert("L")
    img = ImageOps.fit(img, (GRID_W * 4, GRID_H * 4), centering=(0.5, 0.35))
    img = ImageOps.autocontrast(img, cutoff=2)
    return ImageEnhance.Contrast(img).enhance(1.3)


def to_dots(img):
    small = img.resize((GRID_W, GRID_H), Image.LANCZOS)
    bits = np.array(small.convert("1"))           # Floyd-Steinberg dither
    return np.argwhere(bits)                      # (row, col) of lit dots


def build(dots):
    px = 2.0                                      # dot pitch in SVG units
    ox, oy = 62, 118                              # panel origin
    path = "".join(f"M{ox + c * px:.1f} {oy + r * px:.1f}h1.4v1.4h-1.4z" for r, c in dots)

    rows = ""
    for i, (k, v) in enumerate(ROWS):
        y = 176 + i * 38
        rows += (f'<text x="436" y="{y}" fill="{MUTED}" font-size="15">{k}</text>'
                 f'<line x1="{436 + len(k) * 9 + 16}" x2="{1114 - 16 - len(v) * 9}" y1="{y - 4}" y2="{y - 4}" '
                 f'stroke="{LINE}" stroke-dasharray="1 5" stroke-linecap="round"/>'
                 f'<text x="1114" y="{y}" fill="{TEXT}" font-size="15" text-anchor="end">{html.escape(v)}</text>')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"
 font-family="JetBrains Mono, SFMono-Regular, Menlo, Consolas, monospace">
<style>
 @keyframes blink {{ 0%,100% {{opacity:1}} 50% {{opacity:.25}} }}
 @keyframes reveal {{ from {{clip-path: inset(0 0 100% 0)}} to {{clip-path: inset(0 0 0 0)}} }}
 .live {{ animation: blink 1.6s ease-in-out infinite }}
 .art  {{ animation: reveal 2.4s steps(40) both }}
</style>
<rect x="10" y="10" width="{W-20}" height="{H-20}" rx="18" fill="{BG}" stroke="{LINE}"/>
<circle cx="52" cy="46" r="7" fill="#ff5f56"/><circle cx="78" cy="46" r="7" fill="#ffbd2e"/><circle cx="104" cy="46" r="7" fill="#27c93f"/>
<text x="{W/2}" y="52" fill="{MUTED}" font-size="14" text-anchor="middle">profile.sh --live</text>

<rect x="40" y="84" width="340" height="474" rx="10" fill="{PANEL}" stroke="{LINE}"/>
<text x="62" y="108" fill="{ACCENT}" font-size="14" font-weight="700" letter-spacing="1">VISUAL.MAP</text>
<text x="360" y="108" fill="{MUTED}" font-size="11" text-anchor="end">{GRID_W}×{GRID_H} / 1-BIT</text>
<line x1="40" x2="380" y1="120" y2="120" stroke="{LINE}"/>
<path class="art" d="{path}" fill="{DOTS}"/>
<text x="62" y="545" fill="{MUTED}" font-size="10">PTS {len(dots)} · FS/DITHER</text>

<rect x="410" y="84" width="730" height="474" rx="10" fill="{PANEL}" stroke="{LINE}"/>
<text x="436" y="116" fill="{ACCENT}" font-size="14" font-weight="700" letter-spacing="1">SYSTEM.INFO</text>
<circle class="live" cx="960" cy="111" r="4" fill="#ff5c7a"/>
<text x="972" y="116" fill="#ff5c7a" font-size="12" font-weight="700">LIVE</text>
<rect x="1020" y="96" width="100" height="26" rx="13" fill="#12304a" stroke="{ACCENT}" stroke-opacity=".4"/>
<text x="1070" y="114" fill="{TEXT}" font-size="11" text-anchor="middle">@porwalyash438</text>
<line x1="410" x2="1140" y1="132" y2="132" stroke="{LINE}"/>
{rows}
<line x1="436" x2="1114" y1="520" y2="520" stroke="{LINE}"/>
<circle cx="440" cy="540" r="4" fill="#27c93f"/>
<text x="452" y="544" fill="#27c93f" font-size="11">ALL SYSTEMS NOMINAL</text>
<text x="1114" y="544" fill="{MUTED}" font-size="11" text-anchor="end">UTC+5:30 · IN NODE</text>
</svg>'''


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--photo", help="path to your photo (optional)")
    a = ap.parse_args()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build(to_dots(photo(a.photo) if a.photo else monogram())), encoding="utf-8")
    print("wrote", OUT)
