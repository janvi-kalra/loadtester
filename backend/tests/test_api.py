import pytest
import time
import requests
from fastapi.testclient import TestClient
from httpx import AsyncClient
from unittest.mock import patch, MagicMock
from backend.main import app, past_tests, stop_event, HTTPLoadTester, TestResult

client = TestClient(app)

# Mocked responses
def mock_successful_request(*args, **kwargs):
    return 0.1, 1256, True  # latency, size, success

def mock_failed_request(*args, **kwargs):
    return 0, 0, False  # latency, size, success

def response_generator():
    yield mock_successful_request()
    yield mock_failed_request()

@pytest.fixture(autouse=True)
def clear_past_tests_and_stop_event():
    past_tests.clear()
    stop_event.clear()

@pytest.mark.asyncio
async def test_start_load_test():
    response = await AsyncClient(app=app, base_url="http://test").post(
        "/loadtest",
        json={"url": "http://example.com", "qps": 1, "duration": 1}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["url"] == "http://example.com"
    assert data["qps"] == 1
    assert data["duration"] == 1

@pytest.mark.asyncio
async def test_stop_load_test():
    response = await AsyncClient(app=app, base_url="http://test").post(
        "/loadtest",
        json={"url": "http://example.com", "qps": 1, "duration": 1}
    )
    assert response.status_code == 200
    # Stop the test
    response = await AsyncClient(app=app, base_url="http://test").post("/stop")
    assert response.status_code == 200
    assert response.json() == {"message": "Test stopped"}

@pytest.mark.asyncio
async def test_stop_load_test_when_not_running():
    stop_event.set()  # Ensure the stop event is set
    response = await AsyncClient(app=app, base_url="http://test").post("/stop")
    assert response.status_code == 400
    assert response.json() == {"detail": "No test is currently running."}

def test_get_results():
    # Clear past_tests before adding a new dummy test result
    past_tests.clear()
    # Add a dummy test result
    past_tests.append(TestResult(
        url="http://example.com",
        qps=1,
        duration=1,
        total_requests=1,
        successful_requests=1,
        failed_requests=0,
        error_rate=0.0,
        median_latency=0.1,
        p90_latency=0.1,
        p99_latency=0.1,
        avg_latency=0.1,
        min_latency=0.1,
        max_latency=0.1,
        avg_size=100.0,
        current_rps=1.0,
        current_failures_per_sec=0.0,
        timestamp=1625077800.0
    ))

    response = client.get("/results")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["url"] == "http://example.com"

# Mocking requests in HTTPLoadTester
@pytest.mark.asyncio
@patch.object(HTTPLoadTester, 'make_request', side_effect=mock_successful_request)
async def test_load_test_statistics_success(mock_make_request):
    tester = HTTPLoadTester(url="http://example.com", qps=2, duration=1)
    result = await tester.run()
    assert result.successful_requests == 2
    assert result.failed_requests == 0
    assert result.error_rate == 0
    assert result.avg_latency > 0
    assert result.min_latency > 0
    assert result.max_latency > 0

@pytest.mark.asyncio
@patch.object(HTTPLoadTester, 'make_request', side_effect=mock_failed_request)
async def test_load_test_statistics_failure(mock_make_request):
    tester = HTTPLoadTester(url="http://example.com", qps=2, duration=1)
    result = await tester.run()
    assert result.successful_requests == 0
    assert result.failed_requests == 2
    assert result.error_rate == 100
    assert result.avg_latency == 0
    assert result.min_latency == 0
    assert result.max_latency == 0

@pytest.mark.asyncio
@patch.object(HTTPLoadTester, 'make_request', side_effect=response_generator())
async def test_load_test_statistics_mixed(mock_make_request):
    tester = HTTPLoadTester(url="http://example.com", qps=2, duration=1)
    result = await tester.run()
    assert result.successful_requests == 1
    assert result.failed_requests == 1
    assert result.error_rate == 50
    assert result.avg_latency > 0
    assert result.min_latency > 0
    assert result.max_latency > 0
