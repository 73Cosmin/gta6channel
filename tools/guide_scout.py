#!/usr/bin/env python3
"""Find fresh GTA 6 guide videos on YouTube for the guide-video skill (owner 2026-11-26: daily, automatic).

  python3 tools/guide_scout.py [--hours 72] [--top 12]

Searches YouTube (sorted by upload date, owner cookies via env YT_COOKIES) for several guide queries,
drops videos/chapters already used (media/guides_used.csv), then fetches upload date, views and chapters
for the newest candidates and ranks them by views per hour. Prints a table + chapters per video.
"""
import argparse, base64, csv, json, os, subprocess, tempfile, time, urllib.parse

QUERIES = ["gta 6 secret location", "gta 6 how to get", "gta 6 free car", "gta 6 rare car location",
           "gta 6 best weapon location", "gta 6 legendary weapon", "gta 6 make money fast", "gta 6 money spot",
           "gta 6 easter egg", "gta 6 secret mission", "gta 6 hidden", "gta 6 tips and tricks"]
YTDLP = "/tmp/venv/bin/yt-dlp"
USED = "media/guides_used.csv"


def ensure_ytdlp():
    if not os.path.exists(YTDLP):
        subprocess.run(["python3", "-m", "venv", "/tmp/venv"], check=True)
        subprocess.run(["/tmp/venv/bin/pip", "-q", "install", "yt-dlp[default]"], check=True)


def ytdlp(ck, *args, timeout=180):
    r = subprocess.run([YTDLP, "--cookies", ck, "--js-runtimes", "node", "--no-warnings", *args],
                       capture_output=True, text=True, timeout=timeout)
    return r.stdout


def topic_demand(ck, title):
    """YouTube click demand for a topic: views of the top 5 search results (relevance) for 'gta 6 <topic>'."""
    import re
    t = re.sub(r"(?i)\b(gta ?6|gta ?vi|free|location|locations|how to get|where to find|number \d+)\b", " ", title)
    t = re.sub(r"[^\w' ]", " ", t); t = " ".join(t.split())
    if not t:
        return 0, ""
    url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote_plus("gta 6 " + t) + "&sp=EgIQAQ%3D%3D"
    out = ytdlp(ck, "--flat-playlist", "--playlist-end", "5", "--print", "%(view_count)s", url, timeout=90)
    views = [int(x) for x in out.split() if x.isdigit()]
    return sum(views), t


def rank_chapters(ck, vid):
    js = ytdlp(ck, "--skip-download", "--dump-json", f"https://www.youtube.com/watch?v={vid}", timeout=120)
    d = json.loads(js.splitlines()[0])
    used = set()
    if os.path.exists(USED):
        used = {r["chapter"] for r in csv.DictReader(open(USED)) if r["video_id"] == vid}
    print(f"{d['title']} | {d.get('channel')} | {d.get('view_count')} views")
    rows = []
    for c in d.get("chapters") or []:
        if c["title"].lower() in ("intro", "outro") or c["end_time"] - c["start_time"] < 25:
            continue
        dem, q = topic_demand(ck, c["title"])
        s = int(c["start_time"]); e = int(c["end_time"])
        rows.append((dem, f"{s//60}:{s%60:02d}-{e//60}:{e%60:02d}", c["title"], q))
    for dem, span, t, q in sorted(rows, reverse=True):
        flag = "  (USED)" if t.lower() in {u.lower() for u in used} else ""
        print(f"{dem:>11,} demand | {span:13} | {t}  [search: {q}]{flag}")
    print("Generic chapter titles (e.g. 'Number 7') give no demand signal - judge those from the transcript/frames.")


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--hours", type=float, default=72)
    ap.add_argument("--top", type=int, default=12)
    ap.add_argument("--chapters", metavar="VIDEO_ID", help="rank one video's chapters by YouTube topic demand")
    a = ap.parse_args()
    ensure_ytdlp()
    if a.chapters:
        ck = tempfile.mktemp(); open(ck, "wb").write(base64.b64decode(os.environ["YT_COOKIES"])); os.chmod(ck, 0o600)
        try:
            rank_chapters(ck, a.chapters)
        finally:
            os.remove(ck)
        return
    used = set()
    if os.path.exists(USED):
        used = {r["video_id"] for r in csv.DictReader(open(USED)) if r.get("chapter", "") in ("", "ALL")}
    ck = tempfile.mktemp(); open(ck, "wb").write(base64.b64decode(os.environ["YT_COOKIES"])); os.chmod(ck, 0o600)
    try:
        cand = {}
        for q in QUERIES:
            url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote_plus(q) + "&sp=CAISAhAB"
            out = ytdlp(ck, "--flat-playlist", "--playlist-end", "12", "--print",
                        "%(id)s\t%(duration)s\t%(channel)s\t%(title)s", url)
            for line in out.splitlines():
                p = line.split("\t")
                if len(p) == 4 and p[0] not in used and p[1] not in ("NA", "None") and float(p[1]) >= 120:
                    if any(b in p[3].lower() for b in ("glitch", "exploit", "mod menu", "early access", "leak")):
                        continue   # hard rule 4: no exploits / play-early
                    if "gta 6" in p[3].lower() or "gta6" in p[3].lower() or "gta vi" in p[3].lower():
                        cand.setdefault(p[0], p)
        rows, now = [], time.time()
        for vid in list(cand)[:40]:
            js = ytdlp(ck, "--skip-download", "--dump-json", f"https://www.youtube.com/watch?v={vid}", timeout=120)
            if not js.strip():
                continue
            d = json.loads(js.splitlines()[0])
            ts = d.get("timestamp") or time.mktime(time.strptime(d.get("upload_date", "19700101"), "%Y%m%d"))
            age = max(1.0, (now - ts) / 3600)
            if age > a.hours:
                continue
            rows.append((d.get("view_count", 0) / age, age, d, vid))
        rows.sort(key=lambda r: -r[0])
        for vph, age, d, vid in rows[:a.top]:
            print(f"\n{vph:8.0f} views/h | {age:5.1f} h old | {d.get('view_count',0):>8} views | "
                  f"{d.get('channel')} (@{(d.get('uploader_id') or '').lstrip('@')}) | {d['duration']//60}:{d['duration']%60:02d}")
            print(f"  https://youtu.be/{vid}  {d['title']}")
            for c in d.get("chapters") or []:
                s = int(c["start_time"]); print(f"    {s//60}:{s%60:02d}  {c['title']}")
        if not rows:
            print("no fresh candidates")
    finally:
        os.remove(ck)


if __name__ == "__main__":
    main()
