import React, { useState, useEffect } from 'react';
import { Layout, Typography, Button, Space, Modal, Form, Input, Select, message, Spin, InputNumber, Checkbox, Tabs } from 'antd';
import { PlusOutlined, TeamOutlined, BarChartOutlined } from '@ant-design/icons';
import { invoke } from '@tauri-apps/api/tauri';
import TeamCard from '../components/TeamCard';
import TeamWorkflow from '../components/TeamWorkflow';

const { Content } = Layout;
const { Title } = Typography;
const { Option } = Select;

const Teams = () => {
  const [teams, setTeams] = useState([]);
  const [virtualCoworkers, setVirtualCoworkers] = useState([]);
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [loading, setLoading] = useState(false);
  const [loadingTeams, setLoadingTeams] = useState({});
  const [activeTab, setActiveTab] = useState('teams');
  const [selectedTeam, setSelectedTeam] = useState(null);
  const [form] = Form.useForm();

  useEffect(() => {
    fetchTeams();
    fetchVirtualCoworkers();
  }, []);

  const fetchTeams = async () => {
    setLoading(true);
    try {
      const response = await invoke('get_teams');
      setTeams(response.teams || []);
    } catch (error) {
      console.error('Error fetching teams:', error);
      message.error('Failed to fetch teams');
    } finally {
      setLoading(false);
    }
  };

  const fetchVirtualCoworkers = async () => {
    try {
      const response = await invoke('get_virtual_coworkers');
      setVirtualCoworkers(response.virtual_coworkers || []);
    } catch (error) {
      console.error('Error fetching virtual co-workers:', error);
      message.error('Failed to fetch virtual co-workers');
    }
  };

  const handleCreateTeam = async () => {
    try {
      await form.validateFields();
      const values = form.getFieldsValue();

      setLoading(true);
      await invoke('create_team', {
        name: values.name,
        description: values.description,
        virtualCoworkerNames: values.virtualCoworkers,
        collaborationMode: values.collaborationMode,
        maxParallelTasks: values.maxParallelTasks,
        enableConflictResolution: values.enableConflictResolution,
        enableTaskPrioritization: values.enableTaskPrioritization,
        enablePerformanceTracking: values.enablePerformanceTracking,
      });

      message.success(`Team ${values.name} created successfully`);
      setIsModalVisible(false);
      form.resetFields();
      fetchTeams();
    } catch (error) {
      console.error('Error creating team:', error);
      message.error('Failed to create team');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteTeam = async (name) => {
    try {
      setLoadingTeams({ ...loadingTeams, [name]: true });
      await invoke('delete_team', { name });
      message.success(`Team ${name} deleted successfully`);
      fetchTeams();
    } catch (error) {
      console.error('Error deleting team:', error);
      message.error('Failed to delete team');
    } finally {
      setLoadingTeams({ ...loadingTeams, [name]: false });
    }
  };

  const handleRunTeam = async (name, task, coordinator) => {
    try {
      setLoadingTeams({ ...loadingTeams, [name]: true });
      const response = await invoke('run_team', { name, task, coordinatorName: coordinator });
      message.success(`Task submitted with ID: ${response.task_id}`);
      return response;
    } catch (error) {
      console.error('Error running team:', error);
      message.error('Failed to run team');
      throw error;
    } finally {
      setLoadingTeams({ ...loadingTeams, [name]: false });
    }
  };

  const handleEditTeam = async (name, editForm) => {
    try {
      setLoadingTeams({ ...loadingTeams, [name]: true });
      await invoke('update_team', {
        name,
        newName: editForm.name,
        description: editForm.description,
        virtualCoworkerNames: editForm.virtualCoworkers,
        collaborationMode: editForm.collaborationMode,
        maxParallelTasks: editForm.maxParallelTasks,
        enableConflictResolution: editForm.enableConflictResolution,
        enableTaskPrioritization: editForm.enableTaskPrioritization,
        enablePerformanceTracking: editForm.enablePerformanceTracking,
      });
      message.success(`Team ${name} updated successfully`);
      fetchTeams();
    } catch (error) {
      console.error('Error updating team:', error);
      message.error('Failed to update team');
      throw error;
    } finally {
      setLoadingTeams({ ...loadingTeams, [name]: false });
    }
  };

  const handleSelectTeam = (team) => {
    setSelectedTeam(team);
    setActiveTab('workflow');
  };

  return (
    <Content style={{ padding: '24px' }}>
      <Space direction="vertical" size="large" style={{ width: '100%' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Title level={2}>Teams</Title>
          <Space>
            {selectedTeam && (
              <Button
                icon={<TeamOutlined />}
                type={activeTab === 'teams' ? 'primary' : 'default'}
                onClick={() => setActiveTab('teams')}
              >
                Teams
              </Button>
            )}
            {selectedTeam && (
              <Button
                icon={<BarChartOutlined />}
                type={activeTab === 'workflow' ? 'primary' : 'default'}
                onClick={() => setActiveTab('workflow')}
              >
                Workflow
              </Button>
            )}
            <Button
              type="primary"
              icon={<PlusOutlined />}
              onClick={() => setIsModalVisible(true)}
              disabled={loading || virtualCoworkers.length === 0}
            >
              Create Team
            </Button>
          </Space>
        </div>

        {loading ? (
          <div style={{ textAlign: 'center', padding: '50px' }}>
            <Spin size="large" />
          </div>
        ) : (
          <>
            {activeTab === 'teams' ? (
              <>
                {teams.length === 0 ? (
                  <div style={{ textAlign: 'center', padding: '50px' }}>
                    <p>No teams found. Create one to get started!</p>
                    {virtualCoworkers.length === 0 && (
                      <p>You need to create virtual co-workers first before creating a team.</p>
                    )}
                  </div>
                ) : (
                  teams.map((team) => (
                    <TeamCard
                      key={team.name}
                      team={team}
                      virtualCoworkers={virtualCoworkers}
                      onDelete={handleDeleteTeam}
                      onRun={(name, task, coordinator) => {
                        handleSelectTeam(team);
                        return handleRunTeam(name, task, coordinator);
                      }}
                      onEdit={handleEditTeam}
                      loading={loadingTeams[team.name]}
                    />
                  ))
                )}
              </>
            ) : (
              <TeamWorkflow
                team={selectedTeam}
                virtualCoworkers={virtualCoworkers}
                onRunTeam={handleRunTeam}
              />
            )}
          </>
        )}
      </Space>

      <Modal
        title="Create Team"
        open={isModalVisible}
        onOk={handleCreateTeam}
        onCancel={() => setIsModalVisible(false)}
        confirmLoading={loading}
        width={600}
      >
        <Form form={form} layout="vertical" initialValues={{
          collaborationMode: 'SEQUENTIAL',
          maxParallelTasks: 4,
          enableConflictResolution: true,
          enableTaskPrioritization: true,
          enablePerformanceTracking: true,
        }}>
          <Form.Item
            name="name"
            label="Name"
            rules={[{ required: true, message: 'Please enter a name' }]}
          >
            <Input placeholder="Enter team name" />
          </Form.Item>
          <Form.Item
            name="description"
            label="Description"
            rules={[{ required: true, message: 'Please enter a description' }]}
          >
            <Input placeholder="Enter team description" />
          </Form.Item>
          <Form.Item
            name="virtualCoworkers"
            label="Virtual Co-workers"
            rules={[{ required: true, message: 'Please select at least one virtual co-worker' }]}
          >
            <Select mode="multiple" placeholder="Select virtual co-workers">
              {virtualCoworkers.map((coworker) => (
                <Option key={coworker.name} value={coworker.name}>
                  {coworker.name}
                </Option>
              ))}
            </Select>
          </Form.Item>
          <Form.Item
            name="collaborationMode"
            label="Collaboration Mode"
            rules={[{ required: true, message: 'Please select a collaboration mode' }]}
          >
            <Select placeholder="Select collaboration mode">
              <Option value="SEQUENTIAL">Sequential</Option>
              <Option value="PARALLEL">Parallel</Option>
              <Option value="HIERARCHICAL">Hierarchical</Option>
              <Option value="CONSENSUS">Consensus</Option>
            </Select>
          </Form.Item>
          <Form.Item
            name="maxParallelTasks"
            label="Max Parallel Tasks"
            rules={[{ required: true, message: 'Please enter max parallel tasks' }]}
          >
            <InputNumber min={1} max={10} style={{ width: '100%' }} />
          </Form.Item>
          <Form.Item name="enableConflictResolution" valuePropName="checked">
            <Checkbox>Enable Conflict Resolution</Checkbox>
          </Form.Item>
          <Form.Item name="enableTaskPrioritization" valuePropName="checked">
            <Checkbox>Enable Task Prioritization</Checkbox>
          </Form.Item>
          <Form.Item name="enablePerformanceTracking" valuePropName="checked">
            <Checkbox>Enable Performance Tracking</Checkbox>
          </Form.Item>
        </Form>
      </Modal>
    </Content>
  );
};

export default Teams;
