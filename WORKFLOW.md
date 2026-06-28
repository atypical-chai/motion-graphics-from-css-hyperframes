# Workflow & gotchas

Structure and "where things go" live in `README.md`. The input *format* lives in
`GENERATOR-PROMPT.md`. This file is the deeper how-to + the traps to avoid.

## Phase 0 — Design lab (path A, optional: when you don't know the look yet)
Do this in `projects/<project>/css-sandbox/` *before* writing any composition.
The whole point: iterate the LOOK cheaply in a normal browser, instead of
spending render time to find out a design doesn't work.

1. **Brief.** You describe the graphic (or paste a prompt with the design context).
2. **Backdrop.** Drop a real still from the show into the sandbox folder named
   `frame.jpg` (1920×1080 ideal) so designs are judged over actual footage.
   Transparent renders are invisible in a browser, so the sandbox fakes the
   background on purpose.
3. **Lab page.** The assistant builds a throwaway preview HTML in `css-sandbox/`
   (e.g. a side-by-side gallery of variations, or a single tunable test page).
   Open it by double-clicking it; refresh after any change.
4. **Iterate.** Compare, mix, nudge position/colors/motion together until a
   direction is locked. Use the controls (sliders, etc.) to read off exact values.
5. **Lock → leave the sandbox.** The approved look is copied into a real
   composition (`compositions/`) with the contract attributes, then rendered
   (Phase 1 below).

**Sandbox ground rules**
- **Replay button.** Every sandbox page that animates gets a `▶ Replay` button so
  you can re-watch the entrance on demand (a one-shot play-once is truer to the
  final render than an infinite loop). The button is sandbox-only — it's dropped
  when the design is moved to a composition.
- **Never rendered.** Files in `css-sandbox/` are for your eyes only; only
  `compositions/` files become video. Match the sandbox's real pixel sizes
  (font-size, padding) so the scaled-down preview is proportionally accurate.

## Phase 1 — The loop for each clip
(Start here directly for **path B / bypass**, when the design is already decided.)
1. **Generate / author** the composition HTML with your AI (`GENERATOR-PROMPT.md`),
   copy `templates/_TEMPLATE.html`, or paste the locked design from Phase 0.
2. **Save** it under the project: `projects/<project>/compositions/<name>.html`
   (unique `data-composition-id`, correct `data-duration` in seconds).
3. **Preview** (optional, live): `npx hyperframes preview -c projects/<project>/compositions/<name>.html` → open the URL it prints.
4. **Render + verify**:
   - one clip:        `tools\render.ps1 <project> <name>`        (add `-WebM` for a small review copy)
   - one design × N texts: `tools\render-batch.ps1 <project> <name> <batchfile>`
   - every clip in a project: `tools\render-all.ps1 <project>`
5. **Confirm** the verify prints `[PASS]`, then drag `projects/<project>/renders/<name>.mov` into Premiere.

## Phase 2 — Save the finished clip to the template library (optional, recommended)
Once a design is locked and rendered, keep it as a reusable **template** so it's easy
to find and reuse on the next episode/project.

1. **Make a looping preview.** A self-contained HTML that plays the animation over a
   neutral placeholder backdrop (no real footage/guest photos), with a 1–2 line
   "where it's used" note embedded in the file (header comment + a small on-page caption).
2. **Save two copies:**
   - `projects/<project>/templates/<name>.html` — local copy (git-ignored with the project).
   - `templates/<project>/<name>.html` — tracked, global copy (the shared library).
3. **Update the galleries.** Each `templates/.../index.html` lists the clips with a live
   mini-preview; add a card for the new template. The global `templates/index.html`
   links to each project's gallery.
4. Remember: the template is only a *preview of the look*. The render-ready source stays
   in `compositions/` — the template's header comment should point back to it.

## What you bring me
Either:
- **A design brief** (rough idea, references, or a prompt with design context) — and we
  iterate in the **css-sandbox** (Phase 0) until the look is locked, *then* I build and
  render the composition; or
- **A decided design** (description or HTML/CSS draft) in one of the three shapes in
  `GENERATOR-PROMPT.md` — and I skip the sandbox, build the composition file(s) under the
  right project, render, and verify the alpha (Phase 1).

Either way you get back verified `.mov` files in `renders/`.

## The traps (all handled for you)
- **"Zero duration" render failure** → every root needs `data-duration="<seconds>"`. The template + contract enforce it.
- **Silently flattened / empty alpha** → never trust "render succeeded"; the render tools always run the real-pixel check (`verify_alpha.py`).
- **Windows + variables** → inline `--variables` JSON gets mangled by PowerShell, and `Set-Content -Encoding utf8` adds a BOM that breaks parsing. `render-batch.ps1` writes a BOM-less temp file and uses `--variables-file`. You just edit the JSON.
- **(New machine only) browser unzip hangs** → if HyperFrames hangs on "Downloading Chrome", manually unzip its downloaded zip in `~/.cache/hyperframes/chrome/...` with `Expand-Archive`, then `npx hyperframes browser ensure`.

## Format notes
- **MOV (ProRes 4444)** = your transparent deliverable. Reliable alpha. Default.
- **WebM (VP9)** = tiny review/web copy; alpha works but is fragile to verify — the tool handles it.
- **GSAP** is only worth it if render speed becomes a bottleneck (pure CSS pays a ~45s/clip wait). Not needed for correctness — author in CSS, let the verify gate guard you.

## Adding a new project
Make `projects/<new-project>/{compositions,batch,renders}` and work the same way.
The engine (`.agents/`, browser, config) is shared — never duplicated per project.
