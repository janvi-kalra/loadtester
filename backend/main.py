from typing import Union, List
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import concurrent.futures
import time
import statistics
from fastapi.middleware.cors import CORSMiddleware
import requests
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import asyncio

app = FastAPI()

class LoadTestParams(BaseModel):
    url: str
    qps: int
    duration: int

class TestResult(BaseModel):
    url: str
    qps: int
    duration: Union[int, None]
    total_requests: int
    successful_requests: int
    failed_requests: int
    error_rate: float
    median_latency: float
    p90_latency: float
    p99_latency: float
    avg_latency: float
    min_latency: float
    max_latency: float
    avg_size: float
    current_rps: float
    current_failures_per_sec: float
    timestamp: float

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

past_tests: List[TestResult] = []
stop_event = asyncio.Event()

class HTTPLoadTester:
    def __init__(self, url, num_requests, num_concurrent, qps, duration=1):
        self.url = url
        self.num_requests = num_requests
        self.num_concurrent = num_concurrent
        self.qps = qps
        self.duration = duration
        self.session = self.create_session()  # Use a session object with retry strategy
        self.results = []
        self.errors = []
        self.start_time = None

    def create_session(self):
        session = requests.Session()
        retries = Retry(total=5, backoff_factor=0.5, status_forcelist=[429, 500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retries)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session

    def make_request(self):
        latencies = []
        sizes = []
        successful_requests = 0
        failed_requests = 0

        try:
            request_start_time = time.time()
            response = self.session.get(self.url)
            response.raise_for_status()
            latency = time.time() - request_start_time
            latencies.append(latency)
            sizes.append(len(response.content))
            successful_requests += 1
        except Exception as e:
            print(f"Unexpected error for URL {self.url}: {str(e)}")
            failed_requests += 1
        
        return latencies, sizes, successful_requests, failed_requests

    def run(self):
        latencies = []
        sizes = []
        successful_requests = 0
        failed_requests = 0

        self.start_time = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.num_concurrent) as executor:
            future_to_request = {executor.submit(self.make_request): i for i in range(self.num_requests)}
            for future in concurrent.futures.as_completed(future_to_request):
                if stop_event.is_set():
                    break
                try:
                    res_latencies, res_sizes, res_successful, res_failed = future.result()
                    latencies.extend(res_latencies)
                    sizes.extend(res_sizes)
                    successful_requests += res_successful
                    failed_requests += res_failed
                except Exception as exc:
                    print(f"Error processing request: {str(exc)}")
                    failed_requests += 1

        elapsed_time = time.time() - self.start_time
        total_requests = successful_requests + failed_requests
        error_rate = (failed_requests / total_requests) * 100 if total_requests > 0 else 0

        if latencies:
            latencies.sort()
            avg_latency = statistics.mean(latencies)
            min_latency = latencies[0]
            max_latency = latencies[-1]
            median_latency = statistics.median(latencies)
            p90_latency = latencies[int(0.90 * len(latencies))]
            p99_latency = latencies[int(0.99 * len(latencies))]
        else:
            avg_latency = min_latency = max_latency = median_latency = p90_latency = p99_latency = 0

        avg_size = statistics.mean(sizes) if sizes else 0
        current_rps = total_requests / elapsed_time if elapsed_time > 0 else 0
        current_failures_per_sec = failed_requests / elapsed_time if elapsed_time > 0 else 0

        result = TestResult(
            url=self.url,
            qps=self.qps,
            duration=self.duration,
            total_requests=total_requests,
            successful_requests=successful_requests,
            failed_requests=failed_requests,
            error_rate=error_rate,
            median_latency=median_latency,
            p90_latency=p90_latency,
            p99_latency=p99_latency,
            avg_latency=avg_latency,
            min_latency=min_latency,
            max_latency=max_latency,
            avg_size=avg_size,
            current_rps=current_rps,
            current_failures_per_sec=current_failures_per_sec,
            timestamp=time.time()
        )

        return result

async def start_load_test(params: LoadTestParams):
    tester = HTTPLoadTester(url=params.url, num_requests=params.qps * params.duration, num_concurrent=params.qps, qps=params.qps, duration=params.duration)
    result = tester.run()
    past_tests.append(result)
    stop_event.clear()
    return result

@app.post("/loadtest", response_model=TestResult)
async def run_load_test(params: LoadTestParams, background_tasks: BackgroundTasks):
    if stop_event.is_set():
        raise HTTPException(status_code=400, detail="Another test is currently running.")
    stop_event.clear()
    current_test = TestResult(
        url=params.url,
        qps=params.qps,
        duration=params.duration,
        total_requests=0,
        successful_requests=0,
        failed_requests=0,
        error_rate=0,
        median_latency=0,
        p90_latency=0,
        p99_latency=0,
        avg_latency=0,
        min_latency=0,
        max_latency=0,
        avg_size=0,
        current_rps=0,
        current_failures_per_sec=0,
        timestamp=time.time()
    )
    background_tasks.add_task(start_load_test, params)
    return current_test

@app.post("/stop")
async def stop_load_test():
    if not stop_event.is_set():
        stop_event.set()
        return {"message": "Test stopped"}
    else:
        raise HTTPException(status_code=400, detail="No test is currently running.")

@app.get("/results", response_model=List[TestResult])
async def get_results():
    return past_tests
