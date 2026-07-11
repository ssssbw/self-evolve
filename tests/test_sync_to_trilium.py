from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "sync_to_trilium.py"
SPEC = importlib.util.spec_from_file_location("sync_to_trilium", MODULE_PATH)
sync_to_trilium = importlib.util.module_from_spec(SPEC)
assert SPEC is not None and SPEC.loader is not None
SPEC.loader.exec_module(sync_to_trilium)


class SyncEventLoggerTests(unittest.TestCase):
    def test_record_appends_json_line_with_run_context(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            log_path = Path(temp_dir) / "sync.jsonl"
            logger = sync_to_trilium.SyncEventLogger(
                log_path=log_path,
                run_id="run-001",
                started_at="2026-07-11T10:00:00+08:00",
            )

            logger.record(
                "create",
                kind="file",
                path="README.md",
                title="README",
                note_id="note-123",
                hash_before=None,
                hash_after="abc123",
            )

            [event] = log_path.read_text(encoding="utf-8").splitlines()
            payload = json.loads(event)

            self.assertEqual(payload["runId"], "run-001")
            self.assertEqual(payload["startedAt"], "2026-07-11T10:00:00+08:00")
            self.assertEqual(payload["event"], "create")
            self.assertEqual(payload["kind"], "file")
            self.assertEqual(payload["path"], "README.md")
            self.assertEqual(payload["title"], "README")
            self.assertEqual(payload["noteId"], "note-123")
            self.assertIsNone(payload["hashBefore"])
            self.assertEqual(payload["hashAfter"], "abc123")
            self.assertIn("timestamp", payload)

    def test_parser_accepts_log_dir(self) -> None:
        parser = sync_to_trilium.build_parser()

        args = parser.parse_args(["--log-dir", ".custom-sync-logs"])

        self.assertEqual(args.log_dir, ".custom-sync-logs")

    def test_parser_accepts_prune_orphans(self) -> None:
        parser = sync_to_trilium.build_parser()

        args = parser.parse_args(["--prune-orphans"])

        self.assertTrue(args.prune_orphans)


class DotenvTests(unittest.TestCase):
    def test_load_dotenv_sets_missing_values_without_overriding_existing_environment(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            env_path = Path(temp_dir) / ".env"
            env_path.write_text(
                "\n".join(
                    [
                        "# Trilium sync config",
                        "TRILIUM_HOST=https://example.test",
                        "TRILIUM_ROOT_NOTE_ID='root-note'",
                        "TRILIUM_TOKEN=\"secret token\"",
                        "TRILIUM_SYNC_TIMEOUT=30",
                        "IGNORED_LINE_WITHOUT_EQUALS",
                    ]
                ),
                encoding="utf-8",
            )
            original = {key: os.environ.get(key) for key in ["TRILIUM_HOST", "TRILIUM_ROOT_NOTE_ID", "TRILIUM_TOKEN", "TRILIUM_SYNC_TIMEOUT"]}
            os.environ["TRILIUM_HOST"] = "https://already-set.test"
            for key in ["TRILIUM_ROOT_NOTE_ID", "TRILIUM_TOKEN", "TRILIUM_SYNC_TIMEOUT"]:
                os.environ.pop(key, None)
            try:
                loaded = sync_to_trilium.load_dotenv(env_path)

                self.assertEqual(os.environ["TRILIUM_HOST"], "https://already-set.test")
                self.assertEqual(os.environ["TRILIUM_ROOT_NOTE_ID"], "root-note")
                self.assertEqual(os.environ["TRILIUM_TOKEN"], "secret token")
                self.assertEqual(os.environ["TRILIUM_SYNC_TIMEOUT"], "30")
                self.assertEqual(
                    loaded,
                    {
                        "TRILIUM_ROOT_NOTE_ID": "root-note",
                        "TRILIUM_TOKEN": "secret token",
                        "TRILIUM_SYNC_TIMEOUT": "30",
                    },
                )
            finally:
                for key, value in original.items():
                    if value is None:
                        os.environ.pop(key, None)
                    else:
                        os.environ[key] = value

    def test_env_int_uses_environment_value_before_default(self) -> None:
        original = os.environ.get("TRILIUM_SYNC_RETRIES")
        os.environ["TRILIUM_SYNC_RETRIES"] = "5"
        try:
            self.assertEqual(sync_to_trilium.env_int("TRILIUM_SYNC_RETRIES", 3), 5)
        finally:
            if original is None:
                os.environ.pop("TRILIUM_SYNC_RETRIES", None)
            else:
                os.environ["TRILIUM_SYNC_RETRIES"] = original


class TriliumClientTests(unittest.TestCase):
    def test_update_note_content_sends_plain_text_body_for_trilium_parser(self) -> None:
        client = sync_to_trilium.TriliumClient("https://trilium.example.test", "token")
        captured: dict[str, object] = {}

        def fake_request(method: str, path: str, **kwargs: object) -> None:
            captured["method"] = method
            captured["path"] = path
            captured.update(kwargs)

        client._request = fake_request

        client.update_note_content("note-123", "<p>content</p>")

        self.assertEqual(captured["method"], "PUT")
        self.assertEqual(captured["path"], "/etapi/notes/note-123/content")
        self.assertEqual(captured["raw_body"], "<p>content</p>")
        self.assertEqual(captured["content_type"], "text/plain; charset=utf-8")


class OrphanPruneTests(unittest.TestCase):
    def test_find_orphaned_paths_returns_state_items_missing_from_sources(self) -> None:
        items = {
            "README.md": {"kind": "file"},
            "2-Resources": {"kind": "dir"},
            "2-Resources/deleted.md": {"kind": "file"},
        }

        orphaned = sync_to_trilium.find_orphaned_paths(items, {"README.md", "2-Resources"})

        self.assertEqual(orphaned, ["2-Resources/deleted.md"])

    def test_prune_orphans_deletes_remote_notes_and_removes_state_entries(self) -> None:
        class FakeClient:
            def __init__(self) -> None:
                self.deleted: list[str] = []

            def delete_note(self, note_id: str) -> None:
                self.deleted.append(note_id)

        with tempfile.TemporaryDirectory() as temp_dir:
            state_path = Path(temp_dir) / "state.json"
            log_path = Path(temp_dir) / "sync.jsonl"
            state = {
                "rootNoteId": "root",
                "items": {
                    "README.md": {"kind": "file", "noteId": "keep-note", "title": "README"},
                    "old.md": {"kind": "file", "noteId": "old-note", "title": "old"},
                },
            }
            sync_to_trilium.save_state(state_path, state)
            logger = sync_to_trilium.SyncEventLogger(
                log_path=log_path,
                run_id="run-001",
                started_at="2026-07-11T10:00:00+08:00",
            )
            client = FakeClient()
            original_log = sync_to_trilium.log
            sync_to_trilium.log = lambda message: None

            try:
                pruned = sync_to_trilium.prune_orphans(
                    client,
                    state,
                    ["old.md"],
                    state_path,
                    logger,
                )
            finally:
                sync_to_trilium.log = original_log

            saved = sync_to_trilium.load_state(state_path, "root")
            [event] = log_path.read_text(encoding="utf-8").splitlines()
            payload = json.loads(event)

            self.assertEqual(pruned, 1)
            self.assertEqual(client.deleted, ["old-note"])
            self.assertIn("README.md", state["items"])
            self.assertNotIn("old.md", state["items"])
            self.assertNotIn("old.md", saved["items"])
            self.assertEqual(payload["event"], "prune")
            self.assertEqual(payload["path"], "old.md")
            self.assertEqual(payload["noteId"], "old-note")


class SyncHtmlTests(unittest.TestCase):
    def test_sync_info_html_uses_trilium_note_admonition(self) -> None:
        rendered = sync_to_trilium.sync_info_html(
            "guideline/一五计划/第一个五年计划.md",
            "2026-07-11 10:00:00",
        )

        self.assertEqual(
            rendered,
            "<aside class=\"admonition note\">"
            "<p><strong>同步信息</strong></p>"
            "<p><strong>来源路径：</strong><code>guideline/一五计划/第一个五年计划.md</code></p>"
            "<p><strong>同步时间：</strong><code>2026-07-11 10:00:00</code></p>"
            "</aside>",
        )

    def test_folder_and_note_html_use_same_sync_info_box(self) -> None:
        original_now_display = sync_to_trilium.now_display
        sync_to_trilium.now_display = lambda: "2026-07-11 10:00:00"
        try:
            folder = sync_to_trilium.folder_html("guideline/一五计划", "一五计划")
            note = sync_to_trilium.note_html("# 标题", "guideline/一五计划/第一个五年计划.md")
        finally:
            sync_to_trilium.now_display = original_now_display

        self.assertIn("<aside class=\"admonition note\">", folder)
        self.assertIn("<aside class=\"admonition note\">", note)
        self.assertIn("<p><strong>来源路径：</strong><code>guideline/一五计划</code></p>", folder)
        self.assertIn(
            "<p><strong>来源路径：</strong><code>guideline/一五计划/第一个五年计划.md</code></p>",
            note,
        )
        self.assertIn("<p><strong>同步时间：</strong><code>2026-07-11 10:00:00</code></p>", folder)
        self.assertIn("<p><strong>同步时间：</strong><code>2026-07-11 10:00:00</code></p>", note)
        self.assertNotIn("Source path", note)
        self.assertNotIn("Synced at", note)

    def test_markdown_to_html_keeps_nested_unordered_items_inside_ordered_list(self) -> None:
        rendered = sync_to_trilium.markdown_to_html(
            "\n".join(
                [
                    "1. 《金钱心理学》",
                    "   - 重点：财富行为、风险感知、长期主义。",
                    "   - 产出：写下自己的消费、储蓄和投资误区。",
                    "2. 《漫步华尔街》",
                    "   - 重点：市场有效性、随机漫步、指数化投资、资产配置。",
                    "   - 产出：说明为什么不频繁择时。",
                ]
            )
        )

        self.assertEqual(rendered.count("<ol"), 1)
        self.assertEqual(rendered.count("</ol>"), 1)
        self.assertIn("<ul>", rendered)
        self.assertLess(rendered.index("<li>《金钱心理学》"), rendered.index("<ul>"))
        self.assertLess(rendered.index("</ul>"), rendered.index("<li>《漫步华尔街》"))

    def test_markdown_to_html_keeps_common_markdown_features(self) -> None:
        rendered = sync_to_trilium.markdown_to_html(
            "\n".join(
                [
                    "# 标题",
                    "",
                    "这是 **重点** 和 [链接](https://example.test)。",
                    "",
                    "| 维度 | 状态 |",
                    "| --- | --- |",
                    "| 技术 | 进行中 |",
                    "",
                    "```python",
                    "print('ok')",
                    "```",
                ]
            )
        )

        self.assertIn("<h1>标题</h1>", rendered)
        self.assertIn("<strong>重点</strong>", rendered)
        self.assertIn('<a href="https://example.test">链接</a>', rendered)
        self.assertIn("<table>", rendered)
        self.assertIn("<th>维度</th>", rendered)
        self.assertIn("<td>技术</td>", rendered)
        self.assertIn('<code class="language-python">', rendered)
        self.assertIn("print('ok')", rendered)

    def test_extract_source_path_supports_new_and_legacy_metadata(self) -> None:
        new_content = (
            "<aside class=\"admonition note\">"
            "<p><strong>同步信息</strong></p>"
            "<p><strong>来源路径：</strong><code>guideline/一五计划/第一个五年计划.md</code></p>"
            "<p><strong>同步时间：</strong><code>2026-07-11 10:00:00</code></p>"
            "</aside>"
        )
        legacy_content = (
            "<p><strong>Source path:</strong> "
            "<code>guideline/一五计划/第一个五年计划.md</code><br>"
            "<strong>Synced at:</strong> <code>2026-07-10T17:44:27+08:00</code></p>"
        )

        self.assertEqual(
            sync_to_trilium.extract_source_path(new_content),
            "guideline/一五计划/第一个五年计划.md",
        )
        self.assertEqual(
            sync_to_trilium.extract_source_path(legacy_content),
            "guideline/一五计划/第一个五年计划.md",
        )


class SyncTemplateVersionTests(unittest.TestCase):
    def test_missing_or_old_template_version_requires_update(self) -> None:
        current_hash = "abc123"

        self.assertTrue(sync_to_trilium.needs_content_update({"hash": current_hash}, current_hash))
        self.assertTrue(
            sync_to_trilium.needs_content_update(
                {"hash": current_hash, "templateVersion": sync_to_trilium.CONTENT_TEMPLATE_VERSION - 1},
                current_hash,
            )
        )

    def test_current_template_version_and_same_hash_can_skip(self) -> None:
        current_hash = "abc123"

        self.assertFalse(
            sync_to_trilium.needs_content_update(
                {"hash": current_hash, "templateVersion": sync_to_trilium.CONTENT_TEMPLATE_VERSION},
                current_hash,
            )
        )

    def test_directory_without_current_template_version_requires_update(self) -> None:
        self.assertTrue(sync_to_trilium.needs_content_update({"kind": "dir"}))
        self.assertFalse(
            sync_to_trilium.needs_content_update(
                {"kind": "dir", "templateVersion": sync_to_trilium.CONTENT_TEMPLATE_VERSION}
            )
        )


if __name__ == "__main__":
    unittest.main()
