import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from capslane import CapslaneClient


class FakeResponse:
    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return None

    def read(self):
        return json.dumps({"content": [], "lang": "en", "requestId": "req_test"}).encode()


class CapslaneClientTest(unittest.TestCase):
    @patch("capslane.client.urlopen", return_value=FakeResponse())
    def test_api_key_stays_in_header(self, mocked_urlopen):
        client = CapslaneClient("vxl_test_secret")
        result = client.transcript("dQw4w9WgXcQ", mode="native")
        request = mocked_urlopen.call_args.args[0]
        self.assertEqual(result["requestId"], "req_test")
        self.assertNotIn("vxl_test_secret", request.full_url)
        self.assertEqual(request.headers["X-api-key"], "vxl_test_secret")


if __name__ == "__main__":
    unittest.main()

