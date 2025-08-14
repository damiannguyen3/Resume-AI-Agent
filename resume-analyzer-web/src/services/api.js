import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || (
  process.env.NODE_ENV === 'production' 
    ? '' // Use relative URLs in production (same domain)
    : 'http://localhost:8000'
);

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// API functions
export const analyzeResume = async (resumeText, userEmail = null) => {
  try {
    const response = await api.post('/api/analyze', {
      resume_text: resumeText,
      user_email: userEmail,
    });
    return response.data;
  } catch (error) {
    console.error('Error analyzing resume:', error);
    throw new Error(error.response?.data?.detail || 'Failed to analyze resume');
  }
};

export const analyzeSampleResume = async () => {
  try {
    const response = await api.post('/api/analyze/sample');
    return response.data;
  } catch (error) {
    console.error('Error analyzing sample resume:', error);
    throw new Error(error.response?.data?.detail || 'Failed to analyze sample resume');
  }
};

export const checkHealth = async () => {
  try {
    const response = await api.get('/health');
    return response.data;
  } catch (error) {
    console.error('Health check failed:', error);
    throw new Error('API is not available');
  }
};

export default api;
