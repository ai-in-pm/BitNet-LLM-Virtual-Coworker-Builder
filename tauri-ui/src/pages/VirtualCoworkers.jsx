import React, { useState, useEffect } from 'react';
import { Layout, Typography, Button, Space, Modal, Form, Input, Select, message, Spin } from 'antd';
import { PlusOutlined } from '@ant-design/icons';
import { invoke } from '@tauri-apps/api/tauri';
import VirtualCoworkerCard from '../components/VirtualCoworkerCard';

const { Content } = Layout;
const { Title } = Typography;
const { TextArea } = Input;
const { Option } = Select;

const VirtualCoworkers = () => {
  const [virtualCoworkers, setVirtualCoworkers] = useState([]);
  const [models, setModels] = useState([]);
  const [tools, setTools] = useState([]);
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [loading, setLoading] = useState(false);
  const [loadingCoworkers, setLoadingCoworkers] = useState({});
  const [form] = Form.useForm();

  useEffect(() => {
    fetchVirtualCoworkers();
    fetchModels();
    fetchTools();
  }, []);

  const fetchVirtualCoworkers = async () => {
    setLoading(true);
    try {
      const response = await invoke('get_virtual_coworkers');
      setVirtualCoworkers(response.virtual_coworkers || []);
    } catch (error) {
      console.error('Error fetching virtual co-workers:', error);
      message.error('Failed to fetch virtual co-workers');
    } finally {
      setLoading(false);
    }
  };

  const fetchModels = async () => {
    try {
      const response = await invoke('get_models');
      setModels(response.models || []);
    } catch (error) {
      console.error('Error fetching models:', error);
      message.error('Failed to fetch models');
    }
  };

  const fetchTools = async () => {
    try {
      const response = await invoke('get_tools');
      setTools(response.tools || []);
    } catch (error) {
      console.error('Error fetching tools:', error);
      message.error('Failed to fetch tools');
    }
  };

  const handleCreateVirtualCoworker = async () => {
    try {
      await form.validateFields();
      const values = form.getFieldsValue();
      
      setLoading(true);
      await invoke('create_virtual_coworker', {
        name: values.name,
        modelName: values.model,
        description: values.description,
        systemPrompt: values.systemPrompt,
        tools: values.tools || [],
      });
      
      message.success(`Virtual co-worker ${values.name} created successfully`);
      setIsModalVisible(false);
      form.resetFields();
      fetchVirtualCoworkers();
    } catch (error) {
      console.error('Error creating virtual co-worker:', error);
      message.error('Failed to create virtual co-worker');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteVirtualCoworker = async (name) => {
    try {
      setLoadingCoworkers({ ...loadingCoworkers, [name]: true });
      await invoke('delete_virtual_coworker', { name });
      message.success(`Virtual co-worker ${name} deleted successfully`);
      fetchVirtualCoworkers();
    } catch (error) {
      console.error('Error deleting virtual co-worker:', error);
      message.error('Failed to delete virtual co-worker');
    } finally {
      setLoadingCoworkers({ ...loadingCoworkers, [name]: false });
    }
  };

  const handleRunVirtualCoworker = async (name, task) => {
    try {
      setLoadingCoworkers({ ...loadingCoworkers, [name]: true });
      const response = await invoke('run_virtual_coworker', { name, task });
      message.success(`Task submitted with ID: ${response.task_id}`);
      return response;
    } catch (error) {
      console.error('Error running virtual co-worker:', error);
      message.error('Failed to run virtual co-worker');
      throw error;
    } finally {
      setLoadingCoworkers({ ...loadingCoworkers, [name]: false });
    }
  };

  const handleEditVirtualCoworker = async (name, editForm) => {
    try {
      setLoadingCoworkers({ ...loadingCoworkers, [name]: true });
      await invoke('update_virtual_coworker', {
        name,
        newName: editForm.name,
        description: editForm.description,
        modelName: editForm.model,
        systemPrompt: editForm.systemPrompt,
      });
      message.success(`Virtual co-worker ${name} updated successfully`);
      fetchVirtualCoworkers();
    } catch (error) {
      console.error('Error updating virtual co-worker:', error);
      message.error('Failed to update virtual co-worker');
      throw error;
    } finally {
      setLoadingCoworkers({ ...loadingCoworkers, [name]: false });
    }
  };

  return (
    <Content style={{ padding: '24px' }}>
      <Space direction="vertical" size="large" style={{ width: '100%' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Title level={2}>Virtual Co-workers</Title>
          <Button
            type="primary"
            icon={<PlusOutlined />}
            onClick={() => setIsModalVisible(true)}
            disabled={loading}
          >
            Create Virtual Co-worker
          </Button>
        </div>

        {loading ? (
          <div style={{ textAlign: 'center', padding: '50px' }}>
            <Spin size="large" />
          </div>
        ) : (
          <>
            {virtualCoworkers.length === 0 ? (
              <div style={{ textAlign: 'center', padding: '50px' }}>
                <p>No virtual co-workers found. Create one to get started!</p>
              </div>
            ) : (
              virtualCoworkers.map((coworker) => (
                <VirtualCoworkerCard
                  key={coworker.name}
                  virtualCoworker={coworker}
                  onDelete={handleDeleteVirtualCoworker}
                  onRun={handleRunVirtualCoworker}
                  onEdit={handleEditVirtualCoworker}
                  loading={loadingCoworkers[coworker.name]}
                />
              ))
            )}
          </>
        )}
      </Space>

      <Modal
        title="Create Virtual Co-worker"
        open={isModalVisible}
        onOk={handleCreateVirtualCoworker}
        onCancel={() => setIsModalVisible(false)}
        confirmLoading={loading}
      >
        <Form form={form} layout="vertical">
          <Form.Item
            name="name"
            label="Name"
            rules={[{ required: true, message: 'Please enter a name' }]}
          >
            <Input placeholder="Enter virtual co-worker name" />
          </Form.Item>
          <Form.Item
            name="description"
            label="Description"
            rules={[{ required: true, message: 'Please enter a description' }]}
          >
            <Input placeholder="Enter virtual co-worker description" />
          </Form.Item>
          <Form.Item
            name="model"
            label="Model"
            rules={[{ required: true, message: 'Please select a model' }]}
          >
            <Select placeholder="Select a model">
              {models.map((model) => (
                <Option key={model.name} value={model.name}>
                  {model.name}
                </Option>
              ))}
            </Select>
          </Form.Item>
          <Form.Item name="systemPrompt" label="System Prompt">
            <TextArea rows={4} placeholder="Enter system prompt (optional)" />
          </Form.Item>
          <Form.Item name="tools" label="Tools">
            <Select mode="multiple" placeholder="Select tools (optional)">
              {tools.map((tool) => (
                <Option key={tool.name} value={tool.name}>
                  {tool.name}
                </Option>
              ))}
            </Select>
          </Form.Item>
        </Form>
      </Modal>
    </Content>
  );
};

export default VirtualCoworkers;
