"""Channel watermark for ALL videos + slideshows (owner 2026-11-28: 'in allen zukuenftigen Slideshows und Videos ein
Watermark von meinem Account - nicht stoerend, aber gut sichtbar').

Look: '@ne0nleonida' in TikTok Sans 800, white on a dark translucent pill with a small teal dot.
  * videos: top-left inside the TikTok safe zone (x 130, y ~258, just under the search bar), whole video.
  * slides: placed by each builder in a free spot (footer centre / top centre), same pill.
Usage:
  from brandmark import video_mark, slide_mark      (sys.path has tools/ when a builder runs as tools/x.py)
  dr.append(video_mark())                            # ffmpeg drawtext chain element (no leading comma)
  slide_mark(im, cx, cy)                             # PIL RGB/RGBA image, centre point
"""
from PIL import Image, ImageDraw, ImageFont

HANDLE = "@ne0nleonida"
FONT = "brand/fonts/TikTokSans-800.ttf"
TEAL = (94, 230, 200)


def video_mark(x=130, y=258, size=34):
    """drawtext element: white handle on a translucent dark box, top-left of the safe zone, whole video."""
    return (f"drawtext=fontfile={FONT}:text='{HANDLE}':fontsize={size}:fontcolor=white@0.88:"
            f"box=1:boxcolor=0x0E0C18@0.45:boxborderw=14:x={x}:y={y}")


def mark_png(size=28):
    """RGBA pill with teal dot + handle (used for slides and PNG overlays)."""
    f = ImageFont.truetype(FONT, size)
    tw = int(ImageDraw.Draw(Image.new("RGBA", (1, 1))).textlength(HANDLE, font=f))
    h = int(size * 1.75); dot = int(size * 0.38); pad = int(size * 0.65)
    w = pad + dot + int(size * 0.4) + tw + pad
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), h // 2, fill=(14, 12, 24, 175))
    cy = h // 2; d.ellipse((pad, cy - dot // 2, pad + dot, cy + dot // 2), fill=TEAL)
    d.text((pad + dot + int(size * 0.4), cy), HANDLE, font=f, fill=(255, 255, 255, 235), anchor="lm")
    return im


def slide_mark(im, cx, cy, size=28):
    """Paste the pill centred on (cx, cy). Works on RGB (returns same object, modified) and RGBA."""
    m = mark_png(size); x, y = int(cx - m.width / 2), int(cy - m.height / 2)
    if im.mode == "RGBA":
        im.alpha_composite(m, (x, y))
    else:
        im.paste(m, (x, y), m)
    return im
