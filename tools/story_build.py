#!/usr/bin/env python3
"""STORY CLIP builder (owner 2026-11-27, ref x.com/toastergta/status/2126279048179707967 = 2.0M views / 25K likes /
7.8K bookmarks for the SAME SWAT-stash scene our 29 s band version did 1.1K with).

Turns a 16:9 own-gameplay capture into a FULL-SCREEN 9:16 "story" clip:
  * every segment = a 9:16 crop of the 16:9 frame (no band, no blur bars), optional punch-in zoom + cinematic
    letterbox bars for the close-ups, optional pan (x -> x_end) during the segment;
  * original game audio only (NPC/radio dialogue tells the story) - no music, no AI voice;
  * short hook line in a dark translucent rounded box (TikTok 'classic' look) for the first seconds;
  * ONE-WORD subtitles of the in-game dialogue (Scribe timings), big white bold with shadow, middle-lower;
  * optional red arrow(s) pointing at the thing to watch;
  * faint channel watermark + tiny credit bottom-left.

Usage: python3 tools/story_build.py media/configs/<name>.json
config:
{
 "src": "media/raw/clips/x.mp4",                 # 16:9 capture (owner's own gameplay)
 "segments": [ {"a": 3.0, "b": 25.0, "x": 0.5},   # x = horizontal centre of the 9:16 crop (0..1)
               {"a": 31.0, "b": 70.0, "x": 0.42, "zoom": 1.7, "y": 0.45, "bars": true, "x_end": 0.55} ],
 "hook": {"lines": ["It's free money", "at this point"], "emoji": "😭", "secs": 5.0},
 "arrows": [ {"t": [11.5, 13.5], "x": 640, "y": 600, "angle": 225} ],   # output px, angle = direction the arrow points
 "words": "auto" | "path/words.json" | null,     # auto = Scribe on the cut audio (tools/eleven.py)
 "word_y": 1180, "word_size": 92, "skip_words": ["[sirens"],
 "watermark": "ne0nleonida", "credit": "",
 "fps": 60, "out": "media/edits/<date>_story_<slug>.mp4"
}
"""
import json, os, subprocess, sys, tempfile, math
from PIL import Image, ImageDraw, ImageFont

C = json.load(open(sys.argv[1]))
W, H = 1080, 1920
FB = "brand/fonts/TikTokSans-800.ttf"; FM = "brand/fonts/TikTokSans-700.ttf"
EMO = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"
tmp = tempfile.mkdtemp(prefix="story_")
fps = C.get("fps", 60)


def run(*a):
    subprocess.run(list(a), check=True)


def probe(path, entry):
    return subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                    f"stream={entry}", "-of", "csv=p=0", path]).decode().strip()


sw, sh = [int(v) for v in probe(C["src"], "width,height").split(",")]

# 1) segments -> 1080x1920 clips
lst = os.path.join(tmp, "list.txt"); t_out = 0.0; seg_times = []
with open(lst, "w") as L:
    for i, s in enumerate(C["segments"]):
        z = s.get("zoom", 1.0); dur = s["b"] - s["a"]
        ch = sh / z; cw = ch * 9 / 16
        if cw > sw:                        # very wide zoom-out not possible -> clamp
            cw = sw; ch = cw * 16 / 9
        y0 = min(max(s.get("y", 0.5) * sh - ch / 2, 0), sh - ch)
        x1 = s.get("x", 0.5); x2 = s.get("x_end", x1)
        xa = f"min(max(({x1}+({x2}-{x1})*t/{dur:.3f})*{sw}-{cw:.1f}/2,0),{sw - cw:.1f})"
        vf = [f"crop={cw:.0f}:{ch:.0f}:'{xa}':{y0:.0f}", f"scale={W}:{H}:flags=lanczos", f"fps={fps}"]
        if s.get("bars"):                  # cinematic letterbox for punch-in close-ups
            bh = s.get("bar_h", 210)
            vf.append(f"drawbox=x=0:y=0:w={W}:h={bh}:color=black:t=fill,drawbox=x=0:y={H - bh}:w={W}:h={bh}:color=black:t=fill")
        if s.get("gamma"):
            vf.append(f"eq=gamma={s['gamma']}")
        out = os.path.join(tmp, f"s{i:02d}.mp4")
        run("ffmpeg", "-v", "error", "-y", "-ss", str(s["a"]), "-i", C["src"], "-t", f"{dur:.3f}", "-vf", ",".join(vf),
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "15", "-c:a", "aac", "-ar", "48000", "-ac", "2", "-b:a", "192k", out)
        L.write(f"file '{out}'\n"); seg_times.append((t_out, t_out + dur)); t_out += dur
joined = os.path.join(tmp, "joined.mp4")
run("ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", joined)
dur = t_out

# 2) word timings of the in-game dialogue
words = C.get("words")
if words == "auto":
    mp3 = os.path.join(tmp, "a.mp3"); wj = os.path.splitext(C["out"])[0] + "_words.json"
    run("ffmpeg", "-v", "error", "-y", "-i", joined, "-vn", "-ac", "1", "-b:a", "96k", mp3)
    run("python3", "tools/eleven.py", "scribe", mp3, wj)
    words = json.load(open(wj))
elif isinstance(words, str):
    words = json.load(open(words))
words = words or []
skip = tuple(C.get("skip_words", []))
words = [w for w in words if not w[0].startswith("[") and not w[0].endswith("]") and not w[0].startswith(skip)]


def esc(t):
    return t.replace("\\", "\\\\").replace(":", "\\:").replace("'", "’").replace(",", "\\,").replace("%", "\\%")


# 3) overlay PNGs
ov = []   # (png, x, y, t0, t1)
Hk = C.get("hook")
if Hk:
    f = ImageFont.truetype(FM, Hk.get("size", 84)); lines = Hk["lines"]
    em = None
    if Hk.get("emoji"):
        e = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
        ImageDraw.Draw(e).text((0, 0), Hk["emoji"], font=ImageFont.truetype(EMO, 109), embedded_color=True)
        em = e.crop(e.getbbox()).resize((int(f.size * 1.05), int(f.size * 1.05)))
    lw = [f.getlength(l) + (em.width + 14 if (em and k == len(lines) - 1) else 0) for k, l in enumerate(lines)]
    pad, lh = 34, int(f.size * 1.25)
    bw, bh = int(max(lw) + 2 * pad), int(lh * len(lines) + 2 * pad - (lh - f.size) * 0.6)
    img = Image.new("RGBA", (bw, bh), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, bw - 1, bh - 1), 26, fill=(28, 28, 30, 175))
    y = pad - 4
    for k, l in enumerate(lines):
        x = (bw - lw[k]) / 2
        d.text((x, y), l, font=f, fill=(255, 255, 255))
        if em and k == len(lines) - 1:
            img.alpha_composite(em, (int(x + f.getlength(l) + 14), int(y + f.size * 0.05)))
        y += lh
    p = os.path.join(tmp, "hook.png"); img.save(p)
    ov.append((p, (W - bw) // 2, Hk.get("y", 300), 0.0, Hk.get("secs", 5.0)))

for k, a in enumerate(C.get("arrows", [])):
    L_ = 150; img = Image.new("RGBA", (L_ * 2, L_ * 2), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    cx = cy = L_; ang = math.radians(a.get("angle", 225))
    tip = (cx + math.cos(ang) * L_ * 0.95, cy + math.sin(ang) * L_ * 0.95)
    tail = (cx - math.cos(ang) * L_ * 0.55, cy - math.sin(ang) * L_ * 0.55)
    d.line([tail, tip], fill=(0, 0, 0, 200), width=40); d.line([tail, tip], fill=(232, 20, 20, 255), width=28)
    for side in (1, -1):
        wing = (tip[0] - math.cos(ang + side * 0.5) * 70, tip[1] - math.sin(ang + side * 0.5) * 70)
        d.polygon([tip, wing, (tip[0] - math.cos(ang) * 40, tip[1] - math.sin(ang) * 40)], fill=(232, 20, 20, 255),
                  outline=(0, 0, 0, 200))
    p = os.path.join(tmp, f"arrow{k}.png"); img.save(p)
    ov.append((p, int(a["x"] - tip[0]), int(a["y"] - tip[1]), a["t"][0], a["t"][1]))

# 4) filter graph
dr = []
ws, wy = C.get("word_size", 104), C.get("word_y", 1200)
for i, (w, s, e) in enumerate(words):
    e2 = words[i + 1][1] if i + 1 < len(words) else e + 0.4
    e2 = min(e2, e + 0.6)
    t = w.strip()
    dr.append(f"drawtext=fontfile={FB}:text='{esc(t)}':fontsize={ws}:fontcolor=white:borderw=5:bordercolor=black@0.55:"
              f"shadowx=0:shadowy=6:shadowcolor=black@0.6:x=(w-tw)/2:y={wy}-ascent:enable='between(t,{s:.3f},{e2:.3f})'")
if C.get("watermark"):
    dr.append(f"drawtext=fontfile={FM}:text='{esc(C['watermark'])}':fontsize=34:fontcolor=white@0.28:"
              f"x=(w-tw)/2+120:y={C.get('watermark_y', 1020)}")
if C.get("credit"):
    dr.append(f"drawtext=fontfile={FM}:text='{esc(C['credit'])}':fontsize=20:fontcolor=white@0.6:borderw=1:"
              f"bordercolor=black@0.6:x=24:y=h-44")
fg = [f"[0:v]{','.join(dr) if dr else 'null'}[v0]"]; cur = "v0"; inputs = ["-i", joined]
for k, (p, x, y, t0, t1) in enumerate(ov):
    inputs += ["-loop", "1", "-i", p]
    fg.append(f"[{cur}][{k + 1}:v]overlay={x}:{y}:shortest=1:enable='between(t,{t0:.2f},{t1:.2f})'[o{k}]"); cur = f"o{k}"
fg.append("[0:a]loudnorm=I=-14:TP=-1.5:LRA=9[aout]")
run("ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(fg), "-map", f"[{cur}]", "-map", "[aout]",
    "-t", f"{dur:.2f}", "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-r", str(fps),
    "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", C["out"])
print("ok", C["out"], f"{dur:.1f}s", len(words), "words")
