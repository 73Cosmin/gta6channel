#!/usr/bin/env python3
"""Top GTA 6 Twitch clips + live streams via the official Twitch API (Helix).
Token is injected by the environment proxy for api.twitch.tv (never stored here).
Client ID below is public. Token from implicit sign-in lasts ~60 days; on 401 -> ACTION NEEDED: owner redoes sign-in.
Usage: python3 tools/twitch_top.py [hours=6] [n=20] [lang=en,de,...]
"""
import json, sys, urllib.request, datetime
CID = "sxu1ftvu7tqrhvjx9dlfmhd4ga6xs1"; GID = "1867279146"  # Grand Theft Auto VI
def get(path):
    r = urllib.request.Request("https://api.twitch.tv/helix/" + path, headers={"Client-Id": CID})
    return json.load(urllib.request.urlopen(r, timeout=20))
hours = float(sys.argv[1]) if len(sys.argv) > 1 else 6
n = int(sys.argv[2]) if len(sys.argv) > 2 else 20
langs = sys.argv[3].split(",") if len(sys.argv) > 3 else None
since = (datetime.datetime.utcnow() - datetime.timedelta(hours=hours)).strftime("%Y-%m-%dT%H:%M:%SZ")
clips = get(f"clips?game_id={GID}&started_at={since}&first=100")["data"]
clips = [c for c in clips if not langs or c["language"] in langs]
print(f"TOP CLIPS (last {hours:g}h)")
for c in sorted(clips, key=lambda c: -c["view_count"])[:n]:
    print(f'{c["view_count"]:>6} | {c["broadcaster_name"]} | {c["language"]} | {c["duration"]:.0f}s | {c["created_at"]} | {c["title"]} | {c["url"]}')
print("\nLIVE NOW")
for s in get(f"streams?game_id={GID}&first=20")["data"]:
    if not langs or s["language"] in langs:
        print(f'{s["viewer_count"]:>6} | {s["user_login"]} | {s["language"]} | {s["title"][:70]}')
