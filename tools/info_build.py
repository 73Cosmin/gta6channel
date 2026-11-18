#!/usr/bin/env python3
"""Info-style 9:16 video: blurred bg + sharp 16:9 band, one-word yellow captions,
red arrow pop-ins, building checklist. Usage:
  info_build.py <landscape.mp4> <words.json> <vo.mp3> <out.mp4> <shot_starts comma list>
"""
import json, subprocess, sys, os
from PIL import Image, ImageDraw

src, words_p, vo, out, shots = sys.argv[1:6]
shots = [float(x) for x in shots.split(",")]
S = os.path.dirname(os.path.abspath(__file__))
F = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
words = json.load(open(words_p))
dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                     "-of", "csv=p=0", vo]).decode())

# red arrow PNG (points down-right)
arrow = os.path.join(S, "arrow.png")
im = Image.new("RGBA", (260, 260), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
pts = [(20, 60), (150, 60), (150, 20), (240, 130), (150, 240), (150, 200), (20, 200)]
d.polygon(pts, fill=(235, 20, 30, 255), outline=(255, 255, 255, 255), width=10)
im.rotate(165, resample=Image.BICUBIC, expand=True).save(arrow)

def esc(t):
    return t.replace("\\", "\\\\").replace(":", "\\:").replace("'", "’").replace(",", "\\,").replace("%", "\\%")

# shot cuts: equal length segments covering dur
n = len(shots); seg = dur / n
vparts = []
for i, s0 in enumerate(shots):
    vparts.append(f"[0:v]trim=start={s0}:duration={seg:.3f},setpts=PTS-STARTPTS[s{i}]")
concat = "".join(f"[s{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0,fps=30," + os.environ.get("PRECROP", "null") + ",split[a][b]"

f = vparts + [concat,
    "[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:3,eq=brightness=-0.18[bg]",
    "[b]scale=1080:608:force_original_aspect_ratio=increase,crop=1080:608[fg]",
    "[bg][fg]overlay=0:656[v0]"]

draw = []
PINK, CYAN, YEL = "0xFF2BD6", "0x22E6FF", "0xFFE600"
draw.append(f"drawtext=fontfile={F}:text='GTA 6':fontsize=120:fontcolor=white:borderw=7:bordercolor={PINK}:x=(w-tw)/2:y=150")
draw.append(f"drawtext=fontfile={F}:text='PLAY THE SECOND IT UNLOCKS':fontsize=58:fontcolor={CYAN}:borderw=5:bordercolor=black:x=(w-tw)/2:y=300")
# one-word captions in the middle of the band
for i, (wtxt, st, en) in enumerate(words):
    nxt = words[i + 1][1] if i + 1 < len(words) else dur
    end = min(nxt, en + 0.6)
    clean = wtxt.strip(".,").upper()
    col = "0xFF2A2A" if clean in ("ONE", "TWO", "THREE", "MIDNIGHT", "PRELOAD", "REST") else YEL
    draw.append(f"drawtext=fontfile={F}:text='{esc(clean)}':fontsize=96:fontcolor={col}:borderw=8:bordercolor=black:"
                f"x=(w-tw)/2:y=960-th/2:enable='gte(t,{st})*lt(t,{end:.3f})'")
# checklist building under the band
steps = [("1. PRELOAD NOW", "PS5 or Xbox", 3.66), ("2. REST MODE ON", "so the download finishes", 7.54),
         ("3. MIDNIGHT LOCAL", "in YOUR time zone", 11.34)]
for k, (a, b, t0) in enumerate(steps):
    y = 1310 + k * 150
    draw.append(f"drawtext=fontfile={F}:text='{esc(a)}':fontsize=60:fontcolor=white:x=90:y={y}:box=1:boxcolor=0x0A0014@0.85:boxborderw=14:enable='gte(t,{t0})'")
    draw.append(f"drawtext=fontfile={F}:text='{esc(b)}':fontsize=40:fontcolor={CYAN}:x=104:y={y+82}:enable='gte(t,{t0})'")
draw.append(f"drawtext=fontfile={F}:text='FOLLOW FOR MORE GTA 6 TIPS':fontsize=56:fontcolor=white:borderw=6:bordercolor={PINK}:x=(w-tw)/2:y=1180:enable='gte(t,14.86)'")
draw.append(f"drawtext=fontfile={F}:text='Footage\\: Rockstar Games (Trailer 2)':fontsize=26:fontcolor=white@0.85:x=(w-tw)/2:y=h-120")
draw.append(f"drawtext=fontfile={F}:text='Fan page. Not affiliated with Rockstar Games.':fontsize=26:fontcolor=white@0.85:x=(w-tw)/2:y=h-80")
f.append("[v0]" + ",".join(draw) + "[v1]")
# arrows pop in (scale bounce) pointing at the new checklist line
cur = "v1"
f.append(f"[1:v]format=rgba,scale=200:-1,split={len(steps)}" + "".join(f"[ar{k}]" for k in range(len(steps))))
for k, (_, _, t0) in enumerate(steps):
    y = 1310 + k * 150 - 40
    nxt = f"v{k+2}"
    # slide in from the right over 0.25s, stay 2.5s
    f.append(f"[{cur}][ar{k}]overlay=x='if(lt(t,{t0}+0.25),1080-(1080-860)*(t-{t0})/0.25,860)':y={y}:"
             f"enable='between(t,{t0},{t0}+2.8)'[{nxt}]")
    cur = nxt
fc = ";".join(f)
cmd = ["ffmpeg", "-v", "error", "-y", "-i", src, "-loop", "1", "-i", arrow, "-i", vo,
       "-filter_complex", fc, "-map", f"[{cur}]", "-map", "2:a", "-t", f"{dur:.2f}",
       "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-r", "30",
       "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", out]
subprocess.run(cmd, check=True)
print("ok", out)
