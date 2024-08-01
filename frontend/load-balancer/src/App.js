import React, { useState, useEffect } from 'react';
import LoadTestForm from './LoadTestForm';
import TestResults from './TestResults';
import useDownloadCSV from './useDownloadCSV';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faDownload } from '@fortawesome/free-solid-svg-icons';
import './App.css';

function App() {
  const [results, setResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    fetchResults();
  }, []);

  const fetchResults = async () => {
    const response = await fetch('http://127.0.0.1:8000/results');
    const data = await response.json();
    setResults(Array.isArray(data) ? data : []);
  };

  const downloadCSV = useDownloadCSV(results, 'test_results.csv');

  return (
    <div className="App">
      <h1>Load Test Dashboard</h1>
      <LoadTestForm setResults={setResults} setIsLoading={setIsLoading} isLoading={isLoading} fetchResults={fetchResults} />
      <TestResults results={results} />
      <div className="download-icon" onClick={downloadCSV} title="Download CSV">
        <FontAwesomeIcon icon={faDownload} size="2x" />
      </div>
    </div>
  );
}

export default App;
