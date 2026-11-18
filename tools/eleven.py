#!/usr/bin/env python3
"""ElevenLabs via the REST API — use when the ElevenLabs MCP connector does not connect.

Key: env var ELEVENLABS_API_KEY, set in the CLOUD "gta6" environment settings (same way as
TWITCH_TOKEN). Never write the key into a file, log or chat. Also accepted: XI_API_KEY, ELEVEN_API_KEY.

  python3 tools/eleven.py check                                  # is the key there + valid?
  python3 tools/eleven.py tts   "<text with [excited] tags>" out.mp3 [voice_id] [model_id]
  python3 tools/eleven.py scribe in.mp3 words.json [language]     # word timings for info_build.py
  python3 tools/eleven.py music "<prompt>" out.mp3 [seconds]

Defaults: voice Nicholas – YouTuber AHc7z8dzjrGlVbbQ8enm, model eleven_v4 (CLAUDE.md).
scribe writes [["word",start,end], ...] — paste straight into the config's "words".
"""
import json, os, sys, urllib.request, urllib.error, uuid

API = "https://api.elevenlabs.io/v1"
VOICE = "AHc7z8dzjrGlVbbQ8enm"
MODEL = "eleven_v4"


def key():
    for n in ("ELEVENLABS_API_KEY", "XI_API_KEY", "ELEVEN_API_KEY"):
        v = os.environ.get(n, "").strip()
        if v:
            return v
    sys.exit("No ElevenLabs key: set ELEVENLABS_API_KEY in the cloud gta6 environment "
             "(it only reaches sessions started AFTER it was added).")


def call(path, data=None, headers=None, raw=False):
    h = {"xi-api-key": key()}
    h.update(headers or {})
    req = urllib.request.Request(API + path, data=data, headers=h, method="POST" if data else "GET")
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            body = r.read()
    except urllib.error.HTTPError as e:
        sys.exit(f"ElevenLabs HTTP {e.code}: {e.read()[:300].decode(errors='replace')}")
    return body if raw else json.loads(body)


def tts(text, out, voice=VOICE, model=MODEL):
    body = json.dumps({"text": text, "model_id": model}).encode()
    audio = call(f"/text-to-speech/{voice}?output_format=mp3_44100_128", body,
                 {"Content-Type": "application/json", "Accept": "audio/mpeg"}, raw=True)
    open(out, "wb").write(audio)
    print("ok", out, len(audio), "bytes")


def scribe(path, out, lang=None):
    b = uuid.uuid4().hex
    parts = [("model_id", "scribe_v1"), ("timestamps_granularity", "word")]
    if lang:
        parts.append(("language_code", lang))
    data = b"".join(f"--{b}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n".encode()
                    for k, v in parts)
    data += (f"--{b}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{os.path.basename(path)}\"\r\n"
             "Content-Type: application/octet-stream\r\n\r\n").encode() + open(path, "rb").read()
    data += f"\r\n--{b}--\r\n".encode()
    r = call("/speech-to-text", data, {"Content-Type": f"multipart/form-data; boundary={b}"})
    words = [[w["text"], round(w["start"], 2), round(w["end"], 2)]
             for w in r.get("words", []) if w.get("type", "word") == "word"]
    json.dump(words, open(out, "w"))
    print("ok", out, len(words), "words |", r.get("text", "")[:120])


def music(prompt, out, seconds=30):
    body = json.dumps({"prompt": prompt, "music_length_ms": int(float(seconds) * 1000)}).encode()
    audio = call("/music", body, {"Content-Type": "application/json", "Accept": "audio/mpeg"}, raw=True)
    open(out, "wb").write(audio)
    print("ok", out, len(audio), "bytes")


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] == "check":
        u = call("/user/subscription")
        print("key OK | tier:", u.get("tier"), "| chars used:", u.get("character_count"),
              "/", u.get("character_limit"))
    elif a[0] == "tts":
        tts(a[1], a[2], *(a[3:5]))
    elif a[0] == "scribe":
        scribe(a[1], a[2], *(a[3:4]))
    elif a[0] == "music":
        music(a[1], a[2], *(a[3:4]))
    else:
        sys.exit(__doc__)
