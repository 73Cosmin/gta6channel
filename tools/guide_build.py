#!/usr/bin/env python3
"""Secret-guide video builder (1deflay style, playbook 'SECRET-GUIDE VIDEOS').

  python3 tools/guide_build.py media/configs/<name>.json

Every VO sentence gets its own footage cut (step-synced, unlike info_build's equal shots).
Layout: blurred full-screen fill + sharp 16:9 band (y 656-1264), ONE-WORD white captions in the
upper third (inside the TikTok safe zone), credit + disclaimer at y~1480, optional quiet music bed.

config:
{
  "footage": "media/raw/yt/n7/n7.mp4",
  "vo": "media/raw/yt/n7/vo.mp3",
  "words": "media/raw/yt/n7/vo_words.json",     # Scribe [[word,start,end],...] or inline list
  "cuts": [[0.0, 72.0], [4.0, 84.5], ...],      # [vo_time, source_start]; runs until the next cut
  "red_words": ["VICTIM"],                      # optional highlight colour words
  "caption_y": 470,
  "music": "media/music/synthwave_trap_02.mp3", "music_vol": 0.05,   # optional
  "credit": "Footage: @gameranxTV (YouTube)",
  "tail": 0.5,
  "out": "media/edits/x.mp4"
}
"""
import json, subprocess, sys
from PIL import ImageFont

C = json.load(open(sys.argv[1]))
F = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
TT = "brand/fonts/TikTokSans-700.ttf"
vo = C["vo"]
dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                     "-of", "csv=p=0", vo]).decode()) + C.get("tail", 0.5)
W = C["words"]
if isinstance(W, str):
    W = json.load(open(W))


def esc(t):
    return (t.replace("\\", "\\\\").replace(":", "\\:").replace("'", "’")
             .replace(",", "\\,").replace("%", "\\%"))


cuts = C["cuts"]
# pre-cut each segment separately (14 trims on one 1080p input ran out of memory), then concat
import os, tempfile
tmp = tempfile.mkdtemp(prefix="guide_")
lst = os.path.join(tmp, "list.txt")
with open(lst, "w") as L:
    for i, (vt, src, *opt) in enumerate(cuts):
        end = cuts[i + 1][0] if i + 1 < len(cuts) else dur
        g = opt[0] if opt else C.get("gamma", 1.0)          # owner 2026-11-26: no dark openings
        seg = os.path.join(tmp, f"s{i:02d}.mp4")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(src), "-i", C["footage"], "-t", f"{end - vt:.3f}",
                        "-an", "-vf", f"fps=30,scale=1920:1080,eq=gamma={g}:saturation={1.0 + (g - 1) * 0.3:.2f}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16",
                        seg], check=True)
        L.write(f"file '{seg}'\n")
joined = os.path.join(tmp, "joined.mp4")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", joined], check=True)
C["footage"] = joined
f = ["[0:v]setpts=PTS-STARTPTS,split[a][b]"]
f.append("[a]scale=-2:2400,crop=1080:1920,boxblur=22:2,eq=brightness=-0.08:saturation=1.3[bg]")
f.append("[b]scale=1080:608:force_original_aspect_ratio=increase,crop=1080:608,"
         "eq=contrast=1.06:saturation=1.12[fg]")
f.append("[bg][fg]overlay=0:656[v0]")

dr = []
# Title box (owner 2026-11-26, ALL videos): black bold TikTok Sans on white rounded boxes ABOVE the band,
# says what the video is about. "title_until": null = whole video (word captions then go below the band).
from PIL import Image, ImageDraw
title_png = None
if C.get("title"):
    lines = C["title"]; size = C.get("title_size", 78)
    while size > 40 and max(ImageFont.truetype(TT, size).getlength(l) for l in lines) + 56 > 740:
        size -= 2
    ft = ImageFont.truetype(TT, size); padx, lh = 26, int(size * 1.22)
    ws = [ft.getlength(l) for l in lines]
    Wb = int(max(ws) + 2 * padx + 8); Hb = lh * len(lines) + 16
    im = Image.new("RGBA", (Wb, Hb), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for k, wl in enumerate(ws):
        x0 = (Wb - wl) / 2 - padx; y0 = 8 + k * lh
        d.rounded_rectangle([x0, y0, x0 + wl + 2 * padx, y0 + lh], radius=int(size * 0.22), fill=(255, 255, 255, 255))
    for k, (l, wl) in enumerate(zip(lines, ws)):
        d.text(((Wb - wl) / 2, 8 + k * lh + lh / 2), l, font=ft, fill=(0, 0, 0, 255), anchor="lm")
    title_png = os.path.join(tmp, "title.png"); im.save(title_png)
    title_xy = ((1080 - Wb) // 2, 656 - Hb - 24)
TU = C.get("title_until")
red = set(C.get("red_words", []))
cy = C.get("caption_y", 1390 if (title_png and TU is None) else 470)
for i, (w, st, en) in enumerate(W):
    nxt = W[i + 1][1] if i + 1 < len(W) else dur
    e = min(nxt, en + 0.5)
    c = w.strip(".,!?").upper()
    col = "0xFF2A2A" if c in red else "white"
    cs = 104
    while cs > 50 and ImageFont.truetype(TT, cs).getlength(c) + 20 > 700:
        cs -= 4
    dr.append(f"drawtext=fontfile={TT}:text='{esc(c)}':fontsize={cs}:fontcolor={col}:borderw=8:bordercolor=black:"
              f"shadowx=0:shadowy=6:shadowcolor=black@0.6:x=(w-tw)/2:y={cy}-th/2:"
              f"enable='gte(t,{st})*lt(t,{e:.3f})" + (f"*gte(t,{TU})" if (title_png and TU and cy < 656) else "") + "'")
if C.get("credit"):   # tiny bottom-left (owner 2026-11-26: no disclaimer line)
    dr.append(f"drawtext=fontfile={F}:text='{esc(C['credit'])}':fontsize=20:fontcolor=white@0.6:borderw=1:"
              f"bordercolor=black@0.6:x=24:y=h-44")
f.append("[v0]" + ",".join(dr) + "[v1]")

inputs = ["-i", C["footage"], "-i", vo]
cur = "v1"
if title_png:
    inputs_t = ["-loop", "1", "-i", title_png]
    ti = 3 if C.get("music") else 2
    en = f":enable='lt(t,{TU})'" if TU else ""
    f.append(f"[v1][{ti}:v]overlay={title_xy[0]}:{title_xy[1]}:shortest=0{en}[vt]"); cur = "vt"
f.append(f"[1:a]aformat=sample_rates=44100:channel_layouts=stereo,apad=whole_dur={dur:.2f},asplit[vo1][vo2]")
if C.get("music"):
    inputs += ["-stream_loop", "-1", "-i", C["music"]]
    f.append(f"[2:a]aformat=sample_rates=44100:channel_layouts=stereo,volume={C.get('music_vol', 0.05)},"
             f"afade=t=out:st={dur - 0.8:.2f}:d=0.8[mu]")
    f.append("[mu][vo1]sidechaincompress=threshold=0.04:ratio=6:attack=20:release=300[duck]")
    f.append("[vo2][duck]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=7[aout]")
else:
    f.append("[vo1]anullsink;[vo2]loudnorm=I=-14:TP=-1.5:LRA=7[aout]")
if title_png:
    inputs += inputs_t
cmd = ["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(f), "-map", f"[{cur}]",
       "-map", "[aout]", "-t", f"{dur:.2f}", "-c:v", "libx264", "-preset", "medium", "-crf", "21",
       "-pix_fmt", "yuv420p", "-r", "30", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", C["out"]]
subprocess.run(cmd, check=True)
print("ok", C["out"], f"{dur:.2f}s")
