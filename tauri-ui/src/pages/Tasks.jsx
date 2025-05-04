import React, { useState, useEffect } from 'react';
import { Typography, Button, Space, Table, Tag, Modal, Form, Input, Select, message, Spin, Card } from 'antd';
import { PlusOutlined, EyeOutlined, DeleteOutlined, SyncOutlined } from '@ant-design/icons';
import { invoke } from '@tauri-apps/api/tauri';

const { Title, Text, Paragraph } = Typography;
const { TextArea } = Input;
const { Option } = Select;

const Tasks = () => {
  const [tasks, setTasks] = useState([]);
  const [virtualCoworkers, setVirtualCoworkers] = useState([]);
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(false);
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [isViewModalVisible, setIsViewModalVisible] = useState(false);
  const [selectedTask, setSelectedTask] = useState(null);
  const [form] = Form.useForm();

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      await fetchTasks();
      await fetchVirtualCoworkers();
      await fetchTeams();
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchTasks = async () => {
    try {
      // In a real implementation, we would fetch data from the API
      // For now, we'll use mock data
      
      // Simulate API call delay
      await new Promise(resolve => setTimeout(resolve, 500));
      
      const mockTasks = [
        {
          id: 'task_1',
          description: 'Research climate change and summarize findings',
          status: 'completed',
          result: 'Climate change is a significant global challenge caused primarily by human activities, particularly the burning of fossil fuels. Key findings include rising global temperatures, melting ice caps, and increasing frequency of extreme weather events. Addressing climate change requires both mitigation strategies to reduce emissions and adaptation measures to deal with the impacts.',
          assigned_to: 'ResearchCoworker',
          assigned_type: 'virtual_coworker',
          created_at: '2023-07-14 10:30:15',
          completed_at: '2023-07-14 10:35:22'
        },
        {
          id: 'task_2',
          description: 'Analyze sales data for Q2 2023',
          status: 'completed',
          result: 'Analysis of Q2 2023 sales data shows a 15% increase compared to Q1 2023 and a 22% increase compared to Q2 2022. The top-performing product categories were electronics (32% of total sales), home goods (28%), and apparel (18%). Regional analysis indicates strongest growth in the Western region (24%), followed by the Southern region (18%).',
          assigned_to: 'AnalystCoworker',
          assigned_type: 'virtual_coworker',
          created_at: '2023-07-15 14:45:30',
          completed_at: '2023-07-15 14:50:12'
        },
        {
          id: 'task_3',
          description: 'Generate marketing content for new product launch',
          status: 'in_progress',
          result: null,
          assigned_to: 'WriterCoworker',
          assigned_type: 'virtual_coworker',
          created_at: '2023-07-16 09:15:45',
          completed_at: null
        },
        {
          id: 'task_4',
          description: 'Research and write a report on renewable energy technologies',
          status: 'completed',
          result: 'Renewable energy technologies have seen significant advancements in recent years. Solar power efficiency has improved by 20% while costs have decreased by 80% over the past decade. Wind power is now cost-competitive with fossil fuels in many regions. Emerging technologies like green hydrogen and advanced battery storage are addressing intermittency issues. The report recommends increased investment in grid infrastructure and storage solutions to maximize renewable energy potential.',
          assigned_to: 'ResearchTeam',
          assigned_type: 'team',
          created_at: '2023-07-17 11:20:10',
          completed_at: '2023-07-17 11:30:45'
        },
        {
          id: 'task_5',
          description: 'Develop a simple calculator application',
          status: 'pending',
          result: null,
          assigned_to: 'DevelopmentTeam',
          assigned_type: 'team',
          created_at: '2023-07-18 16:30:25',
          completed_at: null
        }
      ];
      
      setTasks(mockTasks);
    } catch (error) {
      console.error('Error fetching tasks:', error);
      message.error('Failed to fetch tasks');
    }
  };

  const fetchVirtualCoworkers = async () => {
    try {
      // In a real implementation, we would fetch data from the API
      // For now, we'll use mock data
      
      // Simulate API call delay
      await new Promise(resolve => setTimeout(resolve, 300));
      
      const mockVirtualCoworkers = [
        {
          id: 1,
          name: 'ResearchCoworker',
          description: 'A virtual co-worker that specializes in research and information gathering'
        },
        {
          id: 2,
          name: 'AnalystCoworker',
          description: 'A virtual co-worker that specializes in data analysis'
        },
        {
          id: 3,
          name: 'WriterCoworker',
          description: 'A virtual co-worker that specializes in content creation'
        },
        {
          id: 4,
          name: 'CodeCoworker',
          description: 'A virtual co-worker that specializes in programming and code generation'
        },
        {
          id: 5,
          name: 'AssistantCoworker',
          description: 'A general-purpose virtual co-worker for everyday tasks'
        }
      ];
      
      setVirtualCoworkers(mockVirtualCoworkers);
    } catch (error) {
      console.error('Error fetching virtual co-workers:', error);
      message.error('Failed to fetch virtual co-workers');
    }
  };

  const fetchTeams = async () => {
    try {
      // In a real implementation, we would fetch data from the API
      // For now, we'll use mock data
      
      // Simulate API call delay
      await new Promise(resolve => setTimeout(resolve, 300));
      
      const mockTeams = [
        {
          id: 1,
          name: 'ResearchTeam',
          description: 'A team that specializes in research and analysis'
        },
        {
          id: 2,
          name: 'DevelopmentTeam',
          description: 'A team that specializes in software development'
        }
      ];
      
      setTeams(mockTeams);
    } catch (error) {
      console.error('Error fetching teams:', error);
      message.error('Failed to fetch teams');
    }
  };

  const handleCreateTask = async () => {
    try {
      await form.validateFields();
      const values = form.getFieldsValue();
      
      setLoading(true);
      
      // In a real implementation, we would call the API
      // For now, we'll just add the task to the local state
      
      // Simulate API call delay
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      const newTask = {
        id: `task_${Date.now()}`,
        description: values.description,
        status: 'pending',
        result: null,
        assigned_to: values.assigned_to,
        assigned_type: values.assigned_type,
        created_at: new Date().toISOString().replace('T', ' ').substring(0, 19),
        completed_at: null
      };
      
      setTasks([...tasks, newTask]);
      message.success('Task created successfully');
      setIsModalVisible(false);
      form.resetFields();
    } catch (error) {
      console.error('Error creating task:', error);
      message.error('Failed to create task');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteTask = async (taskId) => {
    try {
      setLoading(true);
      
      // In a real implementation, we would call the API
      // For now, we'll just remove the task from the local state
      
      // Simulate API call delay
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      setTasks(tasks.filter(task => task.id !== taskId));
      message.success('Task deleted successfully');
    } catch (error) {
      console.error('Error deleting task:', error);
      message.error('Failed to delete task');
    } finally {
      setLoading(false);
    }
  };

  const handleViewTask = (task) => {
    setSelectedTask(task);
    setIsViewModalVisible(true);
  };

  const getStatusTag = (status) => {
    switch (status) {
      case 'completed':
        return <Tag color="success">Completed</Tag>;
      case 'in_progress':
        return <Tag color="processing">In Progress</Tag>;
      case 'pending':
        return <Tag color="warning">Pending</Tag>;
      case 'failed':
        return <Tag color="error">Failed</Tag>;
      default:
        return <Tag>{status}</Tag>;
    }
  };

  const getAssignedToTag = (assignedTo, assignedType) => {
    if (assignedType === 'virtual_coworker') {
      return <Tag color="blue">{assignedTo}</Tag>;
    } else if (assignedType === 'team') {
      return <Tag color="purple">{assignedTo}</Tag>;
    }
    return <Tag>{assignedTo}</Tag>;
  };

  const columns = [
    {
      title: 'ID',
      dataIndex: 'id',
      key: 'id',
      width: 100
    },
    {
      title: 'Description',
      dataIndex: 'description',
      key: 'description',
      ellipsis: true
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      render: (status) => getStatusTag(status),
      filters: [
        { text: 'Completed', value: 'completed' },
        { text: 'In Progress', value: 'in_progress' },
        { text: 'Pending', value: 'pending' },
        { text: 'Failed', value: 'failed' }
      ],
      onFilter: (value, record) => record.status === value
    },
    {
      title: 'Assigned To',
      dataIndex: 'assigned_to',
      key: 'assigned_to',
      render: (assignedTo, record) => getAssignedToTag(assignedTo, record.assigned_type),
      filters: [
        { text: 'Virtual Co-workers', value: 'virtual_coworker' },
        { text: 'Teams', value: 'team' }
      ],
      onFilter: (value, record) => record.assigned_type === value
    },
    {
      title: 'Created At',
      dataIndex: 'created_at',
      key: 'created_at',
      sorter: (a, b) => new Date(a.created_at) - new Date(b.created_at)
    },
    {
      title: 'Actions',
      key: 'actions',
      render: (_, record) => (
        <Space>
          <Button
            icon={<EyeOutlined />}
            onClick={() => handleViewTask(record)}
          />
          <Button
            danger
            icon={<DeleteOutlined />}
            onClick={() => handleDeleteTask(record.id)}
          />
        </Space>
      )
    }
  ];

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
        <Title level={2}>Tasks</Title>
        <Space>
          <Button
            icon={<SyncOutlined />}
            onClick={fetchData}
            loading={loading}
          >
            Refresh
          </Button>
          <Button
            type="primary"
            icon={<PlusOutlined />}
            onClick={() => setIsModalVisible(true)}
            disabled={loading || (virtualCoworkers.length === 0 && teams.length === 0)}
          >
            Create Task
          </Button>
        </Space>
      </div>

      <Table
        dataSource={tasks}
        columns={columns}
        rowKey="id"
        loading={loading}
        pagination={{ pageSize: 10 }}
      />

      <Modal
        title="Create Task"
        open={isModalVisible}
        onOk={handleCreateTask}
        onCancel={() => setIsModalVisible(false)}
        confirmLoading={loading}
        width={600}
      >
        <Form form={form} layout="vertical">
          <Form.Item
            name="description"
            label="Description"
            rules={[{ required: true, message: 'Please enter a description' }]}
          >
            <TextArea
              rows={4}
              placeholder="Enter task description"
            />
          </Form.Item>
          
          <Form.Item
            name="assigned_type"
            label="Assign To"
            rules={[{ required: true, message: 'Please select assignment type' }]}
          >
            <Select
              placeholder="Select assignment type"
              onChange={() => form.setFieldsValue({ assigned_to: undefined })}
            >
              <Option value="virtual_coworker">Virtual Co-worker</Option>
              <Option value="team">Team</Option>
            </Select>
          </Form.Item>
          
          <Form.Item
            name="assigned_to"
            label="Select Assignee"
            rules={[{ required: true, message: 'Please select an assignee' }]}
            dependencies={['assigned_type']}
          >
            <Select placeholder="Select assignee">
              {form.getFieldValue('assigned_type') === 'virtual_coworker' && 
                virtualCoworkers.map(coworker => (
                  <Option key={coworker.id} value={coworker.name}>
                    {coworker.name}
                  </Option>
                ))
              }
              {form.getFieldValue('assigned_type') === 'team' && 
                teams.map(team => (
                  <Option key={team.id} value={team.name}>
                    {team.name}
                  </Option>
                ))
              }
            </Select>
          </Form.Item>
        </Form>
      </Modal>

      <Modal
        title="Task Details"
        open={isViewModalVisible}
        onCancel={() => setIsViewModalVisible(false)}
        footer={[
          <Button key="close" onClick={() => setIsViewModalVisible(false)}>
            Close
          </Button>
        ]}
        width={700}
      >
        {selectedTask && (
          <Card>
            <div style={{ marginBottom: '16px' }}>
              <Text strong>ID:</Text> {selectedTask.id}
            </div>
            <div style={{ marginBottom: '16px' }}>
              <Text strong>Description:</Text>
              <Paragraph style={{ marginTop: '8px' }}>{selectedTask.description}</Paragraph>
            </div>
            <div style={{ marginBottom: '16px' }}>
              <Text strong>Status:</Text> {getStatusTag(selectedTask.status)}
            </div>
            <div style={{ marginBottom: '16px' }}>
              <Text strong>Assigned To:</Text> {getAssignedToTag(selectedTask.assigned_to, selectedTask.assigned_type)}
              <Text> ({selectedTask.assigned_type === 'virtual_coworker' ? 'Virtual Co-worker' : 'Team'})</Text>
            </div>
            <div style={{ marginBottom: '16px' }}>
              <Text strong>Created At:</Text> {selectedTask.created_at}
            </div>
            {selectedTask.completed_at && (
              <div style={{ marginBottom: '16px' }}>
                <Text strong>Completed At:</Text> {selectedTask.completed_at}
              </div>
            )}
            {selectedTask.result && (
              <div>
                <Text strong>Result:</Text>
                <Card style={{ marginTop: '8px', background: '#f5f5f5' }}>
                  <Paragraph>{selectedTask.result}</Paragraph>
                </Card>
              </div>
            )}
          </Card>
        )}
      </Modal>
    </div>
  );
};

export default Tasks;
