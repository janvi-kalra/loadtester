import pytest
from fastapi.testclient import TestClient
from httpx import HTTPStatusError, AsyncClient
from unittest.mock import AsyncMock, patch
from backend.main import app 

client = TestClient(app)

@pytest.mark.asyncio
async def test_load_test_failure():
    # Mock URL that will fail
    test_url = "http://example.com/fail"
    qps = 10
    duration = 2

    async def mock_get(*args, **kwargs):
        raise HTTPStatusError("Request failed", request=None, response=None)

    with patch("httpx.AsyncClient.get", new=mock_get):
        response = client.post("/loadtest", json={"url": test_url, "qps": qps, "duration": duration})
        assert response.status_code == 200
        result = response.json()

        assert result["url"] == test_url
        assert result["qps"] == qps
        assert result["duration"] == duration
        assert result["total_requests"] == qps * duration
        assert result["failed_requests"] == qps * duration
        assert result["successful_requests"] == 0
        assert result["error_rate"] == 100.0

@pytest.mark.asyncio
async def test_load_test_partial_failure():
    test_url = "http://example.com/partial_fail"
    qps = 10
    duration = 2
    total_requests = qps * duration
    fail_requests = total_requests // 2  # Fail exactly 50% of the requests
    request_count = -1

    async def mock_get(*args, **kwargs):
        nonlocal request_count
        request_count += 1

        if request_count < fail_requests:
            raise httpx.HTTPStatusError("Request failed", request=None, response=None)
        return AsyncMock(status_code=200)()

    with patch("httpx.AsyncClient.get", new=mock_get):
        response = client.post("/loadtest", json={"url": test_url, "qps": qps, "duration": duration})
        assert response.status_code == 200
        result = response.json()

        assert result["url"] == test_url
        assert result["qps"] == qps
        assert result["duration"] == duration
        assert result["total_requests"] == total_requests
        assert result["failed_requests"] == fail_requests
        assert result["successful_requests"] == total_requests - fail_requests
        assert result["error_rate"] == pytest.approx(50.0, rel=0.01)
