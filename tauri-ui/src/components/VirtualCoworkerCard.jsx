import React, { useState } from 'react';
import { Card, Button, Typography, Space, Tag, Modal, Input, Form, Select, Spin } from 'antd';
import { EditOutlined, DeleteOutlined, PlayCircleOutlined, ToolOutlined } from '@ant-design/icons';
import { invoke } from '@tauri-apps/api/tauri';

const { Title, Text } = Typography;
const { TextArea } = Input;
const { Option } = Select;

const VirtualCoworkerCard = ({ virtualCoworker, onDelete, onRun, onEdit, loading }) => {
  const [isRunModalVisible, setIsRunModalVisible] = useState(false);
  const [isEditModalVisible, setIsEditModalVisible] = useState(false);
  const [task, setTask] = useState('');
  const [editForm, setEditForm] = useState({
    name: virtualCoworker.name,
    description: virtualCoworker.description,
    model: virtualCoworker.model,
    systemPrompt: virtualCoworker.systemPrompt || '',
  });
  const [runLoading, setRunLoading] = useState(false);
  const [editLoading, setEditLoading] = useState(false);

  const handleRun = async () => {
    setRunLoading(true);
    try {
      await onRun(virtualCoworker.name, task);
      setIsRunModalVisible(false);
      setTask('');
    } catch (error) {
      console.error('Error running virtual co-worker:', error);
    } finally {
      setRunLoading(false);
    }
  };

  const handleEdit = async () => {
    setEditLoading(true);
    try {
      await onEdit(virtualCoworker.name, editForm);
      setIsEditModalVisible(false);
    } catch (error) {
      console.error('Error editing virtual co-worker:', error);
    } finally {
      setEditLoading(false);
    }
  };

  const handleDelete = async () => {
    try {
      await onDelete(virtualCoworker.name);
    } catch (error) {
      console.error('Error deleting virtual co-worker:', error);
    }
  };

  return (
    <>
      <Card
        title={
          <Space>
            <Title level={4}>{virtualCoworker.name}</Title>
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
          <Text>{virtualCoworker.description}</Text>
          <Space>
            <Tag color="blue">Model: {virtualCoworker.model}</Tag>
            <Tag color="green">Tools: {virtualCoworker.tools?.length || 0}</Tag>
          </Space>
        </Space>
      </Card>

      <Modal
        title={`Run ${virtualCoworker.name}`}
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
              placeholder="Enter the task for the virtual co-worker..."
            />
          </Form.Item>
        </Form>
      </Modal>

      <Modal
        title={`Edit ${virtualCoworker.name}`}
        open={isEditModalVisible}
        onOk={handleEdit}
        onCancel={() => setIsEditModalVisible(false)}
        confirmLoading={editLoading}
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
          <Form.Item label="Model">
            <Select
              value={editForm.model}
              onChange={(value) => setEditForm({ ...editForm, model: value })}
              style={{ width: '100%' }}
            >
              <Option value="model1">Model 1</Option>
              <Option value="model2">Model 2</Option>
              <Option value="model3">Model 3</Option>
            </Select>
          </Form.Item>
          <Form.Item label="System Prompt">
            <TextArea
              rows={4}
              value={editForm.systemPrompt}
              onChange={(e) => setEditForm({ ...editForm, systemPrompt: e.target.value })}
              placeholder="Enter system prompt..."
            />
          </Form.Item>
        </Form>
      </Modal>
    </>
  );
};

export default VirtualCoworkerCard;
