import React from 'react';

function TestResults({ results }) {
  return (
    <div>
      <h2>Test Results</h2>
      <div className="table-container">
        <table>
          <thead>
            <tr>
              <th>Timestamp</th>
              <th>URL</th>
              <th># Requests</th>
              <th># Fails</th>
              <th>Median (ms)</th>
              <th>90 %ile</th>
              <th>99 %ile</th>
              <th>Average (ms)</th>
              <th>Min (ms)</th>
              <th>Max (ms)</th>
              <th>Average size (bytes)</th>
              <th>Error Rate (%)</th>
              <th>Current RPS</th>
              <th>Failures per sec</th>
            </tr>
          </thead>
          <tbody>
            {Array.isArray(results) && results.map((test, index) => (
              <tr key={index}>
                <td>{new Date(test.timestamp * 1000).toLocaleString()}</td>
                <td><a href={test.url} target="_blank" rel="noopener noreferrer">{test.url}</a></td>
                <td>{test.total_requests}</td>
                <td>{test.failed_requests}</td>
                <td>{(test.median_latency * 1000).toFixed(2)}</td>
                <td>{(test.p90_latency * 1000).toFixed(2)}</td>
                <td>{(test.p99_latency * 1000).toFixed(2)}</td>
                <td>{(test.avg_latency * 1000).toFixed(2)}</td>
                <td>{(test.min_latency * 1000).toFixed(2)}</td>
                <td>{(test.max_latency * 1000).toFixed(2)}</td>
                <td>{test.avg_size.toFixed(2)}</td>
                <td>{test.error_rate.toFixed(2)}</td>
                <td>{test.current_rps.toFixed(2)}</td>
                <td>{test.current_failures_per_sec.toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default TestResults;
