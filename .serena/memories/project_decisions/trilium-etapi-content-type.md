# Trilium ETAPI Content-Type for Updating Content

- 2026-07-11: A real sync failed on `PUT /etapi/notes/vKlInUyGxL8C/content` with HTTP 500: `Cannot set null content to noteId 'vKlInUyGxL8C'`.
- The noteId mapped to directory path `0-Projects`. Trilium reported it as a normal `text` note with `mime=text/html` and existing content length 199. Local `folder_html("0-Projects", "0-Projects")` also produced a non-empty 199-character HTML string.
- Root cause: the script sent raw HTML with `Content-Type: text/html; charset=utf-8`; TriliumNext ETAPI's `PUT /etapi/notes/:noteId/content` handler calls `note.setContent(req.body)`, and in this deployment that content type was not parsed into `req.body`, so the server saw `null`.
- Fix: `TriliumClient.update_note_content()` now sends the raw HTML string as `Content-Type: text/plain; charset=utf-8`, which the ETAPI body parser can pass through as a string while keeping the note MIME as `text/html`.
- Regression test: `TriliumClientTests.test_update_note_content_sends_plain_text_body_for_trilium_parser` locks this behavior.
- Verification after fix: `./.venv/bin/python -m unittest discover -s tests -p 'test_*.py'` passed 13 tests; `./sync --dry-run` succeeded and reported 123 pending updates after the interrupted real sync.