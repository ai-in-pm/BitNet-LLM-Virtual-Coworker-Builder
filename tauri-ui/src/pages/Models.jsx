import React, { useState, useEffect } from 'react';
import { Typography, Button, Space, Table, Tag, Modal, Form, Input, Select, InputNumber, message, Spin, Tabs } from 'antd';
import { PlusOutlined, DeleteOutlined, EditOutlined, InfoCircleOutlined, RocketOutlined } from '@ant-design/icons';
import { invoke } from '@tauri-apps/api/tauri';
import { open } from '@tauri-apps/api/dialog';
import ModelOptimizer from '../components/ModelOptimizer';

const { Title, Text } = Typography;
const { Option } = Select;

const Models = () => {
  const [models, setModels] = useState([]);
  const [loading, setLoading] = useState(false);
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [isInfoModalVisible, setIsInfoModalVisible] = useState(false);
  const [selectedModel, setSelectedModel] = useState(null);
  const [activeTab, setActiveTab] = useState('models');
  const [optimizedModels, setOptimizedModels] = useState([]);
  const [form] = Form.useForm();

  useEffect(() => {
    fetchModels();
  }, []);

  const fetchModels = async () => {
    setLoading(true);

    try {
      // In a real implementation, we would fetch data from the API
      // For now, we'll use mock data

      // Simulate API call delay
      await new Promise(resolve => setTimeout(resolve, 1000));

      const mockModels = [
        {
          id: 1,
          name: 'BitNet-B1-58-Large',
          model_path: 'models/bitnet_b1_58_large',
          kernel_type: 'i2_s',
          num_threads: 4,
          context_size: 2048,
          temperature: 0.7,
          top_p: 0.9,
          top_k: 40,
          repetition_penalty: 1.1,
          created_at: '2023-07-10 09:15:22'
        },
        {
          id: 2,
          name: 'BitNet-B1-32-Medium',
          model_path: 'models/bitnet_b1_32_medium',
          kernel_type: 'i2_m',
          num_threads: 2,
          context_size: 1024,
          temperature: 0.8,
          top_p: 0.95,
          top_k: 50,
          repetition_penalty: 1.05,
          created_at: '2023-07-12 14:30:45'
        },
        {
          id: 3,
          name: 'BitNet-B1-16-Small',
          model_path: 'models/bitnet_b1_16_small',
          kernel_type: 'i2_s',
          num_threads: 1,
          context_size: 512,
          temperature: 0.9,
          top_p: 1.0,
          top_k: 60,
          repetition_penalty: 1.0,
          created_at: '2023-07-14 11:20:15'
        }
      ];

      setModels(mockModels);
    } catch (error) {
      console.error('Error fetching models:', error);
      message.error('Failed to fetch models');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateModel = async () => {
    try {
      await form.validateFields();
      const values = form.getFieldsValue();

      setLoading(true);

      // In a real implementation, we would call the API
      // For now, we'll just add the model to the local state

      // Simulate API call delay
      await new Promise(resolve => setTimeout(resolve, 1000));

      const newModel = {
        id: models.length + 1,
        name: values.name,
        model_path: values.model_path,
        kernel_type: values.kernel_type,
        num_threads: values.num_threads,
        context_size: values.context_size,
        temperature: values.temperature,
        top_p: values.top_p,
        top_k: values.top_k,
        repetition_penalty: values.repetition_penalty,
        created_at: new Date().toISOString().replace('T', ' ').substring(0, 19)
      };

      setModels([...models, newModel]);
      message.success(`Model ${values.name} created successfully`);
      setIsModalVisible(false);
      form.resetFields();
    } catch (error) {
      console.error('Error creating model:', error);
      message.error('Failed to create model');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteModel = async (model) => {
    try {
      setLoading(true);

      // In a real implementation, we would call the API
      // For now, we'll just remove the model from the local state

      // Simulate API call delay
      await new Promise(resolve => setTimeout(resolve, 1000));

      setModels(models.filter(m => m.id !== model.id));
      message.success(`Model ${model.name} deleted successfully`);
    } catch (error) {
      console.error('Error deleting model:', error);
      message.error('Failed to delete model');
    } finally {
      setLoading(false);
    }
  };

  const handleViewModelInfo = (model) => {
    setSelectedModel(model);
    setIsInfoModalVisible(true);
  };

  const handleOptimizeModel = (model) => {
    setSelectedModel(model);
    setActiveTab('optimize');
  };

  const handleModelOptimized = (result) => {
    // Add the optimized model to the list
    const optimizedModel = {
      ...selectedModel,
      id: `opt-${selectedModel.id}`,
      name: `${selectedModel.name}-optimized`,
      model_path: result.optimizedModelPath,
      is_optimized: true,
      original_model_id: selectedModel.id,
      optimization_settings: result.settings,
      size_mb: result.optimizedSize,
      speedup: result.speedup,
      memory_reduction: result.memoryReduction,
      created_at: new Date().toISOString().replace('T', ' ').substring(0, 19)
    };

    setOptimizedModels([...optimizedModels, optimizedModel]);
    message.success(`Model ${selectedModel.name} optimized successfully`);
  };

  const handleBrowseModelPath = async () => {
    try {
      const selected = await open({
        directory: true,
        multiple: false,
        title: 'Select Model Directory'
      });

      if (selected) {
        form.setFieldsValue({ model_path: selected });
      }
    } catch (error) {
      console.error('Error browsing for model path:', error);
    }
  };

  const columns = [
    {
      title: 'Name',
      dataIndex: 'name',
      key: 'name',
      sorter: (a, b) => a.name.localeCompare(b.name)
    },
    {
      title: 'Kernel Type',
      dataIndex: 'kernel_type',
      key: 'kernel_type',
      render: (kernel_type) => {
        let color = 'blue';
        if (kernel_type === 'i2_m') color = 'green';
        if (kernel_type === 'i2_l') color = 'purple';

        return (
          <Tag color={color}>
            {kernel_type.toUpperCase()}
          </Tag>
        );
      }
    },
    {
      title: 'Context Size',
      dataIndex: 'context_size',
      key: 'context_size',
      sorter: (a, b) => a.context_size - b.context_size
    },
    {
      title: 'Threads',
      dataIndex: 'num_threads',
      key: 'num_threads'
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
            icon={<InfoCircleOutlined />}
            onClick={() => handleViewModelInfo(record)}
          />
          <Button
            type="primary"
            icon={<RocketOutlined />}
            onClick={() => handleOptimizeModel(record)}
          />
          <Button
            danger
            icon={<DeleteOutlined />}
            onClick={() => handleDeleteModel(record)}
          />
        </Space>
      )
    }
  ];

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
        <Title level={2}>Models</Title>
        <Space>
          {selectedModel && (
            <>
              <Button
                type={activeTab === 'models' ? 'primary' : 'default'}
                onClick={() => setActiveTab('models')}
              >
                Models
              </Button>
              <Button
                type={activeTab === 'optimize' ? 'primary' : 'default'}
                icon={<RocketOutlined />}
                onClick={() => setActiveTab('optimize')}
              >
                Optimize
              </Button>
            </>
          )}
          <Button
            type="primary"
            icon={<PlusOutlined />}
            onClick={() => setIsModalVisible(true)}
          >
            Create Model
          </Button>
        </Space>
      </div>

      {activeTab === 'models' ? (
        <Table
          dataSource={[...models, ...optimizedModels]}
          columns={columns}
          rowKey="id"
          loading={loading}
        />
      ) : (
        selectedModel && (
          <ModelOptimizer
            model={{
              ...selectedModel,
              size_mb: selectedModel.size_mb || Math.floor(Math.random() * 1000) + 500 // Mock size if not available
            }}
            onOptimize={handleModelOptimized}
          />
        )
      )}

      <Modal
        title="Create Model"
        open={isModalVisible}
        onOk={handleCreateModel}
        onCancel={() => setIsModalVisible(false)}
        confirmLoading={loading}
        width={600}
      >
        <Form form={form} layout="vertical">
          <Form.Item
            name="name"
            label="Name"
            rules={[{ required: true, message: 'Please enter a name' }]}
          >
            <Input placeholder="Enter model name" />
          </Form.Item>

          <Form.Item
            name="model_path"
            label="Model Path"
            rules={[{ required: true, message: 'Please enter a model path' }]}
          >
            <Input
              placeholder="Enter model path"
              addonAfter={
                <Button size="small" onClick={handleBrowseModelPath}>
                  Browse
                </Button>
              }
            />
          </Form.Item>

          <Form.Item
            name="kernel_type"
            label="Kernel Type"
            rules={[{ required: true, message: 'Please select a kernel type' }]}
            initialValue="i2_s"
          >
            <Select>
              <Option value="i2_s">i2_s (Small)</Option>
              <Option value="i2_m">i2_m (Medium)</Option>
              <Option value="i2_l">i2_l (Large)</Option>
            </Select>
          </Form.Item>

          <Form.Item
            name="num_threads"
            label="Number of Threads"
            rules={[{ required: true, message: 'Please enter number of threads' }]}
            initialValue={4}
          >
            <InputNumber min={1} max={32} style={{ width: '100%' }} />
          </Form.Item>

          <Form.Item
            name="context_size"
            label="Context Size"
            rules={[{ required: true, message: 'Please enter context size' }]}
            initialValue={2048}
          >
            <InputNumber min={512} max={8192} step={512} style={{ width: '100%' }} />
          </Form.Item>

          <Form.Item
            name="temperature"
            label="Temperature"
            rules={[{ required: true, message: 'Please enter temperature' }]}
            initialValue={0.7}
          >
            <InputNumber min={0.1} max={2.0} step={0.1} style={{ width: '100%' }} />
          </Form.Item>

          <Form.Item
            name="top_p"
            label="Top P"
            rules={[{ required: true, message: 'Please enter top p' }]}
            initialValue={0.9}
          >
            <InputNumber min={0.1} max={1.0} step={0.05} style={{ width: '100%' }} />
          </Form.Item>

          <Form.Item
            name="top_k"
            label="Top K"
            rules={[{ required: true, message: 'Please enter top k' }]}
            initialValue={40}
          >
            <InputNumber min={1} max={100} style={{ width: '100%' }} />
          </Form.Item>

          <Form.Item
            name="repetition_penalty"
            label="Repetition Penalty"
            rules={[{ required: true, message: 'Please enter repetition penalty' }]}
            initialValue={1.1}
          >
            <InputNumber min={1.0} max={2.0} step={0.05} style={{ width: '100%' }} />
          </Form.Item>
        </Form>
      </Modal>

      <Modal
        title="Model Information"
        open={isInfoModalVisible}
        onCancel={() => setIsInfoModalVisible(false)}
        footer={[
          <Button key="close" onClick={() => setIsInfoModalVisible(false)}>
            Close
          </Button>
        ]}
        width={600}
      >
        {selectedModel && (
          <div>
            <p><strong>Name:</strong> {selectedModel.name}</p>
            <p><strong>Model Path:</strong> {selectedModel.model_path}</p>
            <p><strong>Kernel Type:</strong> {selectedModel.kernel_type}</p>
            <p><strong>Number of Threads:</strong> {selectedModel.num_threads}</p>
            <p><strong>Context Size:</strong> {selectedModel.context_size}</p>
            <p><strong>Temperature:</strong> {selectedModel.temperature}</p>
            <p><strong>Top P:</strong> {selectedModel.top_p}</p>
            <p><strong>Top K:</strong> {selectedModel.top_k}</p>
            <p><strong>Repetition Penalty:</strong> {selectedModel.repetition_penalty}</p>
            <p><strong>Created At:</strong> {selectedModel.created_at}</p>
          </div>
        )}
      </Modal>
    </div>
  );
};

export default Models;
