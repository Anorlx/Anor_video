import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

import main  # noqa: E402


class ServerPortTest(unittest.TestCase):
    def test_default_server_port_uses_8010(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(main.get_server_port(), 8010)

    def test_server_port_can_be_overridden_with_env(self):
        with patch.dict(os.environ, {"BACKEND_PORT": "8123"}, clear=True):
            self.assertEqual(main.get_server_port(), 8123)


if __name__ == "__main__":
    unittest.main()
