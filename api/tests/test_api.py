import json
import unittest

from src.api import app
from testcontainers.redis import RedisContainer


class TestPhippyAPI(unittest.TestCase):
    redis_container: RedisContainer = {}

    @classmethod
    def setUpClass(cls):
        cls.redis_container = RedisContainer(image="ghcr.io/hlesey/redis:7").with_bind_ports(6379, 6379)
        cls.redis_container.start()
        cls.client = app.test_client()

    @classmethod
    def tearDownClass(cls):
        cls.redis_container.stop()

    def test_version(self):
        # test GET /version endpoint
        res = self.client.get("/version")
        expected = {"version": "1.0"}
        self.assertEqual(res.status_code, 200)
        self.assertEqual(expected, json.loads(res.get_data(as_text=True)))

    def test_readyz(self):
        # test GET /readyz endpoint
        res = self.client.get("/readyz")
        expected = {"ready": True}
        self.assertEqual(res.status_code, 200)
        self.assertEqual(expected, json.loads(res.get_data(as_text=True)))

    def test_livez(self):
        # test GET /livez endpoint
        res = self.client.get("/livez")
        expected = {"alive": True}
        self.assertEqual(res.status_code, 200)
        self.assertEqual(expected, json.loads(res.get_data(as_text=True)))

    def test_hits(self):
        # test POST /hits endpoint
        res = self.client.post("/")
        expected = {"hits": 1}
        self.assertEqual(res.status_code, 201)
        self.assertEqual(expected, json.loads(res.get_data(as_text=True)))

        res = self.client.get("/")
        expected = {"hits": 1}
        self.assertEqual(res.status_code, 200)
        self.assertEqual(expected, json.loads(res.get_data(as_text=True)))

    def test_trigger_error(self):
        # test /trigger_error endpoint
        res = self.client.post("/trigger_error")
        expected = {
            "error": "500 Internal Server Error: The server encountered an internal error and was unable to complete your request."
        }
        self.assertEqual(res.status_code, 500)

        self.assertTrue(expected["error"] in json.loads(res.get_data(as_text=True))["error"])

    def test_metrics(self):
        # trigger few requests
        self.client.get("/version")
        self.client.get("/readyz")
        self.client.get("/livez")
        self.client.post("/trigger_error")
        self.client.post("/")
        self.client.get("/")

        # test /metrics endpoint
        res = self.client.get("/metrics")
        assert res.status_code == 200
        raw_metrics = res.get_data().decode("utf-8").split("\n")
        metrics = [metric.split(" ")[0] for metric in raw_metrics if not metric.startswith("#")]

        expected_metrics = [
            'request_total{app="phippy_api",endpoint="hits",status="201",verb="POST"}',
            'request_total{app="phippy_api",endpoint="hits",status="200",verb="GET"}',
            'request_total{app="phippy_api",endpoint="version",status="200",verb="GET"}',
            'request_total{app="phippy_api",endpoint="readyz",status="200",verb="GET"}',
            'request_total{app="phippy_api",endpoint="livez",status="200",verb="GET"}',
            'request_total{app="phippy_api",endpoint="trigger_error",status="500",verb="POST"}',
            'errors_total{app="phippy_api",endpoint="trigger_error",status="500",verb="POST"}',
        ]
        self.assertTrue(all(metric in metrics for metric in expected_metrics))
        # assert all(metric in expected_metrics for metric in metrics)


if __name__ == "__main__":
    unittest.main()
