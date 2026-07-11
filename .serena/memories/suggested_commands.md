# Suggested Commands

- `rg --files`: list knowledge-base files quickly.
- `git status --short`: check dirty worktree before edits.
- `git diff -- <path>`: inspect scoped Markdown/script changes.
- `find . -name "*.md" -maxdepth 4`: inspect Markdown layout by depth.
- `fvm dart format` / `fvm flutter analyze` may appear in other user projects, but this repo currently has no Flutter pipeline.
- Trilium sync examples usually run `python3 scripts/sync_to_trilium.py` with `TRILIUM_HOST`, `TRILIUM_TOKEN`, `TRILIUM_ROOT_NOTE_ID`; use existing script help for exact flags.