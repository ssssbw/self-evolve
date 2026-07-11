# Trilium Sync Logging

- `scripts/sync_to_trilium.py` writes local JSONL event logs for each run.
- Unix/macOS root `./sync` is the one-command entrypoint for real sync. Windows root `sync.cmd` is the equivalent command prompt entrypoint. Both require local `.env`, then run `scripts/sync_to_trilium.py` with forwarded args; pass `--dry-run` to preview.
- Local `.env` is loaded by `scripts/sync_to_trilium.py` without external dependencies. CLI flags still override environment variables; `.env` does not override already-set OS environment variables.
- `.env.example` documents required keys: `TRILIUM_HOST`, `TRILIUM_ROOT_NOTE_ID`, `TRILIUM_TOKEN`; optional tuning keys: `TRILIUM_SYNC_TIMEOUT`, `TRILIUM_SYNC_RETRIES`, `TRILIUM_SYNC_RETRY_DELAY`, `TRILIUM_SYNC_REQUEST_DELAY`, `TRILIUM_SYNC_LOG_DIR`.
- Default log directory: `.trilium-sync-logs/`; override with `--log-dir` or `TRILIUM_SYNC_LOG_DIR`.
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