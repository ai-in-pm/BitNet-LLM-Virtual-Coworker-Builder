import React, { useState } from 'react';
import { Card, Button, Typography, Space, Tag, Modal, Input, Form, Select, Spin, Checkbox } from 'antd';
import { EditOutlined, DeleteOutlined, PlayCircleOutlined, TeamOutlined } from '@ant-design/icons';
import { invoke } from '@tauri-apps/api/tauri';

const { Title, Text } = Typography;
const { TextArea } = Input;
const { Option } = Select;

const TeamCard = ({ team, virtualCoworkers, onDelete, onRun, onEdit, loading }) => {
  const [isRunModalVisible, setIsRunModalVisible] = useState(false);
  const [isEditModalVisible, setIsEditModalVisible] = useState(false);
  const [task, setTask] = useState('');
  const [coordinator, setCoordinator] = useState(null);
  const [editForm, setEditForm] = useState({
    name: team.name,
    description: team.description,
    virtualCoworkers: team.virtualCoworkers || [],
    collaborationMode: team.collaborationMode || 'SEQUENTIAL',
    maxParallelTasks: team.maxParallelTasks || 4,
    enableConflictResolution: team.enableConflictResolution !== false,
    enableTaskPrioritization: team.enableTaskPrioritization !== false,
    enablePerformanceTracking: team.enablePerformanceTracking !== false,
  });
  const [runLoading, setRunLoading] = useState(false);
  const [editLoading, setEditLoading] = useState(false);

  const handleRun = async () => {
    setRunLoading(true);
    try {
      await onRun(team.name, task, coordinator);
      setIsRunModalVisible(false);
      setTask('');
      setCoordinator(null);
    } catch (error) {
      console.error('Error running team:', error);
    } finally {
      setRunLoading(false);
    }
  };

  const handleEdit = async () => {
    setEditLoading(true);
    try {
      await onEdit(team.name, editForm);
      setIsEditModalVisible(false);
    } catch (error) {
      console.error('Error editing team:', error);
    } finally {
      setEditLoading(false);
    }
  };

  const handleDelete = async () => {
    try {
      await onDelete(team.name);
    } catch (error) {
      console.error('Error deleting team:', error);
    }
  };

  return (
    <>
      <Card
        title={
          <Space>
            <Title level={4}>{team.name}</Title>
            {loading && <Spin size="small" />}
          </Space>
        }
        extra={
          <Space>
            <Button
              type="primary"
              icon={<PlayCircleOutlined />}
              onClick={() => setIsRunModalVisible(true)}
              disabled={loading}
            >
              Run
            </Button>
            <Button
              icon={<EditOutlined />}
              onClick={() => setIsEditModalVisible(true)}
              disabled={loading}
            >
              Edit
            </Button>
            <Button
              danger
              icon={<DeleteOutlined />}
              onClick={handleDelete}
              disabled={loading}
            >
              Delete
            </Button>
          </Space>
        }
        style={{ width: '100%', marginBottom: 16 }}
      >
        <Space direction="vertical" style={{ width: '100%' }}>
          <Text>{team.description}</Text>
          <Space>
            <Tag color="blue">Mode: {team.collaborationMode}</Tag>
            <Tag color="green">Virtual Co-workers: {team.virtualCoworkers?.length || 0}</Tag>
          </Space>
        </Space>
      </Card>

      <Modal
        title={`Run ${team.name}`}
        open={isRunModalVisible}
        onOk={handleRun}
        onCancel={() => setIsRunModalVisible(false)}
        confirmLoading={runLoading}
      >
        <Form layout="vertical">
          <Form.Item label="Task">
            <TextArea
              rows={4}
              value={task}
              onChange={(e) => setTask(e.target.value)}
              placeholder="Enter the task for the team..."
            />
          </Form.Item>
          <Form.Item label="Coordinator (Optional)">
            <Select
              value={coordinator}
              onChange={(value) => setCoordinator(value)}
              style={{ width: '100%' }}
              allowClear
              placeholder="Select a coordinator virtual co-worker"
            >
              {team.virtualCoworkers?.map((coworker) => (
                <Option key={coworker} value={coworker}>
                  {coworker}
                </Option>
              ))}
            </Select>
          </Form.Item>
        </Form>
      </Modal>

      <Modal
        title={`Edit ${team.name}`}
        open={isEditModalVisible}
        onOk={handleEdit}
        onCancel={() => setIsEditModalVisible(false)}
        confirmLoading={editLoading}
        width={600}
      >
        <Form layout="vertical">
          <Form.Item label="Name">
            <Input
              value={editForm.name}
              onChange={(e) => setEditForm({ ...editForm, name: e.target.value })}
            />
          </Form.Item>
          <Form.Item label="Description">
            <Input
              value={editForm.description}
              onChange={(e) => setEditForm({ ...editForm, description: e.target.value })}
            />
          </Form.Item>
          <Form.Item label="Virtual Co-workers">
            <Select
              mode="multiple"
              value={editForm.virtualCoworkers}
              onChange={(value) => setEditForm({ ...editForm, virtualCoworkers: value })}
              style={{ width: '100%' }}
              placeholder="Select virtual co-workers"
            >
              {virtualCoworkers.map((coworker) => (
                <Option key={coworker.name} value={coworker.name}>
                  {coworker.name}
                </Option>
              ))}
            </Select>
          </Form.Item>
          <Form.Item label="Collaboration Mode">
            <Select
              value={editForm.collaborationMode}
              onChange={(value) => setEditForm({ ...editForm, collaborationMode: value })}
              style={{ width: '100%' }}
            >
              <Option value="SEQUENTIAL">Sequential</Option>
              <Option value="PARALLEL">Parallel</Option>
              <Option value="HIERARCHICAL">Hierarchical</Option>
              <Option value="CONSENSUS">Consensus</Option>
            </Select>
          </Form.Item>
          <Form.Item label="Max Parallel Tasks">
            <Input
              type="number"
              value={editForm.maxParallelTasks}
              onChange={(e) => setEditForm({ ...editForm, maxParallelTasks: parseInt(e.target.value) })}
              min={1}
              max={10}
            />
          </Form.Item>
          <Form.Item>
            <Checkbox
              checked={editForm.enableConflictResolution}
              onChange={(e) => setEditForm({ ...editForm, enableConflictResolution: e.target.checked })}
            >
              Enable Conflict Resolution
            </Checkbox>
          </Form.Item>
          <Form.Item>
            <Checkbox
              checked={editForm.enableTaskPrioritization}
              onChange={(e) => setEditForm({ ...editForm, enableTaskPrioritization: e.target.checked })}
            >
              Enable Task Prioritization
            </Checkbox>
          </Form.Item>
          <Form.Item>
            <Checkbox
              checked={editForm.enablePerformanceTracking}
              onChange={(e) => setEditForm({ ...editForm, enablePerformanceTracking: e.target.checked })}
            >
              Enable Performance Tracking
            </Checkbox>
          </Form.Item>
        </Form>
      </Modal>
    </>
  );
};

export default TeamCard;
