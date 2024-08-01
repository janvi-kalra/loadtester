import { useCallback } from 'react';

const useDownloadCSV = (data, filename) => {
  const downloadCSV = useCallback(() => {
    if (!data || !data.length) {
      return;
    }

    const headers = [
      'Timestamp', 'URL', 'QPS', 'Duration', '# Requests', '# Fails',
      'Median (ms)', '90 %ile', '99 %ile', 'Average (ms)', 'Min (ms)', 'Max (ms)',
      'Average size (bytes)', 'Error Rate (%)', 'Current RPS', 'Failures per sec'
    ];

    const csvRows = [
      headers.join(','),
      ...data.map(test => [
        new Date(test.timestamp * 1000).toLocaleString(),
        test.url,
        test.qps,
        test.duration,
        test.total_requests,
        test.failed_requests,
        (test.median_latency * 1000).toFixed(2),
        (test.p90_latency * 1000).toFixed(2),
        (test.p99_latency * 1000).toFixed(2),
        (test.avg_latency * 1000).toFixed(2),
        (test.min_latency * 1000).toFixed(2),
        (test.max_latency * 1000).toFixed(2),
        test.avg_size.toFixed(2),
        test.error_rate.toFixed(2),
        test.current_rps.toFixed(2),
        test.current_failures_per_sec.toFixed(2)
      ].join(','))
    ].join('\n');

    const blob = new Blob([csvRows], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.setAttribute('href', url);
    a.setAttribute('download', filename);
    a.click();
  }, [data, filename]);

  return downloadCSV;
};

export default useDownloadCSV;
