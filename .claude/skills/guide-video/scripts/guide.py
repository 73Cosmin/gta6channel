#!/usr/bin/env python3
"""Helper for the guide-video skill. Run from the repo root.

  guide.py prep  <name> <youtube-url> <start> <end>   download (tools/yt.sh), cut section, Scribe transcript,
                                                     contact sheet every 2 s (timestamps = section seconds)
  guide.py sheet <name> <from> <to> [step]            extra contact sheet of the section (default step 1 s)
  guide.py frame <name> <t>                           one full-size section frame (read menus/map text)
  guide.py vo    <name> "<script with [excited]>"     Nicholas TTS + Scribe word timings + sentence list
  guide.py check <name> [t1 t2 ...]                   phone-crop frames of media/edits/<date>_guide_<name>.mp4
Times may be seconds or m:ss. Files: media/raw/yt/<name>/ (gitignored), sheets in /tmp/guide_<name>/.
"""
import json, os, subprocess, sys, datetime

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def sec(t):
    t = str(t)
    if ":" in t:
        m, s = t.rsplit(":", 1)
        return int(m) * 60 + float(s)
    return float(t)


def run(*a, **k):
    subprocess.run(list(a), check=True, **k)


def sentences(words):
    out, cur, t0 = [], [], None
    for w, s, e in words:
        t0 = s if t0 is None else t0
        cur.append(w)
        if w.endswith((".", "?", "!")):
            out.append(f"{t0:6.2f}-{e:6.2f}  {' '.join(cur)}"); cur, t0 = [], None
    if cur:
        out.append(f"{t0:6.2f}-       {' '.join(cur)}")
    return "\n".join(out)


def sheet(src, out, start, length, step, cols):
    vf = (f"fps=1/{step},scale=300:-1,drawtext=fontfile={FONT}:text='%{{eif\\:t+{start}\\:d}}':"
          f"fontsize=30:fontcolor=yellow:borderw=3:x=5:y=5,tile={cols}x{int(length / step / cols) + 1}")
    run("ffmpeg", "-v", "error", "-y", "-ss", str(start), "-t", str(length), "-i", src, "-vf", vf,
        "-frames:v", "1", out)
    print("sheet", out)


def main():
    cmd, name = sys.argv[1], sys.argv[2]
    D = f"media/raw/yt/{name}"; T = f"/tmp/guide_{name}"
    os.makedirs(D, exist_ok=True); os.makedirs(T, exist_ok=True)
    sec_mp4 = f"{D}/section.mp4"
    if cmd == "prep":
        url, a, b = sys.argv[3], sec(sys.argv[4]), sec(sys.argv[5])
        run("tools/yt.sh", url, "--write-info-json", "-o", f"{D}/src.%(ext)s")
        run("ffmpeg", "-v", "error", "-y", "-ss", str(a), "-to", str(b), "-i", f"{D}/src.mp4", "-c:v", "libx264",
            "-crf", "18", "-preset", "veryfast", "-c:a", "aac", sec_mp4)
        run("ffmpeg", "-v", "error", "-y", "-i", sec_mp4, "-vn", "-ac", "1", "-b:a", "96k", f"{D}/section.mp3")
        run("python3", "tools/eleven.py", "scribe", f"{D}/section.mp3", f"{D}/section_words.json")
        print("\n=== SOURCE TRANSCRIPT (section seconds) ===")
        print(sentences(json.load(open(f"{D}/section_words.json"))))
        sheet(sec_mp4, f"{T}/sheet.jpg", 0, b - a, 2 if b - a <= 110 else 3, 8)
    elif cmd == "sheet":
        a, b = sec(sys.argv[3]), sec(sys.argv[4]); step = float(sys.argv[5]) if len(sys.argv) > 5 else 1
        sheet(sec_mp4, f"{T}/sheet_{int(a)}_{int(b)}.jpg", a, b - a, step, 7)
    elif cmd == "frame":
        t = sec(sys.argv[3]); out = f"{T}/frame_{t:g}.png"
        run("ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", sec_mp4, "-frames:v", "1", "-vf", "scale=1600:-1", out)
        print("frame", out)
    elif cmd == "vo":
        run("python3", "tools/eleven.py", "tts", sys.argv[3], f"{D}/vo.mp3")
        run("python3", "tools/eleven.py", "scribe", f"{D}/vo.mp3", f"{D}/vo_words.json")
        print("\n=== VO SENTENCES (vo seconds) ===")
        print(sentences(json.load(open(f"{D}/vo_words.json"))))
    elif cmd == "check":
        args = sys.argv[3:]
        cfg = None
        if args and os.path.exists(f"media/configs/{args[0].removesuffix('.json')}.json"):
            cfg = json.load(open(f"media/configs/{args.pop(0).removesuffix('.json')}.json"))
        out = cfg["out"] if cfg else f"media/edits/{datetime.date.today()}_guide_{name}.mp4"
        dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                             "-of", "csv=p=0", out]).decode())
        ts = [float(x) for x in args] or [0.05, 1.5, dur * .2, dur * .4, dur * .6, dur * .8, dur - .3]
        for i, t in enumerate(ts):
            run("ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", out, "-frames:v", "1",
                "-vf", "crop=883:1920:98:0,scale=220:-1", f"{T}/c_{i:02d}.png")
        run("ffmpeg", "-v", "error", "-y", "-i", f"{T}/c_%02d.png", "-vf", f"tile={len(ts)}x1", f"{T}/check.png")
        for i in range(len(ts)):
            os.remove(f"{T}/c_{i:02d}.png")
        print("check", f"{T}/check.png", "times", [round(t, 2) for t in ts], f"dur {dur:.2f}s")
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
