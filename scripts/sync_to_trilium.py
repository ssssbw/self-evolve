#!/usr/bin/env python3
"""Sync selected Markdown notes from this repository to Trilium.

This script is intentionally one-way:

    Git / Markdown -> Trilium

Trilium is treated as a read-only mirror. The script stores local sync state in
`.trilium-sync-map.json` so path-to-note mappings can be reused across machines.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import html
import json
import os
from pathlib import Path
import re
import sys
import time
from typing import Any
from urllib import error, parse, request

try:
    from markdown_it import MarkdownIt
except ImportError:
    MarkdownIt = None  # type: ignore[assignment]


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_STATE_PATH = REPO_ROOT / ".trilium-sync-map.json"
DEFAULT_LOG_DIR = REPO_ROOT / ".trilium-sync-logs"
DEFAULT_USER_AGENT = "self-evolve-trilium-sync/0.1"

INCLUDE_PATHS = [
    "README.md",
    "0-Projects",
    "1-Areas",
    "2-Resources",
    "4-Journal",
    "5-Playground",
    "guideline",
]

EXCLUDED_DIRS = {
    ".git",
    ".ai",
    ".spec-workflow",
    ".playwright-mcp",
    ".sisyphus",
    "电子书",
}

SYNC_NOTICE = "本笔记由 self-evolve Git 仓库同步，请勿在 Trilium 端编辑。"
CONTENT_TEMPLATE_VERSION = 3
_MARKDOWN_RENDERER: Any = None


class ConfigError(RuntimeError):
    pass


class SyncEventLogger:
    FIELD_ALIASES = {
        "content_template_version": "contentTemplateVersion",
        "error_type": "errorType",
        "folder_notes": "folderNotes",
        "hash_after": "hashAfter",
        "hash_before": "hashBefore",
        "markdown_files": "markdownFiles",
        "note_id": "noteId",
        "previous_note_id": "previousNoteId",
        "prune_orphans": "pruneOrphans",
        "request_delay": "requestDelay",
        "rebuild_state": "rebuildState",
        "retry_delay": "retryDelay",
        "root_note_id": "rootNoteId",
        "skipped_dirs": "skippedDirs",
        "state_path": "statePath",
        "template_version_after": "templateVersionAfter",
        "template_version_before": "templateVersionBefore",
    }

    def __init__(self, log_path: Path, run_id: str, started_at: str) -> None:
        self.log_path = log_path
        self.run_id = run_id
        self.started_at = started_at
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def record(self, event: str, **fields: Any) -> None:
        payload: dict[str, Any] = {
            "timestamp": now_iso(),
            "runId": self.run_id,
            "startedAt": self.started_at,
            "event": event,
        }
        payload.update(self._normalize_fields(fields))
        with self.log_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")

    @classmethod
    def _normalize_fields(cls, fields: dict[str, Any]) -> dict[str, Any]:
        return {cls.FIELD_ALIASES.get(key, key): value for key, value in fields.items()}


class TriliumClient:
    def __init__(
        self,
        host: str,
        token: str,
        timeout: int = 20,
        retries: int = 3,
        retry_delay: int = 10,
        request_delay: float = 0.2,
    ) -> None:
        self.host = host.rstrip("/")
        self.token = token
        self.timeout = timeout
        self.retries = retries
        self.retry_delay = retry_delay
        self.request_delay = request_delay

    def _request(
        self,
        method: str,
        path: str,
        *,
        json_body: dict[str, Any] | None = None,
        raw_body: str | None = None,
        content_type: str = "application/json",
    ) -> Any:
        url = f"{self.host}{path}"
        headers = {
            "Authorization": self.token,
            "Accept": "application/json",
            "User-Agent": DEFAULT_USER_AGENT,
        }
        data: bytes | None = None

        if json_body is not None:
            data = json.dumps(json_body).encode("utf-8")
            headers["Content-Type"] = "application/json; charset=utf-8"
        elif raw_body is not None:
            data = raw_body.encode("utf-8")
            headers["Content-Type"] = content_type

        req = request.Request(url, data=data, headers=headers, method=method)

        for attempt in range(self.retries + 1):
            try:
                with request.urlopen(req, timeout=self.timeout) as response:
                    body = response.read()
                    if self.request_delay > 0:
                        time.sleep(self.request_delay)
                    if not body:
                        return None
                    response_type = response.headers.get("Content-Type", "")
                    if "application/json" in response_type:
                        return json.loads(body.decode("utf-8"))
                    return body.decode("utf-8")
            except error.HTTPError as exc:
                body = exc.read().decode("utf-8", errors="replace")
                if exc.code in {429, 500, 502, 503, 504} and attempt < self.retries:
                    delay = retry_delay_from_response(body, self.retry_delay)
                    log(
                        f"Retry {attempt + 1}/{self.retries} after HTTP {exc.code} "
                        f"on {method} {path}; waiting {delay}s"
                    )
                    time.sleep(delay)
                    continue
                raise RuntimeError(
                    f"Trilium API {method} {path} failed: HTTP {exc.code} {body}"
                ) from exc
            except error.URLError as exc:
                if attempt < self.retries:
                    delay = self.retry_delay
                    log(
                        f"Retry {attempt + 1}/{self.retries} after network error "
                        f"on {method} {path}; waiting {delay}s"
                    )
                    time.sleep(delay)
                    continue
                raise RuntimeError(f"Cannot connect to Trilium at {self.host}: {exc}") from exc

        raise RuntimeError(f"Trilium API {method} {path} failed after retries")

    def get_note(self, note_id: str) -> Any:
        return self._request("GET", f"/etapi/notes/{parse.quote(note_id)}")

    def get_note_content(self, note_id: str) -> str:
        content = self._request("GET", f"/etapi/notes/{parse.quote(note_id)}/content")
        return content if isinstance(content, str) else ""

    def create_text_note(self, parent_note_id: str, title: str, content: str) -> str:
        payload = {
            "parentNoteId": parent_note_id,
            "title": title,
            "type": "text",
            "mime": "text/html",
            "content": content,
        }
        response = self._request("POST", "/etapi/create-note", json_body=payload)
        note_id = extract_note_id(response)
        if not note_id:
            raise RuntimeError(f"Cannot find noteId in Trilium response: {response!r}")
        return note_id

    def update_note_content(self, note_id: str, content: str) -> None:
        self._request(
            "PUT",
            f"/etapi/notes/{parse.quote(note_id)}/content",
            raw_body=content,
            content_type="text/plain; charset=utf-8",
        )

    def delete_note(self, note_id: str) -> None:
        self._request("DELETE", f"/etapi/notes/{parse.quote(note_id)}")


def parse_dotenv_value(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def load_dotenv(path: Path = REPO_ROOT / ".env") -> dict[str, str]:
    if not path.exists():
        return {}

    loaded: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if not key or key in os.environ:
            continue
        parsed_value = parse_dotenv_value(value)
        os.environ[key] = parsed_value
        loaded[key] = parsed_value
    return loaded


def env_int(name: str, default: int) -> int:
    value = os.environ.get(name)
    if value is None or value == "":
        return default
    try:
        return int(value)
    except ValueError as exc:
        raise ConfigError(f"Invalid integer for {name}: {value}") from exc


def env_float(name: str, default: float) -> float:
    value = os.environ.get(name)
    if value is None or value == "":
        return default
    try:
        return float(value)
    except ValueError as exc:
        raise ConfigError(f"Invalid number for {name}: {value}") from exc


def extract_note_id(response: Any) -> str | None:
    if isinstance(response, dict):
        if isinstance(response.get("noteId"), str):
            return response["noteId"]
        note = response.get("note")
        if isinstance(note, dict) and isinstance(note.get("noteId"), str):
            return note["noteId"]
        branch = response.get("branch")
        if isinstance(branch, dict) and isinstance(branch.get("noteId"), str):
            return branch["noteId"]
    return None


def relative_path(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def is_excluded(path: Path) -> bool:
    try:
        rel_parts = path.relative_to(REPO_ROOT).parts
    except ValueError:
        return True
    return any(part in EXCLUDED_DIRS for part in rel_parts)


def markdown_files() -> list[Path]:
    files: list[Path] = []
    for path_text in INCLUDE_PATHS:
        path = REPO_ROOT / path_text
        if not path.exists():
            continue
        if path.is_file() and path.suffix == ".md" and not is_excluded(path):
            files.append(path)
            continue
        if path.is_dir() and not is_excluded(path):
            for candidate in path.rglob("*.md"):
                if candidate.is_file() and not is_excluded(candidate):
                    files.append(candidate)
    return sorted(files, key=lambda item: relative_path(item))


def parent_dirs_for(files: list[Path]) -> list[Path]:
    dirs: set[Path] = set()
    for path_text in INCLUDE_PATHS:
        path = REPO_ROOT / path_text
        if path.is_dir() and not is_excluded(path):
            dirs.add(path)
    for note_file in files:
        current = note_file.parent
        while current != REPO_ROOT:
            if not is_excluded(current):
                dirs.add(current)
            current = current.parent
    return sorted(dirs, key=lambda item: (len(relative_path(item).split("/")), relative_path(item)))


def load_state(path: Path, root_note_id: str) -> dict[str, Any]:
    if not path.exists():
        return {"version": 1, "rootNoteId": root_note_id, "items": {}}

    with path.open("r", encoding="utf-8") as handle:
        state = json.load(handle)

    if not isinstance(state, dict) or not isinstance(state.get("items"), dict):
        raise ConfigError(f"Invalid sync state file: {path}")

    state.setdefault("version", 1)
    state.setdefault("rootNoteId", root_note_id)
    return state


def save_state(path: Path, state: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(state, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def title_for_path(path: Path) -> str:
    if path.is_file():
        return path.stem
    return path.name


def now_display() -> str:
    return dt.datetime.now(dt.timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S")


def sync_info_html(rel_path: str, synced_at: str | None = None) -> str:
    escaped_path = html.escape(rel_path)
    escaped_synced_at = html.escape(synced_at or now_display())
    return (
        "<aside class=\"admonition note\">"
        "<p><strong>同步信息</strong></p>"
        f"<p><strong>来源路径：</strong><code>{escaped_path}</code></p>"
        f"<p><strong>同步时间：</strong><code>{escaped_synced_at}</code></p>"
        "</aside>"
    )


def folder_html(rel_path: str, title: str) -> str:
    escaped_title = html.escape(title)
    return f"<h1>{escaped_title}</h1>" f"{sync_info_html(rel_path)}"


def note_html(markdown: str, rel_path: str) -> str:
    return f"{sync_info_html(rel_path)}" "<hr>" f"{markdown_to_html(markdown)}"


def needs_content_update(existing: dict[str, Any] | None, current_hash: str | None = None) -> bool:
    if existing is None:
        return True
    if existing.get("templateVersion") != CONTENT_TEMPLATE_VERSION:
        return True
    if current_hash is not None and existing.get("hash") != current_hash:
        return True
    return False


def current_source_paths(files: list[Path], dirs: list[Path]) -> set[str]:
    return {relative_path(path) for path in files} | {relative_path(path) for path in dirs}


def find_orphaned_paths(items: dict[str, dict[str, Any]], source_paths: set[str]) -> list[str]:
    return sorted(path for path in items if path not in source_paths)


def prune_orphans(
    client: Any,
    state: dict[str, Any],
    orphaned: list[str],
    state_path: Path,
    event_logger: SyncEventLogger,
) -> int:
    items = state["items"]
    pruned = 0
    for path in orphaned:
        item = items.get(path)
        if item is None:
            continue
        note_id = item.get("noteId")
        if not note_id:
            continue
        client.delete_note(note_id)
        event_logger.record(
            "prune",
            kind=item.get("kind"),
            path=path,
            title=item.get("title"),
            note_id=note_id,
            reason="missing-source-path",
        )
        del items[path]
        state["lastSyncedAt"] = now_iso()
        save_state(state_path, state)
        pruned += 1
        log(f"PRUNE orphan {path}")
    return pruned


def markdown_renderer() -> Any:
    global _MARKDOWN_RENDERER
    if MarkdownIt is None:
        raise ConfigError(
            "缺少 Python 依赖 markdown-it-py。请先运行: python3 -m pip install -r requirements.txt"
        )
    if _MARKDOWN_RENDERER is None:
        _MARKDOWN_RENDERER = MarkdownIt(
            "commonmark",
            {
                "html": False,
                "breaks": True,
            },
        ).enable("table")
    return _MARKDOWN_RENDERER


def markdown_to_html(markdown: str) -> str:
    return markdown_renderer().render(markdown).strip()


def log(message: str) -> None:
    print(message, flush=True)


def safe_log_timestamp(value: str) -> str:
    return re.sub(r"[^0-9A-Za-z._-]+", "-", value).strip("-")


def event_log_path(log_dir: Path, started_at: str) -> Path:
    return log_dir / f"sync-{safe_log_timestamp(started_at)}.jsonl"


def retry_delay_from_response(body: str, default_delay: int) -> int:
    try:
        parsed = json.loads(body)
    except json.JSONDecodeError:
        return default_delay
    retry_after = parsed.get("retry_after")
    if isinstance(retry_after, int):
        return max(1, min(retry_after, 60))
    return default_delay


def extract_source_path(content: str) -> str | None:
    patterns = [
        r"<strong>\s*来源路径：\s*</strong>\s*<code>\s*(.*?)\s*</code>",
        r"<strong>\s*Source path:\s*</strong>\s*<code>\s*(.*?)\s*</code>",
    ]
    for pattern in patterns:
        match = re.search(pattern, content)
        if match:
            return html.unescape(match.group(1).strip())
    return None


def rebuild_state_from_trilium(
    client: TriliumClient,
    root_note_id: str,
    state: dict[str, Any],
    files: list[Path],
    dirs: list[Path],
    state_path: Path,
    event_logger: SyncEventLogger | None = None,
) -> int:
    expected_files = {relative_path(path): path for path in files}
    expected_dirs = {relative_path(path): path for path in dirs}
    expected_paths = sorted(
        set(expected_files) | set(expected_dirs),
        key=lambda item: (len(item.split("/")), item),
    )
    items = state["items"]
    child_cache: dict[str, list[dict[str, Any]]] = {}
    used_child_ids_by_parent: dict[str, set[str]] = {}
    recovered = 0

    def child_notes(parent_note_id: str) -> list[dict[str, Any]]:
        if parent_note_id in child_cache:
            return child_cache[parent_note_id]
        parent_note = client.get_note(parent_note_id)
        children = [client.get_note(child_id) for child_id in parent_note.get("childNoteIds", [])]
        child_cache[parent_note_id] = children
        return children

    for source_path in expected_paths:
        source = expected_files.get(source_path) or expected_dirs[source_path]
        parent_path = str(Path(source_path).parent).replace("\\", "/")
        parent_note_id = root_note_id if parent_path == "." else items.get(parent_path, {}).get("noteId")
        if not parent_note_id:
            continue

        used_child_ids = used_child_ids_by_parent.setdefault(parent_note_id, set())
        title = title_for_path(source)
        matching_note = None
        for child in child_notes(parent_note_id):
            child_id = child.get("noteId")
            if child.get("title") == title and child_id not in used_child_ids:
                matching_note = child
                used_child_ids.add(child_id)
                break

        if matching_note is None:
            continue

        note_id = matching_note["noteId"]
        if source_path in expected_files:
            kind = "file"
            item = {
                "kind": kind,
                "noteId": note_id,
                "title": matching_note.get("title", title),
                "hash": file_hash(expected_files[source_path]),
                "lastSyncedAt": now_iso(),
            }
        else:
            kind = "dir"
            item = {
                "kind": kind,
                "noteId": note_id,
                "title": matching_note.get("title", title),
                "lastSyncedAt": now_iso(),
            }

        if items.get(source_path, {}).get("noteId") != note_id:
            previous_note_id = items.get(source_path, {}).get("noteId")
            items[source_path] = item
            recovered += 1
            state["rootNoteId"] = root_note_id
            state["lastRebuiltAt"] = now_iso()
            save_state(state_path, state)
            if event_logger is not None:
                event_logger.record(
                    "recover",
                    kind=kind,
                    path=source_path,
                    title=item["title"],
                    note_id=note_id,
                    previous_note_id=previous_note_id,
                    hash_after=item.get("hash"),
                )
            if recovered % 20 == 0:
                log(f"Recovered {recovered} existing Trilium notes...")

    state["rootNoteId"] = root_note_id
    state["lastRebuiltAt"] = now_iso()
    save_state(state_path, state)
    return recovered


def sync(args: argparse.Namespace) -> int:
    load_dotenv()
    host = args.host or os.environ.get("TRILIUM_HOST", "http://localhost:8080")
    token = args.token or os.environ.get("TRILIUM_TOKEN")
    root_note_id = args.root_note_id or os.environ.get("TRILIUM_ROOT_NOTE_ID")
    state_path = Path(args.state).expanduser() if args.state else DEFAULT_STATE_PATH
    started_at = now_iso()
    log_dir_arg = getattr(args, "log_dir", None)
    log_dir = Path(log_dir_arg).expanduser() if log_dir_arg else DEFAULT_LOG_DIR
    event_logger = SyncEventLogger(
        event_log_path(log_dir, started_at),
        run_id=safe_log_timestamp(started_at),
        started_at=started_at,
    )

    if not root_note_id:
        event_logger.record(
            "error",
            error_type="ConfigError",
            error="Missing TRILIUM_ROOT_NOTE_ID or --root-note-id",
        )
        raise ConfigError("Missing TRILIUM_ROOT_NOTE_ID or --root-note-id")
    if not token and not args.dry_run:
        event_logger.record("error", error_type="ConfigError", error="Missing TRILIUM_TOKEN or --token")
        raise ConfigError("Missing TRILIUM_TOKEN or --token")

    files = markdown_files()
    dirs = parent_dirs_for(files)
    state = load_state(state_path, root_note_id)
    items = state["items"]
    orphaned = find_orphaned_paths(items, current_source_paths(files, dirs))

    print(f"Repository: {REPO_ROOT}")
    print(f"Markdown files: {len(files)}")
    print(f"Folder notes: {len(dirs)}")
    print(f"State file: {state_path}")
    print(f"Event log: {event_logger.log_path}")
    event_logger.record(
        "start",
        repository=str(REPO_ROOT),
        markdown_files=len(files),
        folder_notes=len(dirs),
        state_path=str(state_path),
        root_note_id=root_note_id,
        dry_run=args.dry_run,
        rebuild_state=args.rebuild_state,
        prune_orphans=args.prune_orphans,
        content_template_version=CONTENT_TEMPLATE_VERSION,
        timeout=args.timeout,
        retries=args.retries,
        retry_delay=args.retry_delay,
        request_delay=args.request_delay,
    )

    if args.dry_run:
        changed_notes = []
        for folder in dirs:
            rel = relative_path(folder)
            existing = items.get(rel)
            if not needs_content_update(existing):
                continue
            changed_notes.append(rel)
            event_logger.record(
                "dry-run",
                action="create" if existing is None else "update",
                kind="dir",
                path=rel,
                title=title_for_path(folder),
                note_id=existing.get("noteId") if existing else None,
                template_version_before=existing.get("templateVersion") if existing else None,
                template_version_after=CONTENT_TEMPLATE_VERSION,
            )
        for path in files:
            rel = relative_path(path)
            current_hash = file_hash(path)
            existing = items.get(rel)
            previous_hash = existing.get("hash") if existing else None
            if not needs_content_update(existing, current_hash):
                continue
            changed_notes.append(rel)
            event_logger.record(
                "dry-run",
                action="create" if existing is None else "update",
                kind="file",
                path=rel,
                title=title_for_path(path),
                note_id=existing.get("noteId") if existing else None,
                hash_before=previous_hash,
                hash_after=current_hash,
                template_version_before=existing.get("templateVersion") if existing else None,
                template_version_after=CONTENT_TEMPLATE_VERSION,
            )
        print("Dry run enabled. No Trilium notes will be changed.")
        print(f"Notes needing create/update: {len(changed_notes)}")
        for path in changed_notes[:50]:
            print(f"  - {path}")
        if len(changed_notes) > 50:
            print(f"  ... and {len(changed_notes) - 50} more")
        if orphaned:
            if args.prune_orphans:
                print("Orphaned Trilium notes that would be deleted:")
            else:
                print("Orphaned Trilium notes were left untouched:")
            for path in orphaned[:50]:
                item = items[path]
                event_logger.record(
                    "dry-run" if args.prune_orphans else "orphan",
                    action="prune" if args.prune_orphans else "leave-untouched",
                    kind=item.get("kind"),
                    path=path,
                    title=item.get("title"),
                    note_id=item.get("noteId"),
                    reason="missing-source-path",
                )
                print(f"  - {path}")
            if len(orphaned) > 50:
                print(f"  ... and {len(orphaned) - 50} more")
        event_logger.record(
            "summary",
            dry_run=True,
            changed=len(changed_notes),
            created=0,
            updated=0,
            skipped=len(files) + len(dirs) - len(changed_notes),
            orphaned=len(orphaned),
            pruned=0,
        )
        return 0

    try:
        client = TriliumClient(
            host,
            token or "",
            timeout=args.timeout,
            retries=args.retries,
            retry_delay=args.retry_delay,
            request_delay=args.request_delay,
        )
        client.get_note(root_note_id)

        recovered = 0
        if args.rebuild_state:
            recovered = rebuild_state_from_trilium(
                client,
                root_note_id,
                state,
                files,
                dirs,
                state_path,
                event_logger,
            )
            log(f"Rebuilt state from Trilium. recovered={recovered}")

        created = 0
        updated = 0
        skipped = 0
        skipped_dirs = 0

        for folder in dirs:
            rel = relative_path(folder)
            existing = items.get(rel)
            title = title_for_path(folder)
            if existing is None:
                parent = folder.parent
                parent_note_id = root_note_id if parent == REPO_ROOT else items[relative_path(parent)]["noteId"]
                note_id = client.create_text_note(parent_note_id, title, folder_html(rel, title))
                items[rel] = {
                    "kind": "dir",
                    "noteId": note_id,
                    "title": title,
                    "templateVersion": CONTENT_TEMPLATE_VERSION,
                    "lastSyncedAt": now_iso(),
                }
                state["rootNoteId"] = root_note_id
                state["lastSyncedAt"] = now_iso()
                save_state(state_path, state)
                created += 1
                event_logger.record(
                    "create",
                    kind="dir",
                    path=rel,
                    title=title,
                    note_id=note_id,
                    template_version_after=CONTENT_TEMPLATE_VERSION,
                )
                log(f"CREATE dir  {rel}")
            elif needs_content_update(existing):
                client.update_note_content(existing["noteId"], folder_html(rel, title))
                previous_template_version = existing.get("templateVersion")
                existing["title"] = title
                existing["templateVersion"] = CONTENT_TEMPLATE_VERSION
                existing["lastSyncedAt"] = now_iso()
                state["rootNoteId"] = root_note_id
                state["lastSyncedAt"] = now_iso()
                save_state(state_path, state)
                updated += 1
                event_logger.record(
                    "update",
                    kind="dir",
                    path=rel,
                    title=title,
                    note_id=existing.get("noteId"),
                    template_version_before=previous_template_version,
                    template_version_after=CONTENT_TEMPLATE_VERSION,
                )
                log(f"UPDATE dir  {rel}")
            else:
                skipped_dirs += 1
                event_logger.record(
                    "skip",
                    kind="dir",
                    path=rel,
                    title=existing.get("title", title),
                    note_id=existing.get("noteId"),
                    template_version_before=existing.get("templateVersion"),
                    template_version_after=CONTENT_TEMPLATE_VERSION,
                    reason="unchanged",
                )

        for note_file in files:
            rel = relative_path(note_file)
            current_hash = file_hash(note_file)
            existing = items.get(rel)
            content = note_file.read_text(encoding="utf-8")
            rendered = note_html(content, rel)

            if existing is None:
                parent = note_file.parent
                parent_note_id = root_note_id if parent == REPO_ROOT else items[relative_path(parent)]["noteId"]
                title = title_for_path(note_file)
                note_id = client.create_text_note(parent_note_id, title, rendered)
                items[rel] = {
                    "kind": "file",
                    "noteId": note_id,
                    "title": title,
                    "hash": current_hash,
                    "templateVersion": CONTENT_TEMPLATE_VERSION,
                    "lastSyncedAt": now_iso(),
                }
                state["rootNoteId"] = root_note_id
                state["lastSyncedAt"] = now_iso()
                save_state(state_path, state)
                created += 1
                event_logger.record(
                    "create",
                    kind="file",
                    path=rel,
                    title=title,
                    note_id=note_id,
                    hash_before=None,
                    hash_after=current_hash,
                    template_version_after=CONTENT_TEMPLATE_VERSION,
                )
                log(f"CREATE file {rel}")
            elif needs_content_update(existing, current_hash):
                previous_hash = existing.get("hash")
                previous_template_version = existing.get("templateVersion")
                client.update_note_content(existing["noteId"], rendered)
                existing["hash"] = current_hash
                existing["templateVersion"] = CONTENT_TEMPLATE_VERSION
                existing["lastSyncedAt"] = now_iso()
                state["rootNoteId"] = root_note_id
                state["lastSyncedAt"] = now_iso()
                save_state(state_path, state)
                updated += 1
                event_logger.record(
                    "update",
                    kind="file",
                    path=rel,
                    title=existing.get("title", title_for_path(note_file)),
                    note_id=existing.get("noteId"),
                    hash_before=previous_hash,
                    hash_after=current_hash,
                    template_version_before=previous_template_version,
                    template_version_after=CONTENT_TEMPLATE_VERSION,
                )
                log(f"UPDATE file {rel}")
            else:
                skipped += 1
                event_logger.record(
                    "skip",
                    kind="file",
                    path=rel,
                    title=existing.get("title", title_for_path(note_file)),
                    note_id=existing.get("noteId"),
                    hash_before=current_hash,
                    hash_after=current_hash,
                    template_version_before=existing.get("templateVersion"),
                    template_version_after=CONTENT_TEMPLATE_VERSION,
                    reason="unchanged",
                )

        orphaned = find_orphaned_paths(items, current_source_paths(files, dirs))
        pruned = 0
        if orphaned:
            if args.prune_orphans:
                log("Pruning orphaned Trilium notes:")
                pruned = prune_orphans(client, state, orphaned, state_path, event_logger)
            else:
                log("Orphaned Trilium notes were left untouched:")
                for path in orphaned[:50]:
                    item = items[path]
                    event_logger.record(
                        "orphan",
                        kind=item.get("kind"),
                        path=path,
                        title=item.get("title"),
                        note_id=item.get("noteId"),
                        reason="missing-source-path",
                    )
                    log(f"  - {path}")
                if len(orphaned) > 50:
                    log(f"  ... and {len(orphaned) - 50} more")

        state["rootNoteId"] = root_note_id
        state["lastSyncedAt"] = now_iso()
        save_state(state_path, state)
        event_logger.record(
            "summary",
            dry_run=False,
            recovered=recovered,
            created=created,
            updated=updated,
            skipped=skipped,
            skipped_dirs=skipped_dirs,
            orphaned=len(orphaned),
            pruned=pruned,
        )
        if pruned:
            log(f"Done. created={created}, updated={updated}, skipped={skipped}, pruned={pruned}")
        else:
            log(f"Done. created={created}, updated={updated}, skipped={skipped}")
        return 0
    except Exception as exc:
        event_logger.record("error", error_type=type(exc).__name__, error=str(exc))
        raise


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).astimezone().isoformat(timespec="seconds")


def build_parser() -> argparse.ArgumentParser:
    load_dotenv()
    parser = argparse.ArgumentParser(
        description="Sync selected self-evolve Markdown files to Trilium via ETAPI."
    )
    parser.add_argument("--host", help="Trilium host, default TRILIUM_HOST or http://localhost:8080")
    parser.add_argument("--token", help="Trilium ETAPI token. Prefer TRILIUM_TOKEN.")
    parser.add_argument("--root-note-id", help="Target root note ID. Prefer TRILIUM_ROOT_NOTE_ID.")
    parser.add_argument("--state", help="Sync state path. Default: .trilium-sync-map.json")
    parser.add_argument(
        "--log-dir",
        default=os.environ.get("TRILIUM_SYNC_LOG_DIR", str(DEFAULT_LOG_DIR)),
        help="Directory for JSONL sync event logs. Default: .trilium-sync-logs",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=env_int("TRILIUM_SYNC_TIMEOUT", 20),
        help="HTTP timeout in seconds. Default: 20.",
    )
    parser.add_argument(
        "--retries",
        type=int,
        default=env_int("TRILIUM_SYNC_RETRIES", 3),
        help="Retry count for transient HTTP/network errors.",
    )
    parser.add_argument(
        "--retry-delay",
        type=int,
        default=env_int("TRILIUM_SYNC_RETRY_DELAY", 10),
        help="Retry delay in seconds when server gives no hint.",
    )
    parser.add_argument(
        "--request-delay",
        type=float,
        default=env_float("TRILIUM_SYNC_REQUEST_DELAY", 0.2),
        help="Delay after each successful request, useful for small self-hosted Trilium instances.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Scan only; do not call Trilium.")
    parser.add_argument(
        "--rebuild-state",
        action="store_true",
        help="Scan Trilium tree and rebuild local noteId mapping from sync metadata boxes.",
    )
    parser.add_argument(
        "--prune-orphans",
        action="store_true",
        help="Delete Trilium notes whose source paths no longer exist locally, and remove them from state.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return sync(args)
    except ConfigError as exc:
        print(f"Config error: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:
        print(f"Sync failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
