"""Generate the 4 hero/section visuals for the eng-dashboard presentation.

Run:
    set -a; source ~/cowork/.env; set +a
    /Users/cyberjack/cowork/apps/gemini-api/.venv/bin/python \
        /Users/cyberjack/cowork/apps/eng-dashboard/presentation/gen_images.py
"""
import pathlib
from google import genai
from google.genai import types

OUT = pathlib.Path(__file__).parent / "img"
OUT.mkdir(parents=True, exist_ok=True)

STYLE = (
    "Dark slate-900 background, accent palette of cyan-400 and amber-400, "
    "moody cinematic lighting, soft glow, clean modern flat-illustration with "
    "subtle gradients, no text, no letters, no numbers, 16:9."
)

JOBS = {
    "hero.png": (
        "A glowing constellation of skill nodes connected by faint geometric lines, "
        "forming an abstract radar/spider chart suspended in space. Rays of light "
        "emanate from a central core. Sense of progression, mastery, growth. "
        + STYLE
    ),
    "pipeline.png": (
        "An abstract three-stage data pipeline rendered as flat illustration: "
        "left side a stylized spreadsheet/grid icon, center interlocking gears or "
        "a neural classifier shape, right side a glowing dashboard with bar and "
        "radar chart silhouettes. Connecting flow lines between the three stages. "
        + STYLE
    ),
    "skills.png": (
        "An eight-pointed luminous star or hexagonal honeycomb arrangement, each "
        "facet glowing slightly differently to suggest distinct skill domains "
        "(coding, electronics, electrical, mechanical, assembly, testing, teamwork, "
        "management). Symmetrical, balanced, jewel-like. "
        + STYLE
    ),
    "closing.png": (
        "A soft upward arc of glowing particles rising and converging, suggesting "
        "level-up, progression, growth over time. Minimal, hopeful, polished. "
        + STYLE
    ),
}

client = genai.Client()
cfg = types.GenerateContentConfig(
    response_modalities=["IMAGE"],
    image_config=types.ImageConfig(aspect_ratio="16:9"),
)

for name, prompt in JOBS.items():
    path = OUT / name
    if path.exists():
        print(f"skip (exists): {path}")
        continue
    print(f"generating: {name}")
    resp = client.models.generate_content(
        model="gemini-2.5-flash-image",
        contents=prompt,
        config=cfg,
    )
    saved = False
    for part in resp.candidates[0].content.parts:
        if part.inline_data:
            path.write_bytes(part.inline_data.data)
            print(f"  saved: {path} ({len(part.inline_data.data)} bytes)")
            saved = True
            break
    if not saved:
        print(f"  WARN: no image returned for {name}")

print("done.")
