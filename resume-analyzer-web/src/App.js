import React, { useState } from 'react';
import './App.css';
import ResumeUpload from './components/ResumeUpload';
import AnalysisResults from './components/AnalysisResults';
import { analyzeResume, analyzeSampleResume } from './services/api';

function App() {
  const [analysisResults, setAnalysisResults] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [error, setError] = useState(null);

  const handleAnalyze = async (resumeText) => {
    setIsAnalyzing(true);
    setError(null);
    setAnalysisResults(null);

    try {
      let results;
      if (resumeText === 'sample') {
        results = await analyzeSampleResume();
      } else {
        results = await analyzeResume(resumeText);
      }
      setAnalysisResults(results);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="App">
      <div className="app-container">
        {/* Header */}
        <div className="app-title">
          🔍 Resume SEO Analyzer
        </div>

        {/* Resume Upload */}
        <ResumeUpload 
          onAnalyze={handleAnalyze} 
          isAnalyzing={isAnalyzing}
        />

        {/* Error Display */}
        {error && (
          <div className="error-message">
            <strong>Analysis Failed:</strong> {error}
          </div>
        )}

        {/* Analysis Results */}
        <AnalysisResults results={analysisResults} />
      </div>
    </div>
  );
}

export default App;
