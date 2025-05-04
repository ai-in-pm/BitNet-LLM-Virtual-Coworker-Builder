import React, { useState } from 'react';
import { Layout, Menu, Typography, Button, Drawer, Space } from 'antd';
import { Link, useLocation } from 'react-router-dom';
import {
  DashboardOutlined,
  CodeOutlined,
  UserOutlined,
  TeamOutlined,
  ToolOutlined,
  SettingOutlined,
  MenuOutlined,
  GithubOutlined,
  QuestionCircleOutlined
} from '@ant-design/icons';

const { Header, Content, Sider } = Layout;
const { Title, Text } = Typography;

const AppLayout = ({ children }) => {
  const [collapsed, setCollapsed] = useState(false);
  const [mobileDrawerVisible, setMobileDrawerVisible] = useState(false);
  const location = useLocation();

  const menuItems = [
    {
      key: '/',
      icon: <DashboardOutlined />,
      label: <Link to="/">Dashboard</Link>,
    },
    {
      key: '/models',
      icon: <CodeOutlined />,
      label: <Link to="/models">Models</Link>,
    },
    {
      key: '/virtual-coworkers',
      icon: <UserOutlined />,
      label: <Link to="/virtual-coworkers">Virtual Co-workers</Link>,
    },
    {
      key: '/teams',
      icon: <TeamOutlined />,
      label: <Link to="/teams">Teams</Link>,
    },
    {
      key: '/tasks',
      icon: <DashboardOutlined />,
      label: <Link to="/tasks">Tasks</Link>,
    },
    {
      key: '/tools',
      icon: <ToolOutlined />,
      label: <Link to="/tools">Tools</Link>,
    },
    {
      key: '/settings',
      icon: <SettingOutlined />,
      label: <Link to="/settings">Settings</Link>,
    },
  ];

  const toggleDrawer = () => {
    setMobileDrawerVisible(!mobileDrawerVisible);
  };

  // Determine if we're on mobile
  const isMobile = window.innerWidth < 768;

  return (
    <Layout style={{ minHeight: '100vh' }}>
      {/* Desktop Sidebar */}
      {!isMobile && (
        <Sider
          collapsible
          collapsed={collapsed}
          onCollapse={(value) => setCollapsed(value)}
          style={{
            overflow: 'auto',
            height: '100vh',
            position: 'fixed',
            left: 0,
            top: 0,
            bottom: 0,
          }}
        >
          <div style={{ height: 32, margin: 16, textAlign: 'center' }}>
            <Title level={5} style={{ color: 'white', margin: 0 }}>
              {collapsed ? 'BVC' : 'BitNet VC Builder'}
            </Title>
          </div>
          <Menu
            theme="dark"
            mode="inline"
            selectedKeys={[location.pathname]}
            items={menuItems}
          />
          <div style={{ position: 'absolute', bottom: 0, width: '100%', padding: '16px', textAlign: 'center' }}>
            <Space direction="vertical" size="small">
              <Button
                type="link"
                icon={<GithubOutlined />}
                href="https://github.com/bitnet/bitnet-vc-builder"
                target="_blank"
                style={{ color: 'rgba(255, 255, 255, 0.65)' }}
              >
                {!collapsed && 'GitHub'}
              </Button>
              <Button
                type="link"
                icon={<QuestionCircleOutlined />}
                href="https://github.com/bitnet/bitnet-vc-builder/wiki"
                target="_blank"
                style={{ color: 'rgba(255, 255, 255, 0.65)' }}
              >
                {!collapsed && 'Help'}
              </Button>
              <Text style={{ color: 'rgba(255, 255, 255, 0.45)', fontSize: '12px' }}>
                {!collapsed && 'v0.2.0'}
              </Text>
            </Space>
          </div>
        </Sider>
      )}

      <Layout style={{ marginLeft: isMobile ? 0 : (collapsed ? 80 : 200) }}>
        {/* Mobile Header */}
        {isMobile && (
          <Header style={{ padding: '0 16px', background: '#fff', boxShadow: '0 1px 4px rgba(0, 21, 41, 0.08)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <Button
                type="text"
                icon={<MenuOutlined />}
                onClick={toggleDrawer}
                style={{ marginRight: 16 }}
              />
              <Title level={4} style={{ margin: 0 }}>BitNet VC Builder</Title>
            </div>
          </Header>
        )}

        {/* Mobile Drawer */}
        {isMobile && (
          <Drawer
            title="BitNet VC Builder"
            placement="left"
            onClose={toggleDrawer}
            open={mobileDrawerVisible}
            bodyStyle={{ padding: 0 }}
          >
            <Menu
              mode="inline"
              selectedKeys={[location.pathname]}
              items={menuItems}
              style={{ height: '100%' }}
            />
            <div style={{ position: 'absolute', bottom: 0, width: '100%', padding: '16px', textAlign: 'center' }}>
              <Space direction="vertical" size="small">
                <Button
                  type="link"
                  icon={<GithubOutlined />}
                  href="https://github.com/bitnet/bitnet-vc-builder"
                  target="_blank"
                >
                  GitHub
                </Button>
                <Button
                  type="link"
                  icon={<QuestionCircleOutlined />}
                  href="https://github.com/bitnet/bitnet-vc-builder/wiki"
                  target="_blank"
                >
                  Help
                </Button>
                <Text style={{ color: 'rgba(0, 0, 0, 0.45)', fontSize: '12px' }}>
                  v0.2.0
                </Text>
              </Space>
            </div>
          </Drawer>
        )}

        <Content style={{ margin: '24px 16px', overflow: 'initial' }}>
          <div style={{ padding: 24, background: '#fff', minHeight: 360 }}>
            {children}
          </div>
        </Content>
      </Layout>
    </Layout>
  );
};

export default AppLayout;
