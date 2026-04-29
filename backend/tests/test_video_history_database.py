import sys
import tempfile
import unittest
from pathlib import Path


BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

import database  # noqa: E402


class VideoHistoryDatabaseTest(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp_dir.cleanup)
        self.original_db_path = database.DB_PATH
        database.DB_PATH = str(Path(self.tmp_dir.name) / "test.db")
        database.init_db()
        self.user_a = database.create_user("a@example.com", "hash")
        self.user_b = database.create_user("b@example.com", "hash")

    def tearDown(self):
        database.DB_PATH = self.original_db_path

    def test_upsert_inserts_then_updates_same_video_for_same_user(self):
        payload = {
            "id": "yt-123",
            "title": "First title",
            "thumbnail": "https://img.example/1.jpg",
            "duration": 120,
            "duration_string": "2:00",
            "uploader": "Uploader A",
            "platform": "youtube",
        }

        database.upsert_video_history(self.user_a["id"], "https://youtu.be/abc", payload)
        database.upsert_video_history(
            self.user_a["id"],
            "https://youtu.be/abc?t=2",
            {**payload, "title": "Updated title"},
        )

        items, total = database.get_user_video_history(self.user_a["id"], offset=0, limit=20)
        self.assertEqual(total, 1)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["title"], "Updated title")
        self.assertEqual(items[0]["source_url"], "https://youtu.be/abc?t=2")

    def test_history_queries_are_user_scoped_and_paginated(self):
        for idx in range(3):
            database.upsert_video_history(
                self.user_a["id"],
                f"https://example.com/a-{idx}",
                {
                    "id": f"a-{idx}",
                    "title": f"Video A {idx}",
                    "thumbnail": "",
                    "duration": idx,
                    "duration_string": "0:00",
                    "uploader": "Uploader A",
                    "platform": "youtube",
                },
            )

        database.upsert_video_history(
            self.user_b["id"],
            "https://example.com/b-0",
            {
                "id": "b-0",
                "title": "Video B 0",
                "thumbnail": "",
                "duration": 1,
                "duration_string": "0:01",
                "uploader": "Uploader B",
                "platform": "bilibili",
            },
        )

        database.upsert_video_history(
            self.user_a["id"],
            "https://example.com/a-0?latest=1",
            {
                "id": "a-0",
                "title": "Video A 0 Latest",
                "thumbnail": "",
                "duration": 10,
                "duration_string": "0:10",
                "uploader": "Uploader A",
                "platform": "youtube",
            },
        )

        first_page, total = database.get_user_video_history(self.user_a["id"], offset=0, limit=2)
        second_page, second_total = database.get_user_video_history(self.user_a["id"], offset=2, limit=2)

        self.assertEqual(total, 3)
        self.assertEqual(second_total, 3)
        self.assertEqual(len(first_page), 2)
        self.assertEqual(len(second_page), 1)
        self.assertEqual(first_page[0]["video_id"], "a-0")
        self.assertEqual(first_page[0]["title"], "Video A 0 Latest")
        self.assertTrue(all(item["title"].startswith("Video A") for item in first_page + second_page))
        self.assertEqual({item["video_id"] for item in first_page + second_page}, {"a-0", "a-1", "a-2"})
