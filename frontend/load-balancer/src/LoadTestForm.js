import React, { useState, useEffect, useCallback } from 'react';

function LoadTestForm({ setResults, setIsLoading, isLoading, fetchResults }) {
  const [url, setUrl] = useState('');
  const [qps, setQps] = useState('');
  const [duration, setDuration] = useState(1); // Default to 1 second
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    let interval;
    if (isLoading && duration) {
      interval = setInterval(() => {
        setProgress(prev => {
          if (prev >= duration) {
            clearInterval(interval);
            setIsLoading(false);
            fetchResults();
            return duration;
          }
          return prev + 1;
        });
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [isLoading, duration, setIsLoading, fetchResults]);

  const handleSubmit = useCallback(async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setProgress(0);

    try {
      const response = await fetch('http://127.0.0.1:8000/loadtest', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          url,
          qps: parseInt(qps),
          duration,
        }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      setResults(prevResults => Array.isArray(prevResults) ? [data, ...prevResults] : [data]);
    } catch (error) {
      console.error('Error running load test:', error);
      setIsLoading(false);
    }
  }, [url, qps, duration, setResults, setIsLoading]);

  const handleStop = useCallback(async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/stop', {
        method: 'POST',
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      setIsLoading(false);
      setProgress(0);
    } catch (error) {
      console.error('Error stopping load test:', error);
    }
  }, [setIsLoading]);

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>URL:</label>
        <input type="text" value={url} onChange={(e) => setUrl(e.target.value)} required />
      </div>
      <div>
        <label>QPS:</label>
        <input type="number" value={qps} onChange={(e) => setQps(e.target.value)} required />
      </div>
      <div>
        <label>Duration (s): {duration}</label>
        <input
          type="range"
          min="1"
          max="10"
          value={duration}
          onChange={(e) => setDuration(parseInt(e.target.value))}
          required
        />
      </div>
      <button type="submit" disabled={isLoading}>Run Load Test</button>
      {isLoading && <button type="button" onClick={handleStop}>Stop</button>}
      {isLoading && duration && (
        <div>
          <progress value={progress} max={duration}></progress>
        </div>
      )}
    </form>
  );
}

export default LoadTestForm;
