import React, { useState, useEffect } from 'react';
import { Card, Typography, Statistic, Row, Col, Button, List, Spin } from 'antd';
import { UserOutlined, TeamOutlined, DatabaseOutlined, ToolOutlined, PlayCircleOutlined } from '@ant-design/icons';
import { Link } from 'react-router-dom';

const { Title, Text } = Typography;

const Dashboard = () => {
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({
    models: 0,
    virtualCoworkers: 0,
    teams: 0,
    tasks: 0,
    tools: 0
  });
  const [recentTasks, setRecentTasks] = useState([]);
  
  useEffect(() => {
    // Fetch dashboard data
    fetchDashboardData();
  }, []);
  
  const fetchDashboardData = async () => {
    setLoading(true);
    
    try {
      // In a real implementation, we would fetch data from the API
      // For now, we'll use mock data
      
      // Simulate API call delay
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      setStats({
        models: 3,
        virtualCoworkers: 5,
        teams: 2,
        tasks: 12,
        tools: 8
      });
      
      setRecentTasks([
        {
          id: 'task_1',
          description: 'Research climate change',
          status: 'completed',
          timestamp: '2023-07-15 14:30:22'
        },
        {
          id: 'task_2',
          description: 'Analyze sales data',
          status: 'completed',
          timestamp: '2023-07-15 13:45:10'
        },
        {
          id: 'task_3',
          description: 'Generate marketing content',
          status: 'in_progress',
          timestamp: '2023-07-15 13:20:05'
        },
        {
          id: 'task_4',
          description: 'Summarize research paper',
          status: 'pending',
          timestamp: '2023-07-15 12:15:30'
        }
      ]);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };
  
  const getStatusColor = (status) => {
    switch (status) {
      case 'completed':
        return '#52c41a';
      case 'in_progress':
        return '#1890ff';
      case 'pending':
        return '#faad14';
      case 'failed':
        return '#f5222d';
      default:
        return '#d9d9d9';
    }
  };
  
  return (
    <div>
      <Title level={2}>Dashboard</Title>
      
      {loading ? (
        <div style={{ textAlign: 'center', padding: '50px' }}>
          <Spin size="large" />
        </div>
      ) : (
        <>
          <Row gutter={16} style={{ marginBottom: '24px' }}>
            <Col span={4}>
              <Card>
                <Statistic
                  title="Models"
                  value={stats.models}
                  prefix={<DatabaseOutlined />}
                />
                <div style={{ marginTop: '12px', textAlign: 'center' }}>
                  <Link to="/models">
                    <Button type="primary" size="small">View</Button>
                  </Link>
                </div>
              </Card>
            </Col>
            <Col span={4}>
              <Card>
                <Statistic
                  title="Virtual Co-workers"
                  value={stats.virtualCoworkers}
                  prefix={<UserOutlined />}
                />
                <div style={{ marginTop: '12px', textAlign: 'center' }}>
                  <Link to="/virtual-coworkers">
                    <Button type="primary" size="small">View</Button>
                  </Link>
                </div>
              </Card>
            </Col>
            <Col span={4}>
              <Card>
                <Statistic
                  title="Teams"
                  value={stats.teams}
                  prefix={<TeamOutlined />}
                />
                <div style={{ marginTop: '12px', textAlign: 'center' }}>
                  <Link to="/teams">
                    <Button type="primary" size="small">View</Button>
                  </Link>
                </div>
              </Card>
            </Col>
            <Col span={4}>
              <Card>
                <Statistic
                  title="Tasks"
                  value={stats.tasks}
                  prefix={<PlayCircleOutlined />}
                />
                <div style={{ marginTop: '12px', textAlign: 'center' }}>
                  <Link to="/tasks">
                    <Button type="primary" size="small">View</Button>
                  </Link>
                </div>
              </Card>
            </Col>
            <Col span={4}>
              <Card>
                <Statistic
                  title="Tools"
                  value={stats.tools}
                  prefix={<ToolOutlined />}
                />
                <div style={{ marginTop: '12px', textAlign: 'center' }}>
                  <Link to="/tools">
                    <Button type="primary" size="small">View</Button>
                  </Link>
                </div>
              </Card>
            </Col>
          </Row>
          
          <Card title="Recent Tasks" style={{ marginBottom: '24px' }}>
            <List
              dataSource={recentTasks}
              renderItem={task => (
                <List.Item
                  actions={[
                    <Link to={`/tasks/${task.id}`}>
                      <Button type="link">View</Button>
                    </Link>
                  ]}
                >
                  <List.Item.Meta
                    title={task.description}
                    description={
                      <div>
                        <Text type="secondary">{task.timestamp}</Text>
                        <div style={{ marginTop: '4px' }}>
                          <Text
                            style={{
                              color: getStatusColor(task.status),
                              textTransform: 'capitalize'
                            }}
                          >
                            {task.status.replace('_', ' ')}
                          </Text>
                        </div>
                      </div>
                    }
                  />
                </List.Item>
              )}
            />
          </Card>
          
          <Card title="Quick Actions">
            <Row gutter={16}>
              <Col span={6}>
                <Link to="/models/create">
                  <Button type="primary" block>
                    Create Model
                  </Button>
                </Link>
              </Col>
              <Col span={6}>
                <Link to="/virtual-coworkers/create">
                  <Button type="primary" block>
                    Create Virtual Co-worker
                  </Button>
                </Link>
              </Col>
              <Col span={6}>
                <Link to="/teams/create">
                  <Button type="primary" block>
                    Create Team
                  </Button>
                </Link>
              </Col>
              <Col span={6}>
                <Link to="/tasks/create">
                  <Button type="primary" block>
                    Create Task
                  </Button>
                </Link>
              </Col>
            </Row>
          </Card>
        </>
      )}
    </div>
  );
};

export default Dashboard;
