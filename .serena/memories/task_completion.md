# Task Completion

- Markdown-only edits: manually verify headings, tables, links, PARA placement, and relevant `_index.md` discoverability.
- Python script edits: run focused script tests/checks when present; at minimum run syntax/import validation such as `python3 -m py_compile scripts/<script>.py` if no test suite exists.
- For Trilium sync changes, prefer dry-run or isolated state-file checks before real ETAPI writes; real sync requires valid env vars and may need proxy handling.
- Always finish with `git status --short` and summarize changed files plus verification performed.
- After memory changes, user can run `serena memories check` from project root to validate memory references.