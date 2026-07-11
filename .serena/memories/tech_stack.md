# Tech Stack

- Repository is mostly Markdown; no app build pipeline.
- Python utility scripts live under `scripts/`; current Trilium sync entrypoint is `scripts/sync_to_trilium.py`.
- Trilium sync uses Trilium ETAPI over HTTP with env vars: `TRILIUM_HOST`, `TRILIUM_TOKEN`, `TRILIUM_ROOT_NOTE_ID`.
- Current Trilium sync state defaults to `.trilium-sync-state.json` and maps source paths to note IDs/hashes.
- Network issues may require proxy env vars using local proxy port `7897`; MCP tools do not inherit system proxy automatically.