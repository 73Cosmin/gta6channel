---
name: slideshow
description: >-
  Build and publish a branded GTA 6 TikTok photo-mode slideshow (4:5 carousel, 1080x1350) for @ne0nleonida:
  card-style cover, branded body slides, save-worthy utility topic, caption, sound, Buffer REMINDER.
  Use for "slideshow", "Slides", "carousel", "photo post", "X and their locations", checklist / how-to /
  "all collectibles" / "free cars" posts, or when a content run fills a slot with a slideshow.
---

# slideshow

> **CONTENT PLAN v5 (owner 2026-11-28): slideshows are THE TikTok utility format** - guide topics (cars, weapons, money,
> secret quests) go to TikTok as list or step slideshows (Hurricane = step slideshow 38K; supercars list 9.8K overnight),
> the video version only to YouTube. Default: 1 per day as owner reminder at 14:30.

Our biggest posts are slideshows: Platinum checklist 412K, Hurricane how-to 30K (re-upload, 498 saves @8.5 h),
Collectibles 5.7K, "10 hidden controls" 3.6K. Reference account @gta6clips114 ('CARS AND THEIR LOCATIONS' 4.9M /
406K saves). They travel via **saves + shares**, not comments, and grow in waves for days.

## 0. Hard rules (owner)
1. **Topic = save-worthy utility** people WANT: "X and their locations", "how to get/trigger X", money spots,
   checklists ("everything for 100%"), step-by-step secrets. Items must be cool (supercars, luxury, legendary
   weapons, big money) - no beaters/bikes/trivia ("5 things that happen" = worst slideshow ever, 2026-11-22).
   Lists of many THINGS beat single-item guides.
2. **Every fact real and checked** (own capture or credited guide/stream; read menus/maps from frames, never guess).
   No invented cheat codes/dates (CLAUDE.md hard rule 2).
3. **Branding on EVERY slide** (owner 2026-11-26: "das ist unser Wiedererkennungswert" / "man muss merken dass es von
   meinem account ist"): see 2. DESIGN. Slide 1 is ALWAYS the card-style cover.
4. **No "Fan page / not affiliated with Rockstar" line** anywhere (hard rule 2026-11-26). Source only TINY bottom-left
   (18 px grey, builders do this). Caption keeps `📋 Source: @creator`.
5. **TikTok = Buffer REMINDER (schedulingType notification), NEVER automatic**: photo posts via Buffer go out with
   NO sound (2026-11-26 cars slideshow, owner took it down). The owner posts in-app and adds the sound.
6. Bright, clean images only: real in-game frames, no dark/blurry stream shots, no facecam/HUD junk where avoidable.
   Cover = real frame (an AI-looking cover did 543 views vs 10.1K for the same slides with a real frame = 18x).

## 1. Material
- Source: owner capture > credited YouTube guide (download with `tools/yt.sh <url> --write-info-json -o media/raw/yt/<n>/src.%(ext)s`,
  chapters in `src.info.json`) > credited streams/X posts. `media/raw/yt/` is gitignored - never commit raw footage.
- Per item you need: a BRIGHT shot of the item (studio/garage/daylight) + the pause-map frame with the waypoint
  (or the key step frame). Find timestamps with a contact sheet:
  `ffmpeg -ss A -t L -i src.mp4 -vf "fps=1/2,scale=300:-1,tile=6x6" sheet.jpg` and read it; zoom single frames to read
  names/prices/locations exactly.
- 8-14 items (list) or 5-9 steps (how-to). Cover + items + end slide.

## 1b. Image quality beats "own frames" (owner 2026-11-27: "maximal schlecht ... Bildqualität katastrophal")
Frames grabbed from a 1080p YouTube video (blurred motion, HUD, tiny map) look bad on a 4:5 slide - the owner rejected
the dkdynamite version. When a viral reference post has clean car shots + clear map crops, the owner wants THOSE images
restyled in our look: `slides_v2_build.py` items take `"car_img": [path, top, bottom]` / `"map_img": [...]` (row crops of
the reference image, the reference's own label band cut out) + unsharp mask; cover via card builder `"img"`.
Credit the reference account (`Source: @account (X)` tiny + `📋 Source:` in the caption).
**LOW-RES SOURCES MUST BE AI-UPSCALED FIRST (owner 2026-11-27: v2 'extrem schlecht, verpixelt' - X images are only ~626 px wide):**
never plain-resize a <1000 px image to a 1080 slide. Run Real-ESRGAN x4 (CPU, ~80 s/image, run in background for many):
`curl -sL -o /tmp/RealESRGAN_x4plus.pth https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth`
(needs `pip install torch --index-url https://download.pytorch.org/whl/cpu`; model stays OUTSIDE the repo), then
`python3 tools/upscale.py /tmp/RealESRGAN_x4plus.pth in.jpg out_x4.png`, and in the config `"img_scale": 4, "sharpen": false`
with the crops still measured on the original. Example: media/configs/2026-11-27_slides_supercars_v3.json.
Example: media/configs/2026-11-27_slides_supercars_v2.json (ref x.com/eliplaysgta, 714K views).
If we use our own frames: only sharp, still, well-lit shots and FULL-SCREEN pause-map frames - never mid-motion frames.

## 2. DESIGN (our look - all builders in `tools/`)
**Cover (slide 1) = card style**, `tools/slides_card_build.py` slide with `"cover": true`:
bright image top (~820 px) fading into dark navy, pill tag top-left `▍GTA VI / <TOPIC>`, teal counter `01 / NN`
top-right, giant white h1 + teal h2 (the promise: 'DID YOU KNOW' / 'YOU CAN TRIGGER A HURRICANE?',
'9 FREE CARS' / 'WITH NO TRACKER'), white sub line, teal `SWIPE FOR ... →`, teal `SAVE THIS LIST/GUIDE` bottom-right,
tiny source bottom-left. Example: `media/configs/2026-11-26_slides_free_cars_v3_cover.json`.

**Body slides** - pick ONE builder per slideshow:
- **List of things + locations** -> `tools/slides_v2_build.py` (item frame top, map bottom, '1. NAME' white + yellow
  info, 'HEAD HERE' + yellow location). ALWAYS set `"brand": {"tag": "GTA VI  /  <TOPIC>"}` -> same pill + teal
  `NN / TT` counter on every slide + teal divider. Its own cover is NOT our style: build the card cover alone
  (`"total": NN` in the card config) and copy it over `01.jpg`.
  Example: `media/configs/2026-11-26_slides_free_cars_v4.json` (+ `_v3_cover.json`) -> `media/edits/2026-11-26_slides_free_cars_v4/`.
- **How-to steps / checklists** -> `tools/slides_card_build.py` all the way (cover + `"step"` slides: image top half,
  teal 'STEP 1', white head, teal bar, body text; `"list"` slides: teal key/value card rows; `"full"` = whole map
  screenshot on a card). Example: `media/configs/2026-11-26_slides_hurricane_reupload.json`.
- Legacy (don't use for new posts): slides_build.py, slides45_build.py.

**End slide**: question the viewer can answer/correct ('WHICH ONE ARE YOU GRABBING FIRST?') + one twist/info line,
branded (pill + counter). Comment trigger must give them something to correct or pick - a neutral A/B gets 0.

## 3. Build + check
```bash
python3 tools/slides_card_build.py media/configs/<date>_slides_<topic>_cover.json   # or the full card slideshow
python3 tools/slides_v2_build.py  media/configs/<date>_slides_<topic>.json          # list body (with "brand")
cp media/edits/<cover_dir>/01.jpg media/edits/<slides_dir>/01.jpg
```
Read a contact strip of cover + 2 body slides + end (`ffmpeg -i 01.jpg -i 02.jpg ... -filter_complex hstack=N`) and check:
bright images, every name/price/location readable and correct, pill + counter + teal on every slide, nothing cut off,
counter total = real slide count, no disclaimer, credit tiny bottom-left. New design or new topic type -> show the
owner a preview first.

## 4. Caption (≤ ~300 chars)
`<exact search phrase + promise> <emoji> Save this before you <reason>. <question they can answer> 👇`
blank line, `📋 Source: @creator (YouTube)`, then **max 5 hashtags**: #gta6 #gta6cars/#gta6secrets/#gta6tips
#grandtheftauto6 #gta6map (+ #fyp). No fan-page line. Story spoilers -> caption starts with "SPOILER".
Example (cars): "9 FREE cars in GTA 6 with NO tracker + where to find them 🚗 Save this before you spend your money.
Which one are you grabbing first? 👇 / 📋 Source: @subscribefortacos (YouTube) / #gta6 #gta6cars #grandtheftauto6 #gta6map #gta6news"

## 5. Publish
- Commit slides + configs to `main`, confirm each raw URL returns 200
  (`https://raw.githubusercontent.com/73Cosmin/gta6channel/main/media/edits/<dir>/NN.jpg`).
- Buffer TikTok channel `create_post` with all images in order, `schedulingType: "notification"` (REMINDER), at the slot
  (07:00 slot = the day's strongest how-to; day-by-day rule). Never automatic.
- In the run's final message tell the owner: slot time, **sound suggestion** (default: official GTA VI soundtrack
  'Flower In A Hurricane'; or a trending GTA sound), and that the caption is in the Buffer reminder.
- If the owner wants to post manually right away: send the slides with SendUserFile (display "attach") + the caption.
- IG: optional carousel of the same slides (automatic is fine there; IG adds no sound either -> only if the owner asks).
- Log in `log.md`, row in `scoreboard.csv` (format 'Utility slideshow').

## 6. Read + iterate
- Slideshows start slow (Collectibles 137 @30 min -> 3.9K @11.5 h) and grow in waves -> judge at **6-10 h and 24-36 h**,
  never delete before. Key metrics: saves, shares, "photos viewed" (Platinum 5.1/10 = good; 3.2/14 = list too long).
- A flopped slideshow gets ONE re-upload with a new real-frame cover (Hurricane: 543 -> 13.5K with only the cover changed).
- A same-theme "part 2" next to a viral post does not inherit its reach - give it its own strong promise.
- Note wins/losses in `learning.md`; update this skill when the owner changes the look.
