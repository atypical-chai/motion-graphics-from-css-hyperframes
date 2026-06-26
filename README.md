# Motion Graphic Generator

**Make motion graphics by writing plain HTML/CSS, and get back a video with a
see-through (transparent) background that you can drop straight onto a layer in
Premiere Pro, DaVinci Resolve, Final Cut, or any editor.**

![Chapter-break overlay animating over a transparency checkerboard](docs/demo-chapter-break.gif)

<sub>↑ A chapter-break clip from this repo. The grey checkerboard = transparency:
there's no background, so in your editor your footage shows through behind it.</sub>

## What it does (in plain words)
Normally, building animated lower-thirds, chapter titles, callouts, and intros
means learning heavy motion-graphics software (After Effects, etc.). This project
lets you describe the animation as a simple web page — text, shapes, colors, and a
CSS `@keyframes` animation — and it renders that page into a **transparent video
clip**. "Transparent" means there's no background box around your graphic: only the
text/shapes are visible, so when you place the clip over your footage in an editor,
your video shows through behind it, exactly like a professional overlay.

Under the hood it loads your page in a real (headless) Chrome browser, screenshots
every frame, and stitches them into a **ProRes 4444 `.mov`** (the high-quality format
editors use for transparency) — then automatically checks, pixel by pixel, that the
transparency is actually there before handing you the file.

## Who it's for / use cases
- **Video editors / YouTubers / podcasters** who want clean, on-brand overlays
  (chapter breaks, name tags, stat callouts, intros/outros) without learning After Effects.
- **Anyone comfortable with basic HTML/CSS** (or an AI assistant) who'd rather
  "design in code" and reuse/template graphics across many episodes.
- **Batch work:** render one design with dozens of different text values at once
  (e.g. 14 chapter titles → 14 ready-to-edit clips).

> Built on top of HeyGen **HyperFrames** (the headless-Chrome renderer) + **ffmpeg**.
> Animation is pure CSS — no After Effects, no GSAP, no JavaScript animation needed.

## Why this exists
I make videos and kept hitting the same wall: I needed **custom** motion graphics,
but AI video generators give you almost no control and wildly unpredictable
results. Then I noticed something — when I'd discuss a design with an AI assistant
like Claude, it would already hand me **HTML/CSS**. So the question became: *what if
I could turn that HTML straight into a usable video clip?*

That's all this is — the missing bridge from "design discussed in HTML" →
"transparent video clip for any editor." If you already design in code (or let an
LLM do it for you), you can now get a real motion graphic out the other end,
instead of fighting a black-box video generator.

## Roadmap (this is an early, working start)
I'll keep updating this with **new templates and repeatable patterns** for making
**predictable, customizable** motion graphics — the exact thing AI video tools
don't give you. Today it's a solid foundation (chapter breaks, lower-thirds,
callouts, intros via plain CSS); more building blocks are coming. Ideas and
contributions welcome.

---

Turn HTML/CSS animations into **transparent video** (ProRes 4444 `.mov` / VP9 `.webm`)
for editing in Premiere. One engine, many projects.

## How to think about it
- This whole folder is the **engine** (the HyperFrames renderer, its browser, and the
  AI "skills" in `.agents/`). You set it up once.
- Your actual work lives under **`projects/<name>/`**. Each project (a podcast, a client,
  a campaign) is just a folder of animation files. You never copy the engine.

## Folder structure
```
Motion Graphic Generator/
├─ projects/                     ← all your work lives here
│   └─ example/                  ← shipped SAMPLE project (tracked — copy it to start)
│       ├─ css-sandbox/          ← browser design lab: iterate the LOOK  (DESIGN)
│       ├─ compositions/         ← your animation .html files            (INPUT)
│       ├─ batch/                ← .json lists of text values            (INPUT)
│       └─ renders/              ← finished .mov / .webm videos          (OUTPUT)
│   └─ <your-project>/           ← your real shows/clients (git-ignored, stay local)
│       ├─ css-sandbox/
│       ├─ compositions/
│       ├─ batch/
│       └─ renders/
├─ templates/
│   └─ _TEMPLATE.html            ← copy this to start a new animation
├─ tools/
│   ├─ render.ps1                ← render ONE clip + verify alpha
│   ├─ render-batch.ps1          ← render ONE design × MANY text rows
│   ├─ render-all.ps1            ← render EVERY clip in a project
│   └─ verify_alpha.py           ← proves the transparency is real
├─ README.md                     ← you are here
├─ GENERATOR-PROMPT.md           ← the exact format to give Cursor/Claude
├─ WORKFLOW.md                   ← deeper how-to + gotchas
└─ (engine: .agents/, meta.json, hyperframes.json, index.html, ...)  ← don't touch
```

## Where does what go?
| Thing | Where |
|---|---|
| **Design experiments** (look/motion, previewed in a browser) | `projects/<project>/css-sandbox/` |
| **Your animation HTML** | `projects/<project>/compositions/<name>.html` |
| **Your text lists** (for batch) | `projects/<project>/batch/<name>.json` |
| **The instruction format** for your AI tool | `GENERATOR-PROMPT.md` (paste it into Cursor/Claude) |
| **Finished videos** | `projects/<project>/renders/` |

## Two ways to work
**A. Design lab → lock → render** (when you're still figuring out the look).
You bring a description; the assistant builds throwaway preview pages in
`projects/<project>/css-sandbox/` that you open in a normal browser, iterate on
together (position, colors, motion, replay button to re-watch), and once you
approve a design it gets turned into a real composition + rendered. See the
walkthrough in `WORKFLOW.md`.

**B. Bypass → render** (when the design is already decided).
Skip the sandbox entirely: write/paste the composition straight into
`compositions/` and render. This is the original 3-step flow below.

> The sandbox is for your eyes only — those files are NEVER rendered. Only files
> in `compositions/` get turned into video. This keeps experiments from polluting
> the things that actually ship.

## Make a new animation (3 steps — the "bypass" path B)
1. Get HTML from your AI tool using `GENERATOR-PROMPT.md`, **or** copy `templates/_TEMPLATE.html`.
2. Save it as `projects/<project>/compositions/<name>.html`.
3. Render + verify:
   ```
   tools\render.ps1 <project> <name>
   ```
   Wait for `[PASS]`, then grab the `.mov` from `projects/<project>/renders/`.

## Start a new project (e.g. a second show)
```
mkdir projects\<new-project>\css-sandbox, projects\<new-project>\compositions, projects\<new-project>\batch, projects\<new-project>\renders
```
Then either iterate the look in `css-sandbox/` (path A) or drop HTML straight
into `compositions/` and render (path B).

## The three input shapes (see GENERATOR-PROMPT.md for the exact format)
1. **One design, one text** → a single `.html` → `tools\render.ps1 <project> <name>`
2. **One design, many texts** (e.g. 15 chapter titles) → one *parameterized* `.html` + a
   `batch/*.json` of rows → `tools\render-batch.ps1 <project> <name> <batchfile>`
3. **Many different designs** → several `.html` files in `compositions/` →
   `tools\render-all.ps1 <project>`

> First render of any clip takes ~2 min (pure-CSS timing wait). That's expected.
