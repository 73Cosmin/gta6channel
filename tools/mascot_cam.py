#!/usr/bin/env python3
"""Mascot FACECAM track (owner 2026-11-27: raccoon mascot reacts like a streamer facecam, one pose per sentence).

Used by tools/guide_build_v2.py when the config has a "mascot" block; can also preview a track alone:
  python3 tools/mascot_cam.py words.json vo.mp3 out.mov        # prints the sentence -> pose plan

Poses = brand/mascot/raccoon_poses/<name>.jpg (all the same framing/room, so a switch reads as the streamer
moving, not as a scene cut). Pose per sentence: keyword rules below, first sentence = hook pose, never the same
pose twice in a row. Override per sentence index in the config: "mascot": {"poses": {"3": "shocked"}}.

config "mascot" block (all optional):
  {"dir": "brand/mascot/raccoon_poses", "x": 120, "y": 250, "w": 380, "hook_pose": "point_viewer",
   "poses": {"<sentence idx>": "<pose>"}, "live": true}
"""
import json, math, os, re, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

TEAL = (94, 230, 200)
FPS = 30
# (pose, regex) - checked in order, first match wins
RULES = [
    ("point_side", r"\b(save|follow|bookmark|comment|subscribe)\b"),
    ("question", r"\?$"),
    ("secret", r"\b(secret|hidden|nobody|no one|easter egg|rare|unknown)\b"),
    ("warning", r"\b(careful|don'?t|never|avoid|cops?|police|wanted|warning|watch out|before it)\b"),
    ("money", r"(\$|\b(money|cash|grand|dollars?|price|cost|sell|worth|\d+k)\b)"),
    ("map_phone", r"\b(map|gps|waypoint|head to|go to|travel|location|marker|north|south|east|west)\b"),
    ("one", r"^(first|step one|1\.)\b"),
    ("two", r"^(then|next|second|step two|after that)\b"),
    ("three", r"^(third|finally|last|step three)\b"),
    ("gaming", r"\b(drive|driving|jump in|race|steer|fly|shoot|aim|escape)\b"),
    ("car_key", r"\b(keep|garage|register|own|key|park)\b"),
    ("thumbs_up", r"\b(easy|done|that'?s it|simple|risk-?free|works|guaranteed)\b"),
    ("shocked", r"\b(free|insane|crazy|wow|fastest|best|only|huge|never seen|unreal)\b"),
    ("celebrate", r"\b(enjoy|yours|boom|let'?s go|congrats|unlocked)\b"),
    ("laugh", r"\b(lol|funny|haha|hilarious|joke)\b"),
    ("point_down", r"\b(find|look|this|here|there|spot|right|inside|behind|sitting|open|follow the)\b"),
]
FALLBACK = ["talk", "point_down", "think", "point_viewer"]


def sentences(words):
    out, cur = [], []
    for w in words:
        cur.append(w)
        if w[0].rstrip('"\'').endswith((".", "?", "!")):
            out.append(cur); cur = []
    if cur:
        out.append(cur)
    return out


def plan(words, M):
    avail = set(os.path.splitext(f)[0] for f in os.listdir(M.get("dir", "brand/mascot/raccoon_poses")))
    over = {int(k): v for k, v in M.get("poses", {}).items()}
    res, prev = [], None
    for i, s in enumerate(sentences(words)):
        txt = " ".join(w[0] for w in s).strip()
        low = txt.lower()
        if i in over:
            p = over[i]
        else:
            cands = ([M.get("hook_pose", "point_viewer")] if i == 0 else []) + \
                    [p for p, rx in RULES if re.search(rx, low)] + FALLBACK
            cands = [c for c in cands if c in avail and c != prev]
            p = cands[0]
        res.append((s[0][1], p, txt)); prev = p
    return res


def rms_track(vo, dur):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", vo, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                         capture_output=True).stdout
    a = np.frombuffer(raw, np.int16).astype(float) / 32768
    n = int(dur * FPS) + 1; hop = 16000 // FPS
    r = np.array([np.sqrt(np.mean(a[i * hop:(i + 1) * hop] ** 2)) if i * hop < len(a) else 0 for i in range(n)])
    r = r / (np.percentile(r, 95) + 1e-6)
    return np.clip(np.convolve(r, np.ones(3) / 3, "same"), 0, 1.2)


def build(words, vo, dur, M, out):
    d = M.get("dir", "brand/mascot/raccoon_poses")
    W = M.get("w", 380); H = int(W * 3 / 4); B = 6; R = 26; PAD = 24
    cw, ch = W - 2 * B, H - 2 * B
    pl = plan(words, M)
    cache = {}

    def pose_img(p, zoom):
        key = (p, round(zoom, 3))
        if key not in cache:
            im = Image.open(os.path.join(d, p + ".jpg")).convert("RGB")
            # 4:3 crop around the character (pose images are 16:9, raccoon centred)
            th = im.height; tw = int(th * 4 / 3); x0 = (im.width - tw) // 2
            im = im.crop((x0, 0, x0 + tw, th))
            zw, zh = int(cw * zoom), int(ch * zoom)
            im = im.resize((zw, zh), Image.LANCZOS)
            ox, oy = (zw - cw) // 2, (zh - ch) // 2
            cache[key] = im.crop((ox, oy, ox + cw, oy + ch))
        return cache[key]

    # static frame parts: shadow + teal border + rounded mask + LIVE pill
    full = (W + 2 * PAD, H + 2 * PAD)
    base = Image.new("RGBA", full, (0, 0, 0, 0))
    sh = Image.new("RGBA", full, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((PAD, PAD + 8, PAD + W, PAD + H + 8), R, fill=(0, 0, 0, 160))
    base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)))
    ImageDraw.Draw(base).rounded_rectangle((PAD, PAD, PAD + W, PAD + H), R, fill=TEAL + (255,))
    mask = Image.new("L", (cw, ch), 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, cw, ch), R - B, fill=255)
    live = None
    if M.get("live", True):
        f = ImageFont.truetype("brand/fonts/TikTokSans-800.ttf", 20)
        tw = int(f.getlength("LIVE")); live = Image.new("RGBA", (tw + 44, 32), (0, 0, 0, 0)); dl = ImageDraw.Draw(live)
        dl.rounded_rectangle((0, 0, tw + 43, 31), 16, fill=(18, 15, 24, 220))
        dl.ellipse((10, 10, 22, 22), fill=(255, 50, 70)); dl.text((29, 16), "LIVE", font=f, fill="white", anchor="lm")

    rms = rms_track(vo, dur)
    starts = [s for s, _, _ in pl]
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{full[0]}x{full[1]}",
                          "-r", str(FPS), "-i", "-", "-c:v", "qtrle", out], stdin=subprocess.PIPE)
    n = int(dur * FPS)
    for i in range(n):
        t = i / FPS
        k = max(0, sum(1 for s in starts if s <= t + 0.04) - 1)
        pose = pl[k][1]
        since = t - (starts[k] if k else 0)
        pop = 1 + 0.07 * math.exp(-since * 14) if k or since < 0.3 else 1      # punch-in on every pose change
        talk = 1 + 0.025 * float(rms[min(i, len(rms) - 1)])                    # breathes with the voice
        fr = base.copy()
        fr.paste(pose_img(pose, pop * talk), (PAD + B, PAD + B), mask)
        if since < 0.08 and k:                                                 # 2-frame flash = cam "cut"
            fl = Image.new("RGBA", (cw, ch), (255, 255, 255, 90)); fr.paste(fl, (PAD + B, PAD + B), mask)
        if live:
            fr.alpha_composite(live, (PAD + B + 12, PAD + B + 12))
        p.stdin.write(fr.tobytes())
    p.stdin.close(); p.wait()
    return pl, (M.get("x", 120) - PAD, M.get("y", 250) - PAD)


if __name__ == "__main__":
    w = json.load(open(sys.argv[1])); vo = sys.argv[2]
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", vo]))
    pl, xy = build(w, vo, dur, {}, sys.argv[3])
    for s, p, t in pl:
        print(f"{s:6.2f}  {p:12s} {t}")
