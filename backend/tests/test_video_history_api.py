import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient


BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

import auth  # noqa: E402
import database  # noqa: E402
import main  # noqa: E402


class VideoHistoryApiTest(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp_dir.cleanup)
        self.original_db_path = database.DB_PATH
        database.DB_PATH = str(Path(self.tmp_dir.name) / "test.db")
        database.init_db()
        self.client = TestClient(main.app)
        self.user = database.create_user("history@example.com", "hash")
        self.other_user = database.create_user("other@example.com", "hash")
        self.token = auth.create_token(self.user["id"], "history@example.com")

    def tearDown(self):
        database.DB_PATH = self.original_db_path

    def test_parse_saves_history_for_logged_in_user_only(self):
        fake_result = {
            "id": "yt-001",
            "title": "Video One",
            "thumbnail": "https://img.example/1.jpg",
            "duration": 90,
            "duration_string": "1:30",
            "uploader": "Uploader One",
            "platform": "youtube",
            "formats": [],
        }

        with patch.object(main.downloader, "parse_video", return_value=fake_result):
            response = self.client.post(
                "/api/parse",
                json={"url": "https://youtu.be/one"},
                headers={"Authorization": f"Bearer {self.token}"},
            )

        self.assertEqual(response.status_code, 200)
        items, total = database.get_user_video_history(self.user["id"], 0, 20)
        self.assertEqual(total, 1)
        self.assertEqual(items[0]["title"], "Video One")

    def test_guest_parse_does_not_create_history_row(self):
        fake_result = {
            "id": "yt-guest",
            "title": "Guest Video",
            "thumbnail": "",
            "duration": 45,
            "duration_string": "0:45",
            "uploader": "Guest",
            "platform": "youtube",
            "formats": [],
        }

        with patch.object(main.downloader, "parse_video", return_value=fake_result):
            response = self.client.post("/api/parse", json={"url": "https://youtu.be/guest"})

        self.assertEqual(response.status_code, 200)
        items, total = database.get_user_video_history(self.user["id"], 0, 20)
        self.assertEqual(total, 0)
        self.assertEqual(items, [])

    def test_history_endpoint_returns_only_current_user_rows(self):
        database.upsert_video_history(
            self.user["id"],
            "https://youtu.be/self",
            {
                "id": "self-1",
                "title": "Self Video",
                "thumbnail": "",
                "duration": 60,
                "duration_string": "1:00",
                "uploader": "Self",
                "platform": "youtube",
            },
        )
        database.upsert_video_history(
            self.other_user["id"],
            "https://youtu.be/other",
            {
                "id": "other-1",
                "title": "Other Video",
                "thumbnail": "",
                "duration": 30,
                "duration_string": "0:30",
                "uploader": "Other",
                "platform": "youtube",
            },
        )

        response = self.client.get(
            "/api/history?offset=0&limit=20",
            headers={"Authorization": f"Bearer {self.token}"},
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()["data"]
        self.assertEqual(payload["total"], 1)
        self.assertEqual(payload["items"][0]["title"], "Self Video")
        self.assertFalse(payload["has_more"])
