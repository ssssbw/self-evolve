# Trilium Orphan Pruning

- 2026-07-11: Added explicit orphan cleanup support to `scripts/sync_to_trilium.py`.
- Default behavior remains conservative: orphaned Trilium notes are only reported and left untouched unless `--prune-orphans` is provided.
- Preview cleanup: `./sync --prune-orphans --dry-run` lists orphaned notes that would be deleted, without changing Trilium or `.trilium-sync-map.json`.
- Real cleanup: `./sync --prune-orphans` deletes Trilium notes whose source paths no longer exist locally and removes their entries from `.trilium-sync-map.json`.
- The implementation uses `TriliumClient.delete_note()` and `prune_orphans()`, recording `prune` events with `reason=missing-source-path`.
- `README.md` now documents normal sync, dry-run, orphan detection, preview cleanup, and real cleanup.
- Verification after adding this feature: `./.venv/bin/python -m unittest discover -s tests -p 'test_*.py'` passed 16 tests; `./sync --dry-run` and `./sync --prune-orphans --dry-run` both succeeded. At that point only `README.md` needed update due documentation edits, and no orphan warnings were printed.