# Motion Graphic Generator — Project Brief (portable prompt)

> Paste this whole document into a chat to bring an assistant up to speed on my
> motion-graphics pipeline. Its job is to help me turn animation ideas into inputs
> in the EXACT formats below, which I then hand to my coding agent (Cursor) to render.
> Don't invent new formats — produce output that matches one of the three shapes here.

---

## 1. What this system does

It turns **HTML/CSS animations into transparent video** for editing in Premiere Pro.

- **Engine:** HeyGen HyperFrames (headless Chrome renders each frame) + ffmpeg, run from Cursor on Windows.
- **Input:** a self-contained HTML file with a pure-CSS `@keyframes` animation.
- **Output:** `ProRes 4444 .mov` (true alpha channel — the deliverable) and/or small `VP9 .webm` (review copy). Canvas is **1920×1080**.
- **Transparency is real and verified:** every render is auto-checked at the pixel level (it fails loudly if the alpha was silently flattened or the frame came out empty). Validated pixel-for-pixel against a known-good ProRes reference (99%+ identical; only sub-pixel anti-aliased edges differ).
- **Scales three ways** (see §3): one clip; one design rendered with many text values (batch); or many different designs at once.
- **Organized by project:** work lives in `projects/<name>/` (e.g. `podcast`), all driven by one shared engine. Adding a new show = a new folder, not a new setup.

### What it does NOT need / does NOT do
- **No GSAP / JavaScript animation.** Motion is pure CSS `@keyframes`. (A tiny, fixed JS snippet is used ONLY to inject swappable text in the parameterized format — it never animates.)
- **No motion graphics "by description" magic** — the actual look comes from the HTML/CSS you provide. Be concrete about layout, colors, motion, and timing.
- One animation = one HTML file. (Compositing several clips into a single video is a separate advanced feature, not covered here.)
- Embedding video/audio is advanced and out of scope for now — assume vector/text/shape/CSS graphics.

---

## 2. The contract — the "timestamp rule" (EVERY file must follow this)

These rules are what make a file render correctly. The most important is **`data-duration`** —
without it the render fails with "zero duration."

1. **Root element**, exactly this shape, with `data-duration` in **seconds**:
   ```html
   <div id="root" data-composition-id="UNIQUE_NAME" data-start="0" data-duration="<SECONDS>" data-width="1920" data-height="1080">
   ```
2. **Transparent background** so the export keeps an alpha channel:
   ```css
   html,body{ margin:0; padding:0; background:transparent; }
   ```
3. **Animate with pure CSS `@keyframes` only.** No GSAP, no JS animation libraries.
4. **Every animated element** gets a stable `id` AND the clip attributes:
   ```html
   <div id="hero" class="... clip" data-start="0" data-duration="<SECONDS>" data-track-index="0">
   ```
   (Increment `data-track-index` for stacked/overlapping elements.)
5. The CSS `animation-duration` should **match `data-duration`** for one clean loop.
6. **1920×1080**, absolute positioning. A Google Fonts `<link>` is fine.
7. **Brand palette** (use these CSS variables; don't invent colors unless I ask):
   ```css
   --kraft:#ECE2CF; --paper:#F3ECDB; --cream:#F6EDD6; --ink:#232A3A;
   --green:#3F8A5A; --blue:#2F5AA8; --yellow:#E6B53C; --coral:#DF8A64;
   ```
8. At the **visual midpoint** of the animation, the main element must be fully on-screen (that's the frame I spot-check).

---

## 3. The three input formats

Whatever I ask for, give me output in ONE of these shapes. Each says where the file goes and how it's rendered (`<project>` = a folder under `projects/`, e.g. `podcast`).

### FORMAT 1 — one design, one fixed text
A single self-contained HTML file (following the contract). The text is hard-coded.
- **Save as:** `projects/<project>/compositions/<name>.html`
- **Render:** `tools\render.ps1 <project> <name>`

Skeleton:
```html
<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
  :root{ --cream:#F6EDD6; --ink:#232A3A; /* …palette… */ }
  *{box-sizing:border-box;} html,body{margin:0;padding:0;background:transparent;}
  .strip{ position:absolute; bottom:0; left:0; background:var(--cream);
          padding:22px 49px; animation: loop 4s ease-in-out infinite; }
  .strip span{ font-family:'Space Mono',monospace; color:var(--ink); font-size:31px; }
  @keyframes loop{ 0%{transform:translateX(-110%);} 10%,70%{transform:translateX(0);} 80%,100%{transform:translateX(-110%);} }
</style></head>
<body>
  <div id="root" data-composition-id="chapter-break-b" data-start="0" data-duration="4" data-width="1920" data-height="1080">
    <div id="strip" class="strip clip" data-start="0" data-duration="4" data-track-index="0">
      <span>03 &middot; PAYING THE VENDOR</span>
    </div>
  </div>
</body></html>
```

### FORMAT 2 — one design, MANY text values (parameterized + batch)
Use when the design is identical and only the words change (e.g. 15 chapter cards).
The text becomes **variables**; a JSON file lists the rows.
- **Save HTML as:** `projects/<project>/compositions/<name>.html`
- **Save list as:** `projects/<project>/batch/<name>.json`
- **Render all rows:** `tools\render-batch.ps1 <project> <name> <name>`

Two extra requirements on top of the contract:
- Declare the swappable fields on the `<html>` tag:
  ```html
  <html lang="en" data-composition-variables='[
    {"id":"num","type":"string","label":"Number","default":"03"},
    {"id":"title","type":"string","label":"Title","default":"PAYING THE VENDOR"}
  ]'>
  ```
- Give each text element a stable `id`, and at the END of `<body>` add this fixed snippet (reads the values once, fills the text — it does NOT animate):
  ```html
  <span><span id="ch-num">03</span> &middot; <span id="ch-title">PAYING THE VENDOR</span></span>
  ...
  <script>
    const v = window.__hyperframes.getVariables();
    document.getElementById('ch-num').textContent = v.num;
    document.getElementById('ch-title').textContent = v.title;
  </script>
  ```

The JSON list — one row per output (`out` = output file name, plus one key per variable):
```json
[
  { "out": "ch-03-paying-the-vendor", "num": "03", "title": "PAYING THE VENDOR" },
  { "out": "ch-04-the-negotiation",   "num": "04", "title": "THE NEGOTIATION" },
  { "out": "ch-05-closing-the-deal",  "num": "05", "title": "CLOSING THE DEAL" }
]
```

### FORMAT 3 — many DIFFERENT designs
Use when the clips look different from each other (e.g. an intro card + a lower-third + an outro).
Return **each design as its own complete HTML file** (each obeys the contract, each with a unique `data-composition-id`). Label them clearly; do NOT merge them into one document.
- **Save each as:** `projects/<project>/compositions/<its-name>.html`
- **Render the whole project:** `tools\render-all.ps1 <project>`

---

## 4. What I get back
Verified `.mov` files (and optional `.webm`) in `projects/<project>/renders/`, each confirmed to
have a real alpha channel, ready to drag into Premiere.

## 5. How to use this with me (the assistant reading this)
There are two entry points:

- **Design not decided yet → use the design lab first.** Before producing a final
  composition, iterate the LOOK in `projects/<project>/css-sandbox/`: build throwaway
  browser preview pages (a side-by-side gallery of variations and/or a single tunable
  test page) over a real `frame.jpg` still, so I can judge designs against actual
  footage. Every animated sandbox page gets a `▶ Replay` button for testing. These
  files are NEVER rendered — only `compositions/` files are. Once I approve a design,
  copy that look into a real composition and proceed below.
- **Design already decided → skip the lab** and go straight to producing the composition.

When I describe an animation, help me:
1. Pick the right format (1, 2, or 3) for what I'm trying to do.
2. Nail down the concrete details the pipeline needs: **exact text, layout/position, colors (from the palette), the motion, and the total duration in seconds.**
3. Produce the HTML (and JSON list, for Format 2) in the exact shape above, ready for me to drop into the project and render.
Always include `data-duration`, keep the background transparent, and keep motion pure-CSS.
