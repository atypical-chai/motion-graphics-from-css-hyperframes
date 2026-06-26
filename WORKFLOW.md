# Workflow & gotchas

Structure and "where things go" live in `README.md`. The input *format* lives in
`GENERATOR-PROMPT.md`. This file is the deeper how-to + the traps to avoid.

## The loop for each clip
1. **Generate** HTML with your AI (`GENERATOR-PROMPT.md`) or copy `templates/_TEMPLATE.html`.
2. **Save** it under the project: `projects/<project>/compositions/<name>.html`
   (unique `data-composition-id`, correct `data-duration` in seconds).
3. **Preview** (optional, live): `npx hyperframes preview -c projects/<project>/compositions/<name>.html` → open the URL it prints.
4. **Render + verify**:
   - one clip:        `tools\render.ps1 <project> <name>`        (add `-WebM` for a small review copy)
   - one design × N texts: `tools\render-batch.ps1 <project> <name> <batchfile>`
   - every clip in a project: `tools\render-all.ps1 <project>`
5. **Confirm** the verify prints `[PASS]`, then drag `projects/<project>/renders/<name>.mov` into Premiere.

## What you bring me
Just the **animation description** (or a rough HTML/CSS draft) in one of the three shapes
in `GENERATOR-PROMPT.md`. I turn it into composition file(s) under the right project,
render, and verify the alpha — then hand you the `.mov`.

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
