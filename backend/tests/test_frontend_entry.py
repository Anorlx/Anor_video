import sys
import unittest
from pathlib import Path

from fastapi.testclient import TestClient


BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from main import app  # noqa: E402


class FrontendEntryTest(unittest.TestCase):
    def test_root_serves_built_frontend(self):
        client = TestClient(app)

        response = client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("Agent_video", response.text)


if __name__ == "__main__":
    unittest.main()
