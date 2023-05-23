import json
import os

from testcontainers.redis import RedisContainer


def test_api(client):
    redis_container = setup_redis()

    # test GET /version endpoint
    res = client.get("/version")
    expected = {"version": "1.0"}
    assert res.status_code == 200
    assert expected == json.loads(res.get_data(as_text=True))

    # test GET /readyz endpoint
    res = client.get("/readyz")
    expected = {"ready": True}
    assert res.status_code == 200
    assert expected == json.loads(res.get_data(as_text=True))

    # test GET /livez endpoint
    res = client.get("/livez")
    expected = {"alive": True}
    assert res.status_code == 200
    assert expected == json.loads(res.get_data(as_text=True))

    # test POST /hits endpoint
    res = client.post("/")
    expected = {"hits": 1}
    assert res.status_code == 201
    assert expected == json.loads(res.get_data(as_text=True))

    # test GET /hits endpoint
    res = client.get("/")
    expected = {"hits": 1}
    assert res.status_code == 200
    assert expected == json.loads(res.get_data(as_text=True))

    # test /trigger_error endpoint
    res = client.post("/trigger_error")
    expected = {
        "error": "500 Internal Server Error: The server encountered an internal error and was unable to complete your request."
    }
    assert res.status_code == 500
    assert expected["error"] in json.loads(res.get_data(as_text=True))["error"]

    # test /metrics endpoint
    res = client.get("/metrics")
    assert res.status_code == 200
    metrics = res.get_data().decode("utf-8").split("\n")
    expected_metrics = [
        'request_total{app="phippy_api",endpoint="version",status="200",verb="GET"} 1.0',
        'request_total{app="phippy_api",endpoint="hits",status="201",verb="POST"} 1.0',
        'request_total{app="phippy_api",endpoint="trigger_error",status="500",verb="POST"} 1.0'
        'errors_total{app="phippy_api",endpoint="trigger_error",status="500",verb="POST"} 1.0',
    ]

    for metric in expected_metrics:
        metric in metrics

    teardown_redis(redis_container)


def setup_redis():
    redis_container = RedisContainer(image="ghcr.io/hlesey/redis:4").with_bind_ports(6379, 6379)
    redis_container.start()
    return redis_container


def teardown_redis(redis_container):
    redis_container.stop()
