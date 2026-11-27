# Mascot proposals v1 (2026-11-27)

Idea from the Danny Why video ("bend, don't copy"): an own recurring character that presents every guide
(hook + end), so our videos look different from the 1deflay-style clones. AI-made -> set isAiGenerated.
Made with ElevenLabs gpt-image-2.5-sunburst (flow "NE0N LEONIDA Maskottchen v1"), style: GTA-VI-key-art-like
painted illustration, bold outlines, pink/teal/orange sunset palette. Original characters, no Rockstar characters/logos.

1. `1_gator.png` - "Neon" the alligator: floral shirt, gold chain, aviators, pink 80s sports car
2. `2_flamingo.png` - flamingo hustler: white suit, phone with map pin (fits "secret location" guides)
3. `3_masked.png` - faceless masked guy: pink bandana, teal cap, cash duffel (fits a faceless page)
4. `4_raccoon.png` - raccoon treasure hunter: beanie + headlamp, backpack with cash/keys, points at viewer
5. `5_panther.png` - Florida panther street racer: teal racing jacket, car key (fits car guides)

Status: waiting for the owner's pick. Next: same character in 5-8 poses, background removed (PNG), for the hook card.

## Raccoon facecam (owner picked #4, 2026-11-27)
`raccoon_poses/<pose>.jpg` - 19 poses, same streamer-room framing (base: gemini-3-pro-image from 4_raccoon.png,
poses: seedream-5.5 edits of the base): talk, point_viewer, point_down, point_side, shocked, thumbs_up, think, secret,
money, car_key, map_phone, gaming, one, two, three, warning, laugh, celebrate, question.
Used by `tools/mascot_cam.py` via guide_build_v2 config `"mascot": {...}`: facecam top-left (x120 y250 w380, teal border,
LIVE pill), GTA VI logo moves right of it, one pose per sentence (keyword rules, never the same pose twice in a row,
override with `"poses": {"<idx>": "<pose>"}`), punch-in + flash on every pose change, breathes with the voice.
Test: media/configs/2026-11-27_guide_urus_raccoon_test.json -> media/edits/2026-11-27_guide_urus_raccoon_test.mp4
(NOT published, waiting for owner feedback).
