# The format to give your HTML/CSS generator (Cursor / Claude / etc.)

Pick the shape that matches what you need, copy that block into your AI tool, fill the
ALL-CAPS placeholders, then save the output into the folder shown and render. Every
shape obeys the same **contract** (below) so the file drops straight into the engine.

## Where to save the output
| You asked for | Save the file(s) as | Then run |
|---|---|---|
| Shape 1 — one design, one text | `projects/<project>/compositions/<name>.html` | `tools\render.ps1 <project> <name>` |
| Shape 2 — one design, many texts | `projects/<project>/compositions/<name>.html` **+** a list at `projects/<project>/batch/<name>.json` | `tools\render-batch.ps1 <project> <name> <name>` |
| Shape 3 — many different designs | one `.html` **per design** in `projects/<project>/compositions/` | `tools\render-all.ps1 <project>` |

(`<project>` = a folder under `projects/`, e.g. `podcast`.)

---

## The contract (ALL shapes must follow this)
Tell your AI tool to always obey these rules. Output ONE self-contained HTML file per design, nothing else.

1. Root element exactly this shape, with **`data-duration` in seconds** (REQUIRED — without it the render fails with "zero duration"):
   `<div id="root" data-composition-id="UNIQUE_NAME" data-start="0" data-duration="<SECONDS>" data-width="1920" data-height="1080">`
2. Transparent background so the export keeps alpha: `html,body{ margin:0; padding:0; background:transparent; }`
3. Animate with **pure CSS `@keyframes` only**. NO JavaScript animation, NO GSAP, NO libraries.
4. Every animated element gets a **stable `id`** plus `class="... clip" data-start="0" data-duration="<SECONDS>" data-track-index="0"` (increment `data-track-index` for stacked elements).
5. `animation-duration` should match `data-duration` for a clean single loop.
6. Canvas is 1920x1080; position with absolute positioning. A Google Fonts `<link>` is fine.
7. Use this brand palette (CSS variables), don't invent colors unless asked:
   `--kraft:#ECE2CF; --paper:#F3ECDB; --cream:#F6EDD6; --ink:#232A3A; --green:#3F8A5A; --blue:#2F5AA8; --yellow:#E6B53C; --coral:#DF8A64;`
8. At the visual midpoint of the animation the main element must be fully on-screen (that's the frame I spot-check).

---

## SHAPE 1 — one design, one fixed text
> Build ONE self-contained HTML composition for the HyperFrames renderer, obeying the contract below. Output only the HTML.
> **Animation:** DESCRIBE IT (look, position, motion, exact text, total seconds). e.g. "bottom-left cream chapter strip reading `03 · PAYING THE VENDOR`, slides in from the left over 0.4s, holds ~2.4s, slides out; 4 seconds total."
> **Contract:** [paste the 8 contract rules above]

Save as `projects/<project>/compositions/<name>.html` → `tools\render.ps1 <project> <name>`

---

## SHAPE 2 — one design, MANY text values (parameterized)
Use when the design is identical and only the words change (e.g. 15 chapter cards).
> Build ONE self-contained HTML composition for HyperFrames, obeying the contract below, AND make every piece of on-screen text a **variable** so I can swap it per render without editing the file:
> 1. Declare the variables on the `<html>` tag: `data-composition-variables='[{"id":"num","type":"string","label":"Number","default":"03"},{"id":"title","type":"string","label":"Title","default":"PAYING THE VENDOR"}]'` (one entry per swappable field).
> 2. Give each text element a stable `id`. At the END of `<body>`, add a small script that reads the values once and fills them in:
>    `const v = window.__hyperframes.getVariables(); document.getElementById('ch-num').textContent = v.num; document.getElementById('ch-title').textContent = v.title;`
> 3. Keep ALL motion as pure CSS `@keyframes`. The variables only fill text; they never animate.
> **Animation:** DESCRIBE IT + list the swappable fields (e.g. `num`, `title`) and total seconds.
> **Contract:** [paste the 8 contract rules above]

Then make a text list `projects/<project>/batch/<name>.json` — one row per output:
```json
[
  { "out": "ch-03-paying-the-vendor", "num": "03", "title": "PAYING THE VENDOR" },
  { "out": "ch-04-the-negotiation",   "num": "04", "title": "THE NEGOTIATION" }
]
```
`out` = the output file name. Render all rows: `tools\render-batch.ps1 <project> <name> <name>`
(Working example: `projects/podcast/compositions/chapter-break.html` + `projects/podcast/batch/chapter-breaks.json`.)

---

## SHAPE 3 — many DIFFERENT designs, each its own text
Use when the clips look different from each other.
> Build SEVERAL self-contained HyperFrames compositions, **each obeying the contract below**. Return each as a SEPARATE complete HTML file with its own unique `data-composition-id`, clearly labeled so I can save each to its own file. Do not merge them into one document.
> **Animations:** list them, e.g.
>   1. "lower-third name tag: ... 5s, text `JANE DOE / HOST`"
>   2. "outro card: ... 3s, text `THANKS FOR WATCHING`"
> **Contract:** [paste the 8 contract rules above]

Save each as `projects/<project>/compositions/<its-name>.html` → render the whole project: `tools\render-all.ps1 <project>`

---

## After saving (any shape)
The render auto-runs the alpha check and must print **`[PASS]`**. If it says alpha is
flattened or the frame is empty, the timing/transparency is wrong — fix and re-render.
Outputs land in `projects/<project>/renders/`.
