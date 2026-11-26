#!/usr/bin/env python3
"""Guide video builder v2 (owner 2026-11-26, refs @gta6_deutschland).

  python3 tools/guide_build_v2.py media/configs/<name>.json

Layout: gameplay ZOOMED to nearly full screen (band 1080x1500 at y 210, blurred fill above/below),
GTA VI logo top centre below the TikTok search bar, 2-3-word captions (Poppins ExtraBold, white,
one key word yellow, soft shadow) in the lower middle, NO black/white title boxes.
Hook: VO "This is how you get <X>" + a picture card of the item that SLIDES IN from the side
(rounded, white border, item label pill below) with a swoosh, then slides out; then the walkthrough.

config:
{
 "footage": "...mp4", "vo": "...mp3", "words": "...json",
 "cuts": [[vo_t, src_t, gamma?, xfocus?], ...],   # xfocus 0..1 = which part of the 16:9 frame stays in the crop
 "hook": {"img_t": 36.9, "img_gamma": 1.0, "label": "PROGEN ROYAL RUBY EMERUS", "in": 0.3, "out": 4.6,
          "from": "right"},                        # right|left|top|bottom
 "yellow_words": ["EMERUS"], "music": "...", "music_vol": 0.05,
 "credit": "Footage: @x (YouTube)", "tail": 0.8, "out": "media/edits/....mp4"
}
"""
import json, os, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter

C = json.load(open(sys.argv[1]))
PF = "brand/fonts/Poppins-ExtraBold.ttf"
DJ = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
LOGO = C.get("logo", "brand/logo/gta6_logo.png")
BAND_Y, BAND_H = 210, 1500
vo = C["vo"]
dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                     "-of", "csv=p=0", vo]).decode()) + C.get("tail", 0.5)
W = C["words"]
if isinstance(W, str):
    W = json.load(open(W))
W = [[("6" if w.strip(".,!?") == "VI" else w), s, e] for w, s, e in W]
tmp = tempfile.mkdtemp(prefix="guide2_")


def esc(t):
    return (t.replace("\\", "\\\\").replace(":", "\\:").replace("'", "’")
             .replace(",", "\\,").replace("%", "\\%"))


# 0) JUMP-CUT GUARD (owner 2026-11-26: "komische Jumpcuts ganz random" in the Emerus guide -> never again).
# A jump cut = the picture skips a little inside the SAME shot (same place, slightly moved) -> looks like a glitch.
# For every cut: cont = where the previous segment would continue, src = where the new cut starts.
#  1. |src - cont| < 2.0 s            -> MERGE: drop the cut, the footage just keeps playing (no skip at all).
#  2. junction frames look alike      -> DISSOLVE: 0.3 s crossfade from the previous segment's last frame, so a
#     (mean gray diff 0.01-0.16)         time skip inside one shot reads as an intended "later..." transition.
#  3. clearly different picture       -> normal hard cut (that is a real cut, fine).
# Identical frames (diff < 0.01, e.g. a static map screen) need nothing.
import numpy as np


def gray(t):
    b = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{max(t, 0):.3f}", "-i", C["footage"], "-frames:v", "1",
                        "-vf", "scale=64:36,format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
    return np.frombuffer(b, np.uint8).astype(float) if len(b) == 64 * 36 else None


cuts = [list(c) for c in C["cuts"]]
merged, dissolve = [cuts[0]], set()
for i, cut in enumerate(cuts[1:], 1):
    pv = merged[-1]; cont = pv[1] + (cut[0] - pv[0]); src = cut[1]
    if abs(src - cont) < 2.0 and i not in C.get("keep_cut", []):
        print(f"jumpcut guard: cut {i} at vo {cut[0]:.2f}s merged (src {src:.2f} vs continuous {cont:.2f})")
        continue
    a, b = gray(cont - 0.05), gray(src)
    d = abs(a - b).mean() / 255 if a is not None and b is not None else 1.0
    if 0.01 <= d < C.get("dissolve_below", 0.16):
        dissolve.add(len(merged))
        print(f"jumpcut guard: cut {i} at vo {cut[0]:.2f}s same-looking shot (diff {d:.3f}) -> 0.3 s dissolve")
    merged.append(cut)

# 1) segments: zoomed crop 1080x1500 per cut
cuts = merged
lst = os.path.join(tmp, "list.txt")
bw = int(round(BAND_H * 16 / 9 / 2)) * 2
with open(lst, "w") as L:
    for i, cut in enumerate(cuts):
        vt, src = cut[0], cut[1]
        g = cut[2] if len(cut) > 2 and cut[2] else C.get("gamma", 1.0)
        xf = cut[3] if len(cut) > 3 else 0.5
        end = cuts[i + 1][0] if i + 1 < len(cuts) else dur
        seg = os.path.join(tmp, f"s{i:02d}.mp4")
        x = int((bw - 1080) * xf)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(src), "-i", C["footage"], "-t", f"{end - vt:.3f}", "-an",
                        "-vf", f"fps=30,scale={bw}:{BAND_H},crop=1080:{BAND_H}:{x}:0,"
                               f"eq=gamma={g}:contrast=1.05:saturation={1.1 + (g - 1) * 0.3:.2f}",
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", seg], check=True)
        if i in dissolve:      # crossfade from the previous segment's last frame (no timing change)
            prev = os.path.join(tmp, f"s{i - 1:02d}.mp4"); last = os.path.join(tmp, f"last{i:02d}.png")
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-sseof", "-0.1", "-i", prev, "-frames:v", "1", last], check=True)
            seg2 = os.path.join(tmp, f"s{i:02d}x.mp4")
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", seg, "-loop", "1", "-i", last, "-filter_complex",
                            "[1:v]format=rgba,fade=t=out:st=0:d=0.3:alpha=1[o];[0:v][o]overlay=shortest=1",
                            "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-r", "30", seg2], check=True)
            seg = seg2
        L.write(f"file '{seg}'\n")
joined = os.path.join(tmp, "joined.mp4")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", joined], check=True)

# 2) overlays as PNGs
logo = Image.open(LOGO).convert("RGBA")
lw = C.get("logo_w", 250); logo = logo.resize((lw, int(logo.height * lw / logo.width)))
sh = Image.new("RGBA", (logo.width + 40, logo.height + 40), (0, 0, 0, 0))
sh.paste((0, 0, 0, 150), (20, 26), logo.split()[3]); sh = sh.filter(ImageFilter.GaussianBlur(8))
sh.alpha_composite(logo, (20, 20)); logo_png = os.path.join(tmp, "logo.png"); sh.save(logo_png)
logo_xy = ((1080 - sh.width) // 2, C.get("logo_y", 232))

H = C.get("hook")
if H:
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(H["img_t"]), "-i", C["footage"], "-frames:v", "1",
                    os.path.join(tmp, "hook.png")], check=True)
    im = Image.open(os.path.join(tmp, "hook.png")).convert("RGB")
    im = ImageEnhance.Brightness(im).enhance(H.get("img_gamma", 1.0))
    cw = H.get("w", 900); ch = int(cw * 9 / 16)
    if H.get("crop"):           # [x0,y0,x1,y1] in source pixels
        im = im.crop(tuple(H["crop"]))
    s = max(cw / im.width, ch / im.height); im = im.resize((int(im.width * s) + 1, int(im.height * s) + 1))
    im = im.crop(((im.width - cw) // 2, (im.height - ch) // 2, (im.width - cw) // 2 + cw, (im.height - ch) // 2 + ch))
    bd = 8; lab = H.get("label", ""); fl = ImageFont.truetype(PF, 44)
    lab_h = 92 if lab else 0
    card = Image.new("RGBA", (cw + 2 * bd + 40, ch + 2 * bd + lab_h + 60), (0, 0, 0, 0))
    shadow = Image.new("RGBA", card.size, (0, 0, 0, 0)); d = ImageDraw.Draw(shadow)
    d.rounded_rectangle((20, 28, 20 + cw + 2 * bd, 28 + ch + 2 * bd), 34, fill=(0, 0, 0, 170))
    card.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(12)))
    d = ImageDraw.Draw(card)
    d.rounded_rectangle((20, 20, 20 + cw + 2 * bd, 20 + ch + 2 * bd), 34, fill=(255, 255, 255, 255))
    m = Image.new("L", (cw, ch), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, cw, ch), 28, fill=255)
    card.paste(im, (20 + bd, 20 + bd), m)
    if lab:
        while fl.getlength(lab) > cw - 60:
            fl = ImageFont.truetype(PF, fl.size - 2)
        tw = fl.getlength(lab); x0 = (card.width - tw) / 2 - 30; y0 = 20 + ch + 2 * bd + 18
        d.rounded_rectangle((x0, y0, x0 + tw + 60, y0 + 70), 35, fill=(18, 14, 30, 235), outline=(255, 70, 170), width=4)
        d.text((card.width / 2, y0 + 35), lab, font=fl, fill=(255, 255, 255), anchor="mm")
    hook_png = os.path.join(tmp, "card.png"); card.save(hook_png)
    hx = (1080 - card.width) // 2; hy = C.get("hook_y", 960) - card.height // 2

# 3) filter graph
f = ["[0:v]setpts=PTS-STARTPTS,split[a][b]",
     "[a]scale=1382:1920,crop=1080:1920,boxblur=24:2,eq=brightness=-0.1[bg]",
     f"[bg][b]overlay=0:{BAND_Y}[v0]"]
dr = []
# captions: chunks of 2-3 words, one key word yellow
yel = set(w.upper() for w in C.get("yellow_words", []))
chunks, cur = [], []
for w in W:
    cur.append(w)
    txt = " ".join(x[0] for x in cur)
    if w[0].endswith((".", "?", "!", ",")) or len(cur) >= 3 or len(txt) >= 14:
        chunks.append(cur); cur = []
if cur:
    chunks.append(cur)
fs = C.get("caption_size", 66); cy = C.get("caption_y", 1290)
font = ImageFont.truetype(PF, fs)
for i, ch_ in enumerate(chunks):
    st = ch_[0][1]; en = chunks[i + 1][0][1] if i + 1 < len(chunks) else dur
    words = [x[0].strip(",") for x in ch_]
    words = [w.rstrip(".") if not w.endswith("..") else w for w in words]
    clean = [w.strip(".,!?").upper() for w in words]
    hi = [k for k, c in enumerate(clean) if c in yel or any(ch.isdigit() for ch in c)]
    if not hi:
        cand = [k for k, c in enumerate(clean) if len(c) >= 4]
        hi = [max(cand, key=lambda k: len(clean[k]))] if cand else []
    sp = font.getlength(" "); ws = [font.getlength(w) for w in words]
    total = sum(ws) + sp * (len(words) - 1); scale = min(1.0, 900 / total)
    fsz = int(fs * scale); fnt = ImageFont.truetype(PF, fsz); sp = fnt.getlength(" ")
    ws = [fnt.getlength(w) for w in words]; total = sum(ws) + sp * (len(words) - 1)
    x = (1080 - total) / 2
    for k, w in enumerate(words):
        col = "0xFFE81F" if k in hi else "white"
        dr.append(f"drawtext=fontfile={PF}:text='{esc(w)}':fontsize={fsz}:fontcolor={col}:borderw=3:bordercolor=black@0.85:"
                  f"shadowx=0:shadowy=5:shadowcolor=black@0.55:x={x:.0f}:y={cy}-ascent:"
                  f"enable='gte(t,{st:.3f})*lt(t,{en:.3f})'")
        x += ws[k] + sp
# credit: tiny, bottom-left corner (owner 2026-11-26: no "fan page / not affiliated" line any more, source barely visible)
if C.get("credit"):
    dr.append(f"drawtext=fontfile={DJ}:text='{esc(C['credit'])}':fontsize=20:fontcolor=white@0.6:borderw=1:"
              f"bordercolor=black@0.6:x=24:y=h-44")
f.append("[v0]" + ",".join(dr) + "[v1]")

inputs = ["-i", joined, "-i", vo, "-loop", "1", "-i", logo_png]
idx = 3
f.append(f"[v1][2:v]overlay={logo_xy[0]}:{logo_xy[1]}:shortest=1[v2]"); cur = "v2"
if H:
    inputs += ["-loop", "1", "-i", hook_png]; hi_ = idx; idx += 1
    t0, t1, D = H.get("in", 0.3), H["out"], 0.38
    frm = H.get("from", "right")
    ease_in = f"pow(1-(t-{t0})/{D},3)"; ease_out = f"pow((t-{t1})/{D},3)"
    if frm in ("right", "left"):
        sgn = 1 if frm == "right" else -1
        xe = f"if(lt(t,{t0}+{D}),{hx}+{sgn}*1300*{ease_in},if(gt(t,{t1}),{hx}-{sgn}*1300*{ease_out},{hx}))"; ye = str(hy)
    else:
        sgn = 1 if frm == "bottom" else -1
        ye = f"if(lt(t,{t0}+{D}),{hy}+{sgn}*1500*{ease_in},if(gt(t,{t1}),{hy}-{sgn}*1500*{ease_out},{hy}))"; xe = str(hx)
    f.append(f"[{cur}][{hi_}:v]overlay=x='{xe}':y='{ye}':eval=frame:shortest=1:"
             f"enable='between(t,{t0},{t1}+{D})'[v3]"); cur = "v3"
f.append(f"[1:a]aformat=sample_rates=44100:channel_layouts=stereo,apad=whole_dur={dur:.2f},asplit[vo1][vo2]")
mix = ["[vo2]"]
if C.get("music"):
    inputs += ["-stream_loop", "-1", "-i", C["music"]]; mi = idx; idx += 1
    f.append(f"[{mi}:a]aformat=sample_rates=44100:channel_layouts=stereo,volume={C.get('music_vol', 0.05)},"
             f"afade=t=out:st={dur - 0.8:.2f}:d=0.8[mu]")
    f.append("[mu][vo1]sidechaincompress=threshold=0.04:ratio=6:attack=20:release=300[duck]"); mix.append("[duck]")
else:
    f.append("[vo1]anullsink")
if H:
    sw = C.get("swoosh", "media/music/swoosh.wav")
    for k, (tt, vol) in enumerate([(H.get("in", 0.3), C.get("swoosh_vol", 0.7)), (H["out"], C.get("swoosh_vol", 0.7) * 0.55)]):
        inputs += ["-i", sw]; si = idx; idx += 1
        f.append(f"[{si}:a]aformat=sample_rates=44100:channel_layouts=stereo,volume={vol},adelay={int(tt * 1000)}:all=1[sw{k}]")
        mix.append(f"[sw{k}]")
f.append("".join(mix) + f"amix=inputs={len(mix)}:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=7[aout]")
cmd = ["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(f), "-map", f"[{cur}]",
       "-map", "[aout]", "-t", f"{dur:.2f}", "-c:v", "libx264", "-preset", "medium", "-crf", "21",
       "-pix_fmt", "yuv420p", "-r", "30", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", C["out"]]
subprocess.run(cmd, check=True)
print("ok", C["out"], f"{dur:.2f}s")
