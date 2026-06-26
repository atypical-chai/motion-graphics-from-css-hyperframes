# `example` — sample project (start here)

This is a **working sample** showing how a project is laid out. Your own real
projects (shows, clients) live next to this one but are **git-ignored** — they
stay on your machine and are never pushed. Copy this folder to begin a new one.

## What's in a project
```
example/
├─ css-sandbox/      ← DESIGN: browser preview pages to iterate the look (never rendered)
│   └─ chapter-break-lab.html   (+ drop a frame.jpg here to preview over footage)
├─ compositions/     ← INPUT: the actual animation .html files that get rendered
│   └─ chapter-break-chip.html  (parameterized: number + title are swappable)
├─ batch/            ← INPUT: .json lists of text values for parameterized designs
│   └─ chapter-breaks.json      (3 sample rows)
└─ renders/          ← OUTPUT: finished .mov/.webm (created on render; git-ignored)
```

## Try it
```powershell
# from the repo root:
tools\render-batch.ps1 example chapter-break-chip chapter-breaks
```
This renders one `.mov` per row of `batch/chapter-breaks.json` into `renders/`,
each auto-verified for a real alpha channel.

## The two ways to work
- **Design lab → lock → render** — sketch the look in `css-sandbox/` first, then
  copy the approved design into `compositions/`. (Phase 0 in `../../WORKFLOW.md`.)
- **Bypass → render** — design already decided? Write the file straight into
  `compositions/` and render.

See the repo root: `README.md`, `WORKFLOW.md`, `GENERATOR-PROMPT.md`, `PROJECT-BRIEF.md`.
