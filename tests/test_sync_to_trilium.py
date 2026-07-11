from __future__ import annotations

import importlib.util
import json
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
