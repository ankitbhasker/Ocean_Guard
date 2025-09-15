import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import './App.css';
import axios from 'axios';

// Components
import Navbar from './components/Navbar';
import Dashboard from './components/Dashboard';
import ReportForm from './components/ReportForm';
import MapView from './components/MapView';
import SocialMediaAnalytics from './components/SocialMediaAnalytics';
import AlertsPanel from './components/AlertsPanel';
import ReportsManager from './components/ReportsManager';
import LoginForm from './components/LoginForm';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Setup axios defaults
axios.defaults.headers.common['Authorization'] = 'Bearer mock_jwt_token';

function App() {
  const [currentUser, setCurrentUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    // Initialize the app
    initializeApp();
  }, []);

  const initializeApp = async () => {
    try {
      // For demo purposes, set a mock user
      const mockUser = {
        id: 'demo_user_id',
        username: 'demo_user',
        email: 'demo@oceanhazard.com',
        role: 'citizen',
        full_name: 'Demo User'
      };
      setCurrentUser(mockUser);

      // Fetch initial alerts
      await fetchAlerts();
    } catch (error) {
      console.error('Failed to initialize app:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchAlerts = async () => {
    try {
      const response = await axios.get(`${API}/alerts`);
      setAlerts(response.data);
    } catch (error) {
      console.error('Failed to fetch alerts:', error);
    }
  };

  const handleLogin = (user) => {
    setCurrentUser(user);
  };

  const handleLogout = () => {
    setCurrentUser(null);
    delete axios.defaults.headers.common['Authorization'];
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading Ocean Hazard Platform...</p>
        </div>
      </div>
    );
  }

  if (!currentUser) {
    return <LoginForm onLogin={handleLogin} />;
  }

  return (
    <div className="App min-h-screen bg-gray-50">
      <BrowserRouter>
        <Navbar user={currentUser} onLogout={handleLogout} />
        
        {/* Global Alerts Bar */}
        {alerts.length > 0 && (
          <div className="bg-red-600 text-white px-4 py-2">
            <div className="max-w-7xl mx-auto flex items-center">
              <span className="animate-pulse text-sm font-medium mr-2">🚨 ALERT:</span>
              <span className="text-sm">{alerts[0]?.message}</span>
            </div>
          </div>
        )}

        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <Routes>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="/dashboard" element={<Dashboard user={currentUser} />} />
            <Route path="/report" element={<ReportForm user={currentUser} />} />
            <Route path="/map" element={<MapView user={currentUser} />} />
            <Route path="/social-media" element={<SocialMediaAnalytics user={currentUser} />} />
            <Route path="/alerts" element={<AlertsPanel user={currentUser} alerts={alerts} onRefresh={fetchAlerts} />} />
            <Route path="/reports" element={<ReportsManager user={currentUser} />} />
          </Routes>
        </main>
      </BrowserRouter>
    </div>
  );
}

export default App;
