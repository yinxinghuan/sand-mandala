#!/usr/bin/env python3
"""Generate the Sand Mandala poster via online txt2img API + PIL title overlay.

Output: /Users/yin/code/games/sand-mandala/poster.png  (1024×1024)
"""
import json
import os
import ssl
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
OUT  = ROOT / "poster.png"

API_URL     = "http://aiservice.wdabuliu.com:8019/genl_image"
API_TIMEOUT = 360
RATE_WAIT   = 78
USER_ID     = 91501987

_SSL = ssl.create_default_context()
_SSL.check_hostname = False
_SSL.verify_mode = ssl.CERT_NONE

PROMPT = (
    "intricate Tibetan sand mandala, 8-fold radial symmetry, "
    "vivid sand grain texture, jewel-tone palette: deep saffron, gold, turquoise, "
    "lapis blue, crimson, sage green, bone white, "
    "concentric rings with lotus petals and geometric patterns, "
    "centered top-down view, faint blueprint guide lines fading at edges, "
    "deep midnight indigo background with subtle vignette, "
    "ultra detailed, sacred geometry, professional poster, square 1:1, "
    "photographic clarity"
)


def call_api(prompt: str) -> str:
    payload = json.dumps({
        "query": "",
        "params": {"prompt": prompt, "user_id": USER_ID},   # txt2img — no url
    }).encode()
    req = urllib.request.Request(
        API_URL, data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=API_TIMEOUT) as r:
            result = json.loads(r.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        try:    result = json.loads(body)
        except: sys.exit(f"HTTP {e.code}: {body}")
    code = result.get("code")
    if code == 200:
        return result["url"]
    if code in (429, 100):
        raise RuntimeError("rate_limit")
    sys.exit(f"API code={code}  msg={result.get('msg')}")


def download(url: str, dest: Path) -> None:
    src_ext = os.path.splitext(url.split("?")[0])[1].lower() or ".png"
    tmp = dest.with_suffix(dest.suffix + src_ext) if src_ext != dest.suffix else dest
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60, context=_SSL) as r:
        tmp.write_bytes(r.read())
    if tmp != dest:
        subprocess.run(["sips", "-s", "format", "png", str(tmp), "--out", str(dest)],
                       check=True, capture_output=True)
        tmp.unlink()


def add_title(src_path: Path, dst_path: Path) -> None:
    img = Image.open(src_path).convert("RGB")
    # square crop center, then resize to 1024
    w, h = img.size
    s = min(w, h)
    img = img.crop(((w - s) // 2, (h - s) // 2, (w - s) // 2 + s, (h - s) // 2 + s))
    img = img.resize((1024, 1024), Image.LANCZOS)

    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)

    # darken upper band so title reads cleanly (publish rule: title in upper half)
    # extends over title + subtitle, fades smoothly to image
    band_h = 320
    grad = Image.new("RGBA", (img.width, band_h), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grad)
    for y in range(band_h):
        a = int(195 * (1 - y / band_h) ** 1.4)
        gd.line([(0, y), (img.width, y)], fill=(8, 4, 18, a))
    overlay.paste(grad, (0, 0), grad)

    # title text
    try:
        font_main = ImageFont.truetype("/Library/Fonts/AGaramondPro-Bold.otf", 110)
        font_sub  = ImageFont.truetype("/Library/Fonts/AGaramondPro-Italic.otf", 30)
    except OSError:
        font_main = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia.ttf", 110)
        font_sub  = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia Italic.ttf", 30)

    title    = "SAND  MANDALA"
    subtitle = "draw · dissolve · begin again"

    # measure + center
    tw, th = d.textbbox((0, 0), title, font=font_main)[2:]
    tx = (img.width - tw) // 2
    ty = 56
    # subtle drop shadow
    d.text((tx + 3, ty + 4), title, font=font_main, fill=(0, 0, 0, 180))
    d.text((tx, ty), title, font=font_main, fill=(244, 235, 208, 250))

    sw, sh = d.textbbox((0, 0), subtitle, font=font_sub)[2:]
    sx = (img.width - sw) // 2
    sy = ty + th + 24
    d.text((sx + 1, sy + 2), subtitle, font=font_sub, fill=(0, 0, 0, 200))
    d.text((sx, sy), subtitle, font=font_sub, fill=(232, 200, 110, 255))

    final = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    final.save(dst_path, "PNG", optimize=True)
    print(f"saved {dst_path}  ({dst_path.stat().st_size // 1024} KB)")


def main():
    print("PROMPT:", PROMPT, "\n")
    print("calling API…  (txt2img, ~75-200s)")
    while True:
        try:
            url = call_api(PROMPT)
            break
        except RuntimeError:
            print(f"  rate limited, waiting {RATE_WAIT}s…")
            time.sleep(RATE_WAIT)
    print(f"  result: {url}")

    raw = ROOT / "_poster_raw.png"
    download(url, raw)
    print(f"  downloaded raw ({raw.stat().st_size // 1024} KB)")

    add_title(raw, OUT)
    raw.unlink()


if __name__ == "__main__":
    main()
