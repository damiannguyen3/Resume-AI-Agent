import React, { useState, useEffect } from 'react';
import './GoogleAuth.css';

const GoogleAuth = ({ onAuthChange }) => {
  const [isSignedIn, setIsSignedIn] = useState(false);
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const initializeGoogleAuth = () => {
      if (window.google) {
        window.google.accounts.id.initialize({
          client_id: process.env.REACT_APP_GOOGLE_CLIENT_ID,
          callback: handleCredentialResponse,
        });
        setIsLoading(false);
      }
    };

    const handleCredentialResponse = (response) => {
      // Decode the JWT token to get user info
      const userInfo = parseJwt(response.credential);
      if (userInfo) {
        const userData = {
          id: userInfo.sub,
          name: userInfo.name,
          email: userInfo.email,
          imageUrl: userInfo.picture,
        };
        setUser(userData);
        setIsSignedIn(true);
        onAuthChange(userData);
      }
    };

    const parseJwt = (token) => {
      try {
        return JSON.parse(atob(token.split('.')[1]));
      } catch (e) {
        console.error('Failed to parse JWT token:', e);
        return null;
      }
    };

    // Load Google Identity Services
    if (!window.google) {
      const script = document.createElement('script');
      script.src = 'https://accounts.google.com/gsi/client';
      script.onload = initializeGoogleAuth;
      script.onerror = () => {
        console.error('Failed to load Google Identity Services');
        setIsLoading(false);
      };
      document.head.appendChild(script);
    } else {
      initializeGoogleAuth();
    }
  }, [onAuthChange]);

  const signIn = () => {
    if (window.google) {
      window.google.accounts.id.prompt();
    }
  };

  const signOut = () => {
    setUser(null);
    setIsSignedIn(false);
    onAuthChange(null);
    // Clear any stored credentials
    if (window.google) {
      window.google.accounts.id.disableAutoSelect();
    }
  };

  if (isLoading) {
    return (
      <div className="loading-container">
        <p className="loading-text">Loading...</p>
      </div>
    );
  }

  return (
    <div className="google-auth-container">
      {isSignedIn ? (
        <div className="signed-in-content">
          <div className="user-info">
            <img
              src={user.imageUrl}
              alt={user.name}
              className="user-avatar"
            />
            <div>
              <h3 className="user-name">{user.name}</h3>
              <p className="user-email">{user.email}</p>
            </div>
          </div>
          <button
            onClick={signOut}
            className="sign-out-btn"
          >
            Sign Out
          </button>
        </div>
      ) : (
        <div className="sign-in-content">
          <h2 className="app-title">
            🔍 Resume SEO Analyzer
          </h2>
          <p className="app-description">
            Sign in with Google to analyze your resume and get personalized SEO recommendations
          </p>
          <button
            onClick={signIn}
            className="sign-in-btn"
          >
            <svg className="google-icon" viewBox="0 0 24 24">
              <path fill="currentColor" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
              <path fill="currentColor" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
              <path fill="currentColor" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
              <path fill="currentColor" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
            </svg>
            <span>Sign in with Google</span>
          </button>
        </div>
      )}
    </div>
  );
};

export default GoogleAuth;
