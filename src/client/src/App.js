import React, { useState, useEffect } from 'react';
import './App.css';

import LoginForm from './LoginForm';
import Cookies from 'js-cookie';


import ComponentHost from './ComponentHost';
import ComponentPlayer from './ComponentPlayer';

function App() {
  const [activeTab, setActiveTab] = useState('prepare');
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const token = Cookies.get('authToken');
    const sessionToken = sessionStorage.getItem('authToken');
    if (token && token === sessionToken) {
      setIsAuthenticated(true);
    }
  }, []);

  const handleLogin = () => {
    setIsAuthenticated(true);
  };
  if (!isAuthenticated) {
    return <LoginForm onLogin={handleLogin} />;
  }

  return (
    <div className="App">
      <header className="App-header">
        <div>
          <button onClick={() => setActiveTab('host')}>Host Interface</button>
          <button onClick={() => setActiveTab('player')}>Player Interface</button>
        </div>
        {activeTab === 'host' && <ComponentHost />}
        {activeTab === 'player' && <ComponentPlayer />}
      </header>
    </div>
  );
}

export default App;
