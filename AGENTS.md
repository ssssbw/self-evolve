# Repository Guidelines

## Project Structure & Module Organization

This repository is a Markdown-based personal knowledge base organized with the PARA method. Treat Markdown files as the primary source content.

- `0-Projects/`: active projects with clear goals, plans, and project notes.
- `1-Areas/`: long-term domains such as `A1-技术`, `A2-理财`, and `A3-认知`.
- `2-Resources/`: reference indexes for tools, reading lists, and courses.
- `3-Archive/`: completed or inactive material moved out of active work.
- `4-Journal/`: recurring reviews, split into `weekly/`, `monthly/`, and `yearly/`.
- `5-Playground/`: homework, discussions, and challenges.
- `.ai/`: AI handoff context and session notes; consult it before continuing prior work.

## Build, Test, and Development Commands

There is no application build pipeline. Use lightweight repository checks:

- `rg --files`: list tracked content paths quickly.
- `git status --short`: review pending changes before editing or committing.
- `git diff -- README.md 0-Projects/`: inspect content changes in key areas.
- `find . -name "*.md" -maxdepth 4`: locate Markdown files by structure.

## Coding Style & Naming Conventions

Use Markdown with clear headings, short paragraphs, and actionable bullet lists. Preserve the existing numeric top-level directory prefixes (`0-Projects`, `1-Areas`, etc.) and Chinese domain names. Name project folders with an ID plus title, for example `P001-CS基础重建`. For dated journal entries, follow existing patterns such as `2026-W17.md`. Keep filenames descriptive, stable, and easy to sort.

## Testing Guidelines

No automated tests are configured. Before submitting changes, manually verify links, headings, and table formatting in the edited Markdown files. Confirm new notes are placed in the correct PARA section and that index files such as `_index.md` are updated when discoverability would otherwise suffer.

## Commit & Pull Request Guidelines

Recent history uses concise conventional-style prefixes, for example `init:` and `feat:`. Continue this pattern with short Chinese or English summaries, such as `feat: 添加月度复盘模板` or `docs: update resource index`. Pull requests should describe the intent, list affected directories, mention any moved or archived content, and include screenshots only when visual Markdown rendering is important.

## Agent-Specific Instructions

Before making repository changes, read `README.md` and relevant `.ai/` context when available. Keep edits narrowly scoped, avoid reorganizing unrelated notes, and do not overwrite existing personal content unless explicitly requested.
