import sys
import tempfile
import unittest
from pathlib import Path


BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

import database  # noqa: E402


class SummaryUnlimitedTest(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp_dir.cleanup)
        self.original_db_path = database.DB_PATH
        database.DB_PATH = str(Path(self.tmp_dir.name) / "test.db")
        database.init_db()

    def tearDown(self):
        database.DB_PATH = self.original_db_path

    def test_regular_users_can_summarize_without_daily_limit(self):
        user = database.create_user("regular@example.com", "hash")

        for _ in range(20):
            allowed, remaining = database.check_and_increment_summary(user["id"])
            self.assertTrue(allowed)
            self.assertEqual(remaining, -1)


if __name__ == "__main__":
    unittest.main()
