# Trilium Sync Logging

- `scripts/sync_to_trilium.py` writes local JSONL event logs for each run.
- Default log directory: `.trilium-sync-logs/`; override with `--log-dir`.
- Log files are named from the run start timestamp, e.g. `sync-YYYY-MM-DDTHH-MM-SS-08-00.jsonl`.
- Events include `start`, `dry-run`, `recover`, `create`, `update`, `skip`, `orphan`, `summary`, and `error` where applicable.
- Event fields use JSON-friendly camelCase for durable fields such as `runId`, `startedAt`, `noteId`, `hashBefore`, `hashAfter`, `rootNoteId`, `statePath`, `templateVersionBefore`, `templateVersionAfter`.
- Trilium note metadata is rendered as `<aside class="admonition note">` with Chinese labels `同步信息`, `来源路径：`, `同步时间：`; display time format is `YYYY-MM-DD HH:MM:SS`.
- `CONTENT_TEMPLATE_VERSION` forces existing notes to refresh when the generated HTML template changes, even if Markdown file hashes are unchanged; directory notes participate in the same version check.
- `extract_source_path()` must support both the new Chinese admonition metadata and legacy English `Source path` metadata, because older synced notes may still exist in Trilium.
- 2026-07-11 incident: a real sync ran without an existing usable `.trilium-sync-map.json`, creating a duplicate top-level Trilium tree. User chose to keep the newer state-mapped tree. Old 2026-07-10 top-level notes deleted: `C87dYtIENJfv`, `5IE5Dbu8iKfm`, `9ej2Q3BT9Rqy`, `refxGiWjz7sU`, `POGQRFCSxnzh`, `iQ64uamPzpju`, `DGnxrML4AVP4`. Post-cleanup root has 7 children and no duplicate titles.
- `.trilium-sync-map.json` is intended to be committed for this private repo so another computer can keep path-to-noteId/hash/templateVersion state and avoid duplicate creation.
- Before future real syncs against an already-populated Trilium root without the committed map, run `--rebuild-state` first to avoid duplicate creation.
- `.trilium-sync-logs/`, `.env`, `__pycache__/`, and `*.pyc` are ignored locally; `.env` contains secrets and must not be committed.