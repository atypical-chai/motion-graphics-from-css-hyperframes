# Motion Graphic Generator

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
