import React from 'react';
import './AnalysisResults.css';

const AnalysisResults = ({ results }) => {
  if (!results) return null;

  const getPriorityColor = (priority) => {
    switch (priority.toLowerCase()) {
      case 'high': return 'priority-high';
      case 'medium': return 'priority-medium';
      case 'low': return 'priority-low';
      default: return 'priority-default';
    }
  };

  const getPriorityEmoji = (priority) => {
    switch (priority.toLowerCase()) {
      case 'high': return '🔴';
      case 'medium': return '🟡';
      case 'low': return '🟢';
      default: return '⚪';
    }
  };

  const getScoreColor = (score) => {
    if (score >= 8) return 'score-green';
    if (score >= 6) return 'score-yellow';
    if (score >= 4) return 'score-orange';
    return 'score-red';
  };

  return (
    <div className="analysis-results">
      {/* Header */}
      <div className="results-container">
        <div className="results-header">
          <h2 className="results-title">
            ✅ Analysis Complete!
          </h2>
          <div className="results-divider"></div>
        </div>
        
        <div className="results-grid">
          <div className="grid-item">
            <h3 className="grid-label">Current Role</h3>
            <p className="grid-value">{results.current_role}</p>
          </div>
          <div className="grid-item">
            <h3 className="grid-label">Target Industry</h3>
            <p className="grid-value">{results.target_industry}</p>
          </div>
          <div className="grid-item">
            <h3 className="grid-label">Overall SEO Score</h3>
            <p className={`grid-value overall-score ${getScoreColor(results.overall_score)}`}>
              {results.overall_score}/10
            </p>
          </div>
        </div>
      </div>

      {/* Score Breakdown */}
      <div className="results-container">
        <h3 className="section-title">📊 Score Breakdown</h3>
        <div className="score-grid">
          <div className="score-item">
            <span className="score-label">🔤 Keywords</span>
            <span className={`score-value ${getScoreColor(results.score_breakdown.keyword_score)}`}>
              {results.score_breakdown.keyword_score}/10
            </span>
          </div>
          <div className="score-item">
            <span className="score-label">🤖 ATS Compatibility</span>
            <span className={`score-value ${getScoreColor(results.score_breakdown.ats_compatibility)}`}>
              {results.score_breakdown.ats_compatibility}/10
            </span>
          </div>
          <div className="score-item">
            <span className="score-label">🏭 Industry Terms</span>
            <span className={`score-value ${getScoreColor(results.score_breakdown.industry_terms)}`}>
              {results.score_breakdown.industry_terms}/10
            </span>
          </div>
          <div className="score-item">
            <span className="score-label">💪 Skills Optimization</span>
            <span className={`score-value ${getScoreColor(results.score_breakdown.skills_optimization)}`}>
              {results.score_breakdown.skills_optimization}/10
            </span>
          </div>
          <div className="score-item">
            <span className="score-label">📄 Format & Structure</span>
            <span className={`score-value ${getScoreColor(results.score_breakdown.format_structure)}`}>
              {results.score_breakdown.format_structure}/10
            </span>
          </div>
        </div>
        <div className="explanation-box">
          <h4 className="explanation-title">💡 Explanation:</h4>
          <p className="explanation-text">{results.score_breakdown.explanation}</p>
        </div>
      </div>

      {/* Summary */}
      <div className="results-container">
        <h3 className="section-title">📝 Summary</h3>
        <p className="summary-text">{results.summary}</p>
      </div>

      {/* Missing Keywords */}
      {results.missing_keywords && results.missing_keywords.length > 0 && (
        <div className="results-container">
          <h3 className="section-title">🔍 Missing Keywords</h3>
          <div className="keywords-container">
            {results.missing_keywords.map((keyword, index) => (
              <span
                key={index}
                className="keyword-tag"
              >
                {keyword}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* SEO Recommendations */}
      <div className="results-container">
        <h3 className="section-title">
          💡 SEO Recommendations ({results.seo_recommendations.length} total)
        </h3>
        <div className="results-divider"></div>
        
        <div className="recommendations-list">
          {results.seo_recommendations.map((rec, index) => (
            <div key={index} className="recommendation-item">
              <div className="recommendation-header">
                <span className="priority-emoji">{getPriorityEmoji(rec.priority)}</span>
                <div className="recommendation-content">
                  <div className="recommendation-meta">
                    <h4 className="recommendation-category">{rec.category}</h4>
                    <span className={`priority-badge ${getPriorityColor(rec.priority)}`}>
                      {rec.priority} Priority
                    </span>
                  </div>
                  <div className="recommendation-text">
                    <p className="recommendation-description">
                      <span className="text-bold">💡 Recommendation:</span> {rec.recommendation}
                    </p>
                  </div>
                  <div className="implementation-box">
                    <p className="implementation-text">
                      <span className="text-bold">🛠️ How to implement:</span> {rec.implementation}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default AnalysisResults;
