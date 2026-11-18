#!/usr/bin/env bash
# Top Twitch clips for every streamer in watchlist.md (column 1 of the Creators table, Platform = Twitch).
# Usage: tools/twitch_clips.sh [range: 24hr|7d] [per-channel N]
# Needs: python3 -m venv /tmp/venv && /tmp/venv/bin/pip install yt-dlp
# Download one: /tmp/venv/bin/yt-dlp -o media/raw/clips/%(id)s.mp4 <clip url>
R=${1:-24hr}; N=${2:-5}
grep -iE '^\| *@?[A-Za-z0-9_]+ *\| *twitch' watchlist.md | awk -F'|' '{gsub(/[ @]/,"",$2); print $2}' | while read -r c; do
  timeout 60 /tmp/venv/bin/yt-dlp --flat-playlist --playlist-end "$N" \
    --print "%(view_count)s | $c | %(title)s | %(url)s" "https://www.twitch.tv/$c/clips?filter=clips&range=$R" 2>/dev/null
done | sort -t'|' -k1 -nr
