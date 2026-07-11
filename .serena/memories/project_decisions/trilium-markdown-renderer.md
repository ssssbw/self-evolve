# Trilium Markdown Renderer

- 2026-07-11: `scripts/sync_to_trilium.py` switched Markdown rendering from the old handwritten block parser to `markdown-it-py` using `MarkdownIt("commonmark", {"html": False, "breaks": True}).enable("table")`.
- Reason: the handwritten parser split ordered list items with indented unordered sublists into separate `<ol>` blocks, causing Trilium to display every item as `1`.
- Dependency is declared in `requirements.txt`: `markdown-it-py>=3.0.0,<4.0.0`.
- Root `./sync` and Windows `sync.cmd` now create/reuse a project-local `.venv` and install `requirements.txt` automatically when `markdown_it` is missing. `.venv/` is ignored by Git.
- `CONTENT_TEMPLATE_VERSION` was bumped to `3`, so the next real sync will update all existing Trilium notes/directories to refresh generated HTML even if Markdown hashes are unchanged.
- Verification observed: `./sync --dry-run` after the bump reports `Notes needing create/update: 125` (`98` Markdown files + `27` folder notes), which is expected for the template-version refresh.
- Network note: initial dependency installation may need proxy configuration; on this machine non-escalated sandbox PyPI lookup failed, while external network eventually installed `markdown-it-py 3.0.0` after retries.