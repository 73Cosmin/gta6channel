#!/usr/bin/env bash
# YouTube download with the owner's cookies (tested 2026-11-26).
# YT_COOKIES = base64 Netscape cookie file, env var in the cloud gta6 environment (never write it into the repo).
# Usage: tools/yt.sh <url> [extra yt-dlp args]   e.g. tools/yt.sh URL -o media/raw/clips/%(id)s.%(ext)s
set -euo pipefail
[ -x /tmp/venv/bin/yt-dlp ] || { python3 -m venv /tmp/venv && /tmp/venv/bin/pip -q install "yt-dlp[default]"; }
[ -n "${YT_COOKIES:-}" ] || { echo "YT_COOKIES not set" >&2; exit 1; }
CK=$(mktemp /tmp/ytck.XXXXXX); chmod 600 "$CK"; trap 'rm -f "$CK"' EXIT
printf '%s' "$YT_COOKIES" | base64 -d > "$CK"
# --js-runtimes node is required: without it YouTube's n-challenge fails and only images are offered.
/tmp/venv/bin/yt-dlp --cookies "$CK" --js-runtimes node -f "bv*[height<=1080]+ba/b" --merge-output-format mp4 "$@"
