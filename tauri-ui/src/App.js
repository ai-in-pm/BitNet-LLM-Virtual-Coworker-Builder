import React, { useState, useEffect } from 'react';
import { Routes, Route, Link, useLocation } from 'react-router-dom';
import { Layout, Menu, Typography, Button, message } from 'antd';
import {
  HomeOutlined,
  SettingOutlined,
  TeamOutlined,
  UserOutlined,
  CodeOutlined,
  ApiOutlined,
  DatabaseOutlined,
  ToolOutlined,
  PlayCircleOutlined,
  HistoryOutlined,
} from '@ant-design/icons';
import { invoke } from '@tauri-apps/api/tauri';

// Import pages
import Dashboard from './pages/Dashboard';
import Models from './pages/Models';
import VirtualCoworkers from './pages/VirtualCoworkers';
import Teams from './pages/Teams';
import Tasks from './pages/Tasks';
import Tools from './pages/Tools';
import Settings from './pages/Settings';
import ApiStatus from './components/ApiStatus';

const { Header, Content, Footer, Sider } = Layout;
const { Title } = Typography;

function App() {
  const [collapsed, setCollapsed] = useState(false);
  const [apiRunning, setApiRunning] = useState(false);
  const [apiPort, setApiPort] = useState(8000);
  const location = useLocation();
  
  useEffect(() => {
    // Check API server status on load
    checkApiStatus();
  }, []);
  
  const checkApiStatus = async () => {
    try {
      const running = await invoke('check_api_server');
      setApiRunning(running);
      
      if (running) {
        const port = await invoke('get_api_server_port');
        setApiPort(port);
      }
    } catch (error) {
      console.error('Error checking API status:', error);
    }
  };
  
  const startApiServer = async () => {
    try {
      await invoke('start_api_server', { port: apiPort });
      setApiRunning(true);
      message.success('API server started successfully');
    } catch (error) {
      message.error(`Failed to start API server: ${error}`);
    }
  };
  
  const stopApiServer = async () => {
    try {
      await invoke('stop_api_server');
      setApiRunning(false);
      message.success('API server stopped successfully');
    } catch (error) {
      message.error(`Failed to stop API server: ${error}`);
    }
  };
  
  const getSelectedKeys = () => {
    const path = location.pathname;
    if (path === '/') return ['dashboard'];
    if (path.startsWith('/models')) return ['models'];
    if (path.startsWith('/virtual-coworkers')) return ['virtual-coworkers'];
    if (path.startsWith('/teams')) return ['teams'];
    if (path.startsWith('/tasks')) return ['tasks'];
    if (path.startsWith('/tools')) return ['tools'];
    if (path.startsWith('/settings')) return ['settings'];
    return [];
  };
  
  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Sider collapsible collapsed={collapsed} onCollapse={setCollapsed}>
        <div className="logo" />
        <Menu theme="dark" selectedKeys={getSelectedKeys()} mode="inline">
          <Menu.Item key="dashboard" icon={<HomeOutlined />}>
            <Link to="/">Dashboard</Link>
          </Menu.Item>
          <Menu.Item key="models" icon={<DatabaseOutlined />}>
            <Link to="/models">Models</Link>
          </Menu.Item>
          <Menu.Item key="virtual-coworkers" icon={<UserOutlined />}>
            <Link to="/virtual-coworkers">Virtual Co-workers</Link>
          </Menu.Item>
          <Menu.Item key="teams" icon={<TeamOutlined />}>
            <Link to="/teams">Teams</Link>
          </Menu.Item>
          <Menu.Item key="tasks" icon={<PlayCircleOutlined />}>
            <Link to="/tasks">Tasks</Link>
          </Menu.Item>
          <Menu.Item key="tools" icon={<ToolOutlined />}>
            <Link to="/tools">Tools</Link>
          </Menu.Item>
          <Menu.Item key="settings" icon={<SettingOutlined />}>
            <Link to="/settings">Settings</Link>
          </Menu.Item>
        </Menu>
        <div className="version-info">
          <Typography.Text>v0.2.0</Typography.Text>
        </div>
      </Sider>
      <Layout className="site-layout">
        <Header className="site-layout-background" style={{ padding: 0, background: '#fff' }}>
          <div style={{ display: 'flex', alignItems: 'center', padding: '0 24px', justifyContent: 'space-between' }}>
            <Title level={3} style={{ margin: 0 }}>BitNet Virtual Co-worker Builder</Title>
            <ApiStatus
              running={apiRunning}
              port={apiPort}
              onStart={startApiServer}
              onStop={stopApiServer}
            />
          </div>
        </Header>
        <Content style={{ margin: '0 16px' }}>
          <div className="content-container">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/models" element={<Models />} />
              <Route path="/virtual-coworkers" element={<VirtualCoworkers />} />
              <Route path="/teams" element={<Teams />} />
              <Route path="/tasks" element={<Tasks />} />
              <Route path="/tools" element={<Tools />} />
              <Route path="/settings" element={<Settings />} />
            </Routes>
          </div>
        </Content>
        <Footer style={{ textAlign: 'center' }}>
          BitNet Virtual Co-worker Builder ©2023 Created by BitNet Team
        </Footer>
      </Layout>
    </Layout>
  );
}

export default App;
