"""실제 HTTP 서버에 요청해 화면과 입력 처리를 검증한다."""

import re
import socket
import threading
import time
import unittest
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import urlopen

import uvicorn
from main import app


class CalculatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sock = socket.socket()
        cls.sock.bind(("127.0.0.1", 0))
        cls.base_url = f"http://127.0.0.1:{cls.sock.getsockname()[1]}"
        cls.server = uvicorn.Server(uvicorn.Config(app, log_level="error"))
        cls.thread = threading.Thread(
            target=cls.server.run, kwargs={"sockets": [cls.sock]}, daemon=True
        )
        cls.thread.start()
        for _ in range(100):
            if cls.server.started:
                return
            time.sleep(0.05)
        cls.server.should_exit = True
        cls.thread.join(timeout=5)
        cls.sock.close()
        raise RuntimeError("검증용 서버를 시작하지 못했습니다.")

    @classmethod
    def tearDownClass(cls):
        cls.server.should_exit = True
        cls.thread.join(timeout=5)
        cls.sock.close()

    def get(self, path):
        try:
            response = urlopen(self.base_url + path, timeout=5)
        except HTTPError as error:
            response = error
        with response:
            return response.status, response.read().decode("utf-8")

    def test_home_and_css(self):
        status, html = self.get("/")
        self.assertEqual(status, 200)
        self.assertIn('action="/calculate"', html)
        self.assertNotIn("$first", html)
        status, css = self.get("/static/style.css")
        self.assertEqual(status, 200)
        self.assertIn("@media", css)

    def test_calculations(self):
        cases = [
            ("12", "3", ["15", "9", "36", "4"]),
            ("-5", "2", ["-3", "-7", "-10", "-2.5"]),
            ("0.1", "0.2", ["0.3", "-0.1", "0.02", "0.5"]),
            ("0", "2", ["2", "-2", "0", "0"]),
            (" 12 ", "+3", ["15", "9", "36", "4"]),
            ("0.0000000001", "0.0000000001",
             ["0.0000000002", "0", "0.00000000000000000001", "1"]),
        ]
        for first, second, expected in cases:
            with self.subTest(first=first, second=second):
                status, html = self.get("/calculate?" + urlencode({"first": first, "second": second}))
                self.assertEqual(status, 200)
                self.assertEqual(re.findall(r'<p class="value">(.*?)</p>', html), expected)

    def test_zero_division(self):
        for zero in ("0", "-0", "0.0"):
            with self.subTest(zero=zero):
                status, html = self.get("/calculate?" + urlencode({"first": "8", "second": zero}))
                self.assertEqual(status, 200)
                self.assertEqual(re.findall(r'<p class="value">(.*?)</p>', html),
                                 ["8", "8", "0", "0으로 나눌 수 없습니다"])

    def test_invalid_inputs(self):
        for invalid in ("", " ", "abc", "NaN", "Infinity", "1e100", "1,000",
                        "1234567890123", "0.12345678901", "9" * 1000):
            for field in ("first", "second"):
                with self.subTest(invalid=invalid[:30], field=field):
                    params = {"first": "2", "second": "3", field: invalid}
                    status, html = self.get("/calculate?" + urlencode(params))
                    self.assertEqual(status, 400)
                    self.assertIn('role="alert"', html)
                    self.assertNotIn('class="result"', html)

    def test_missing_and_html_input(self):
        self.assertEqual(self.get("/calculate")[0], 400)
        payload = '"><script>alert(1)</script>'
        status, html = self.get("/calculate?" + urlencode({"first": payload, "second": "2"}))
        self.assertEqual(status, 400)
        self.assertNotIn("<script>", html)
        self.assertIn("&lt;script&gt;", html)

    def test_large_and_repeating_results(self):
        status, html = self.get("/calculate?first=999999999999&second=999999999999")
        self.assertEqual(status, 200)
        self.assertIn("999999999998000000000001", html)
        cases = [
            ("1", "3", "0.33333"),
            ("2", "3", "0.66667"),
            ("-2", "3", "-0.66667"),
            ("123456", "1", "123460"),
            ("0.00123456", "1", "0.0012346"),
            ("123445", "10", "12344"),  # 정확히 중간이면 짝수로 반올림
            ("999999", "10", "100000"),
        ]
        for first, second, expected in cases:
            with self.subTest(first=first, second=second):
                status, html = self.get("/calculate?" + urlencode({"first": first, "second": second}))
                self.assertEqual(status, 200)
                self.assertEqual(re.findall(r'<p class="value">(.*?)</p>', html)[3], expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
