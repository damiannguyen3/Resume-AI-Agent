import React, { useState } from 'react';
import './ResumeUpload.css';

const ResumeUpload = ({ onAnalyze, isAnalyzing }) => {
  const [resumeText, setResumeText] = useState('');
  const [activeTab, setActiveTab] = useState('paste');

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file && file.type === 'text/plain') {
      const reader = new FileReader();
      reader.onload = (e) => {
        setResumeText(e.target.result);
      };
      reader.readAsText(file);
    } else {
      alert('Please upload a .txt file');
    }
  };

  const handleAnalyze = () => {
    if (resumeText.trim()) {
      onAnalyze(resumeText);
    } else {
      alert('Please provide resume text');
    }
  };

  const handleSampleAnalyze = () => {
    // Use the sample resume
    onAnalyze('sample');
  };

  return (
    <div className="resume-upload-container">
      <h2 className="upload-title">Upload Your Resume</h2>
      
      {/* Tab Navigation */}
      <div className="tab-navigation">
        <button
          className={`tab-button ${activeTab === 'paste' ? 'active' : ''}`}
          onClick={() => setActiveTab('paste')}
        >
          Paste Text
        </button>
        <button
          className={`tab-button ${activeTab === 'upload' ? 'active' : ''}`}
          onClick={() => setActiveTab('upload')}
        >
          Upload File
        </button>
        <button
          className={`tab-button ${activeTab === 'sample' ? 'active' : ''}`}
          onClick={() => setActiveTab('sample')}
        >
          Try Sample
        </button>
      </div>

      {/* Tab Content */}
      {activeTab === 'paste' && (
        <div>
          <label className="form-label">
            Paste your resume text here:
          </label>
          <textarea
            value={resumeText}
            onChange={(e) => setResumeText(e.target.value)}
            className="resume-textarea"
            placeholder="Paste your resume content here..."
            disabled={isAnalyzing}
          />
        </div>
      )}

      {activeTab === 'upload' && (
        <div>
          <label className="form-label">
            Upload a .txt file:
          </label>
          <input
            type="file"
            accept=".txt"
            onChange={handleFileUpload}
            className="file-input"
            disabled={isAnalyzing}
          />
          {resumeText && (
            <div className="file-preview">
              <p className="preview-label">Preview:</p>
              <div className="preview-content">
                <pre className="preview-text">{resumeText.substring(0, 500)}...</pre>
              </div>
            </div>
          )}
        </div>
      )}

      {activeTab === 'sample' && (
        <div className="sample-container">
          <h3 className="sample-title">Try Sample Resume</h3>
          <p className="sample-description">
            Test the analyzer with our sample resume to see how it works.
          </p>
          <button
            onClick={handleSampleAnalyze}
            disabled={isAnalyzing}
            className={`analyze-button secondary ${isAnalyzing ? 'disabled' : ''}`}
          >
            {isAnalyzing ? (
              <div className="button-content">
                <div className="loading-spinner"></div>
                <span>Analyzing Sample...</span>
              </div>
            ) : (
              'Analyze Sample Resume'
            )}
          </button>
        </div>
      )}

      {/* Analyze Button for paste/upload tabs */}
      {activeTab !== 'sample' && (
        <div className="button-section">
          <button
            onClick={handleAnalyze}
            disabled={isAnalyzing || !resumeText.trim()}
            className={`analyze-button primary ${(isAnalyzing || !resumeText.trim()) ? 'disabled' : ''}`}
          >
            {isAnalyzing ? (
              <div className="button-content">
                <div className="loading-spinner"></div>
                <span>Analyzing Resume...</span>
              </div>
            ) : (
              '🔍 Analyze Resume'
            )}
          </button>
        </div>
      )}
    </div>
  );
};

export default ResumeUpload;
