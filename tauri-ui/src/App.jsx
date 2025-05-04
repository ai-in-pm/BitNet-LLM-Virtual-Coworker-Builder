import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ConfigProvider } from 'antd';

import AppLayout from './components/AppLayout';
import Dashboard from './pages/Dashboard';
import Models from './pages/Models';
import VirtualCoworkers from './pages/VirtualCoworkers';
import Teams from './pages/Teams';
import Tasks from './pages/Tasks';
import Tools from './pages/Tools';
import Settings from './pages/Settings';

const App = () => {
  return (
    <ConfigProvider
      theme={{
        token: {
          colorPrimary: '#1677ff',
        },
      }}
    >
      <Router>
        <AppLayout>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/models" element={<Models />} />
            <Route path="/virtual-coworkers" element={<VirtualCoworkers />} />
            <Route path="/teams" element={<Teams />} />
            <Route path="/tasks" element={<Tasks />} />
            <Route path="/tools" element={<Tools />} />
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </AppLayout>
      </Router>
    </ConfigProvider>
  );
};

export default App;
