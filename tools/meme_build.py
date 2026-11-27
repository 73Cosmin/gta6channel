#!/usr/bin/env python3
"""Meme builder (owner's humor refs, 2026-11-18): full-screen 9:16 scene + white TikTok pill caption.

Usage: /tmp/venv/bin/python tools/meme_build.py media/configs/<name>.json

Config keys:
  clips:   [{"src": path, "start": 0, "dur": 5, "speed": 1.0, "reverse": false, "zoom": 1.0}]  played in order
  caption: main caption, "\n" for line breaks, emoji allowed (shown whole video unless "caption_until")
  caption_y: centre of caption as fraction of height (default 0.20)
  pops:    [{"text": "...", "t": 3.0, "until": null, "y": 0.62}]  extra captions that appear later (punchline)
  music:   path to mp3, "music_start": seconds offset, "music_vol": 1.0
  sfx:     [{"src": path, "t": 2.0, "vol": 1.0}] optional
  footer:  small disclaimer line at bottom (default: AI-generated scene + fan page line)
  credit:  optional extra small line above footer (e.g. "🎥 @creator" or "Footage: Rockstar Games")
  out:     output mp4 path
"""
import json, os, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
TXT = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"
EMO = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"
DEFAULT_FOOTER = "AI-generated scene"   # owner 2026-11-26: no fan-page/not-affiliated line


def is_emoji(ch):
    o = ord(ch)
    return o >= 0x1F000 or 0x2600 <= o <= 0x27BF or o in (0xFE0F, 0x200D)


def runs(line):
    out, cur, emo = [], "", None
    for ch in line:
        e = is_emoji(ch)
        if emo is None or e == emo:
            cur += ch
        else:
            out.append((cur, emo)); cur = ch
        emo = e
    if cur:
        out.append((cur, emo))
    return out


def render_line(line, size):
    """Render one line (text + colour emoji) as RGBA, black text on transparent."""
    f = ImageFont.truetype(TXT, size)
    ef = ImageFont.truetype(EMO, 109)
    parts = []
    for seg, emo in runs(line):
        if emo:
            for ch in seg:
                if ch in ("️", "‍"):
                    continue
                im = Image.new("RGBA", (140, 140), (0, 0, 0, 0))
                ImageDraw.Draw(im).text((0, 0), ch, font=ef, embedded_color=True)
                im = im.crop(im.getbbox() or (0, 0, 1, 1))
                s = int(size * 1.05)
                im = im.resize((int(im.width * s / im.height), s), Image.LANCZOS)
                parts.append((im, int(size * 0.12)))
        else:
            l, t, r, b = f.getbbox(seg)
            im = Image.new("RGBA", (r + 4, int(size * 1.25)), (0, 0, 0, 0))
            ImageDraw.Draw(im).text((0, int(size * 0.05)), seg, font=f, fill=(0, 0, 0, 255))
            parts.append((im, 0))
    w = sum(p.width for p, _ in parts) + 6 * max(0, len(parts) - 1)
    h = int(size * 1.3)
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    x = 0
    for im, dy in parts:
        out.alpha_composite(im, (x, max(0, (h - im.height) // 2 + (0 if dy == 0 else -2))))
        x += im.width + 6
    return out


def pill(text, y_frac, size=62, path=None):
    """TikTok-style caption: each line on its own white rounded box, boxes merged, centred."""
    lines = [render_line(l, size) for l in text.split("\n")]
    padx, pady, rad = 26, 8, 22
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    total_h = sum(l.height + 2 * pady for l in lines)
    y = int(H * y_frac - total_h / 2)
    d = ImageDraw.Draw(canvas)
    boxes = []
    for l in lines:
        bw, bh = l.width + 2 * padx, l.height + 2 * pady
        x = (W - bw) // 2
        boxes.append((x, y, x + bw, y + bh, l))
        y += bh
    for x0, y0, x1, y1, _ in boxes:
        d.rounded_rectangle((x0, y0, x1, y1), radius=rad, fill=(255, 255, 255, 255))
    for x0, y0, x1, y1, l in boxes:
        canvas.alpha_composite(l, (x0 + padx, y0 + pady))
    canvas.save(path)


def small_lines(lines, path):
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(canvas)
    f = ImageFont.truetype(TXT, 26)
    y = H - 70 - 36 * (len(lines) - 1)
    for ln in lines:
        w = d.textlength(ln, font=f)
        d.text(((W - w) / 2, y), ln, font=f, fill=(255, 255, 255, 230), stroke_width=3, stroke_fill=(0, 0, 0, 200))
        y += 36
    canvas.save(path)


def main(cfg_path):
    C = json.load(open(cfg_path))
    tmp = tempfile.mkdtemp()
    # 1) video segments -> 1080x1920 cover-crop
    segs = []
    for i, c in enumerate(C["clips"]):
        z = c.get("zoom", 1.0)
        vf = (f"scale={int(W*z)}:{int(H*z)}:force_original_aspect_ratio=increase,crop={W}:{H},"
              f"setsar=1,fps=30")
        if c.get("reverse"):
            vf += ",reverse"
        sp = c.get("speed", 1.0)
        if sp != 1.0:
            vf += f",setpts=PTS/{sp}"
        o = f"{tmp}/s{i}.mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(c.get("start", 0)), "-t", str(c["dur"]),
                        "-i", c["src"], "-an", "-vf", vf, "-c:v", "libx264", "-crf", "16", "-preset", "fast", o],
                       check=True)
        segs.append(o)
    lst = f"{tmp}/l.txt"
    open(lst, "w").write("".join(f"file '{s}'\n" for s in segs))
    base = f"{tmp}/base.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", base], check=True)
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                         "-of", "csv=p=0", base]).decode())
    # 2) overlays
    ovs = []
    cap = f"{tmp}/cap.png"
    pill(C["caption"], C.get("caption_y", 0.20), C.get("caption_size", 62), cap)
    ovs.append((cap, 0, C.get("caption_until", dur)))
    for j, p in enumerate(C.get("pops", [])):
        pp = f"{tmp}/pop{j}.png"
        pill(p["text"], p.get("y", 0.62), p.get("size", 62), pp)
        ovs.append((pp, p["t"], p.get("until") or dur))
    foot = f"{tmp}/foot.png"
    small_lines([l for l in [C.get("credit"), C.get("footer", DEFAULT_FOOTER)] if l], foot)
    ovs.append((foot, 0, dur))
    # 3) compose
    cmd = ["ffmpeg", "-v", "error", "-y", "-i", base]
    for o, _, _ in ovs:
        cmd += ["-i", o]
    music = C.get("music")
    cmd += ["-ss", str(C.get("music_start", 0)), "-i", music]
    sfx = C.get("sfx", [])
    for s in sfx:
        cmd += ["-i", s["src"]]
    fc, last = [], "0:v"
    for k, (_, t0, t1) in enumerate(ovs, start=1):
        fc.append(f"[{last}][{k}:v]overlay=0:0:enable='between(t,{t0},{t1})'[v{k}]")
        last = f"v{k}"
    mi = len(ovs) + 1
    fc.append(f"[{mi}:a]atrim=0:{dur},asetpts=PTS-STARTPTS,volume={C.get('music_vol',1.0)},"
              f"afade=t=out:st={max(0,dur-1.2)}:d=1.2[m]")
    amix = ["[m]"]
    for n, s in enumerate(sfx):
        idx = mi + 1 + n
        ms = int(s["t"] * 1000)
        fc.append(f"[{idx}:a]adelay={ms}|{ms},volume={s.get('vol',1.0)}[x{n}]")
        amix.append(f"[x{n}]")
    fc.append(f"{''.join(amix)}amix=inputs={len(amix)}:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11,"
              f"aresample=44100[a]")
    cmd += ["-filter_complex", ";".join(fc), "-map", f"[{last}]", "-map", "[a]", "-t", str(dur),
            "-c:v", "libx264", "-crf", "16", "-preset", "slow", "-profile:v", "high", "-maxrate", "16M", "-bufsize", "32M", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", C["out"]]
    subprocess.run(cmd, check=True)
    print("built", C["out"], f"{dur:.1f}s")


if __name__ == "__main__":
    main(sys.argv[1])
