import React, { useState } from 'react';
import { Card, Typography, Button, Space, Tag, Modal, Form, Input, InputNumber, Select, message, Spin } from 'antd';
import { EditOutlined, DeleteOutlined, InfoCircleOutlined } from '@ant-design/icons';

const { Title, Text, Paragraph } = Typography;
const { Option } = Select;

const ModelCard = ({ 
  model, 
  onDelete, 
  onEdit,
  loading 
}) => {
  const [isInfoModalVisible, setIsInfoModalVisible] = useState(false);
  const [isEditModalVisible, setIsEditModalVisible] = useState(false);
  const [editForm] = Form.useForm();

  const handleEdit = async () => {
    try {
      await editForm.validateFields();
      const values = editForm.getFieldsValue();
      
      await onEdit(model.name, {
        name: values.name,
        model_path: values.model_path,
        kernel_type: values.kernel_type,
        num_threads: values.num_threads,
        context_size: values.context_size,
        temperature: values.temperature,
        top_p: values.top_p,
        top_k: values.top_k,
        repetition_penalty: values.repetition_penalty
      });
      
      setIsEditModalVisible(false);
    } catch (error) {
      console.error('Error editing model:', error);
    }
  };

  const handleDelete = async () => {
    Modal.confirm({
      title: `Delete ${model.name}?`,
      content: 'This action cannot be undone.',
      okText: 'Delete',
      okType: 'danger',
      cancelText: 'Cancel',
      onOk: () => onDelete(model.name)
    });
  };

  const openInfoModal = () => {
    setIsInfoModalVisible(true);
  };

  const openEditModal = () => {
    editForm.setFieldsValue({
      name: model.name,
      model_path: model.model_path,
      kernel_type: model.kernel_type,
      num_threads: model.num_threads,
      context_size: model.context_size,
      temperature: model.temperature,
      top_p: model.top_p,
      top_k: model.top_k,
      repetition_penalty: model.repetition_penalty
    });
    setIsEditModalVisible(true);
  };

  const getKernelTypeTag = (kernelType) => {
    switch (kernelType) {
      case 'i2_s':
        return <Tag color="green">Small (i2_s)</Tag>;
      case 'i2_m':
        return <Tag color="blue">Medium (i2_m)</Tag>;
      case 'i2_l':
        return <Tag color="purple">Large (i2_l)</Tag>;
      default:
        return <Tag>{kernelType}</Tag>;
    }
  };

  return (
    <Card
      style={{ marginBottom: '16px' }}
      title={
        <Space>
          <Title level={4}>{model.name}</Title>
          {loading && <Spin size="small" />}
        </Space>
      }
      extra={
        <Space>
          <Button
            icon={<InfoCircleOutlined />}
            onClick={openInfoModal}
          >
            Info
          </Button>
          <Button
            icon={<EditOutlined />}
            onClick={openEditModal}
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
    >
      <div style={{ marginBottom: '16px' }}>
        <Text strong>Path:</Text> <Text>{model.model_path}</Text>
      </div>
      
      <div style={{ marginBottom: '16px' }}>
        <Space>
          {getKernelTypeTag(model.kernel_type)}
          <Tag color="cyan">Threads: {model.num_threads}</Tag>
          <Tag color="gold">Context: {model.context_size}</Tag>
        </Space>
      </div>
      
      <div>
        <Text type="secondary">Created: {model.created_at}</Text>
      </div>

      {/* Info Modal */}
      <Modal
        title={`${model.name} Details`}
        open={isInfoModalVisible}
        onCancel={() => setIsInfoModalVisible(false)}
        footer={[
          <Button key="close" onClick={() => setIsInfoModalVisible(false)}>
            Close
          </Button>
        ]}
        width={600}
      >
        <div style={{ marginBottom: '16px' }}>
          <Text strong>Model Path:</Text>
          <Paragraph style={{ marginTop: '4px' }}>{model.model_path}</Paragraph>
        </div>
        
        <div style={{ marginBottom: '16px' }}>
          <Text strong>Kernel Type:</Text>
          <div style={{ marginTop: '4px' }}>{getKernelTypeTag(model.kernel_type)}</div>
        </div>
        
        <div style={{ marginBottom: '16px' }}>
          <Text strong>Number of Threads:</Text>
          <Paragraph style={{ marginTop: '4px' }}>{model.num_threads}</Paragraph>
        </div>
        
        <div style={{ marginBottom: '16px' }}>
          <Text strong>Context Size:</Text>
          <Paragraph style={{ marginTop: '4px' }}>{model.context_size}</Paragraph>
        </div>
        
        <div style={{ marginBottom: '16px' }}>
          <Text strong>Generation Parameters:</Text>
          <div style={{ marginTop: '8px' }}>
            <Space direction="vertical">
              <div>
                <Text>Temperature:</Text> <Text>{model.temperature}</Text>
              </div>
              <div>
                <Text>Top P:</Text> <Text>{model.top_p}</Text>
              </div>
              <div>
                <Text>Top K:</Text> <Text>{model.top_k}</Text>
              </div>
              <div>
                <Text>Repetition Penalty:</Text> <Text>{model.repetition_penalty}</Text>
              </div>
            </Space>
          </div>
        </div>
        
        <div>
          <Text strong>Created At:</Text>
          <Paragraph style={{ marginTop: '4px' }}>{model.created_at}</Paragraph>
        </div>
      </Modal>

      {/* Edit Modal */}
      <Modal
        title={`Edit ${model.name}`}
        open={isEditModalVisible}
        onOk={handleEdit}
        onCancel={() => setIsEditModalVisible(false)}
        width={600}
      >
        <Form form={editForm} layout="vertical">
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
            rules={[{ required: true, message: 'Please enter model path' }]}
          >
            <Input placeholder="Enter model path" />
          </Form.Item>
          
          <Form.Item
            name="kernel_type"
            label="Kernel Type"
            rules={[{ required: true, message: 'Please select kernel type' }]}
          >
            <Select placeholder="Select kernel type">
              <Option value="i2_s">Small (i2_s)</Option>
              <Option value="i2_m">Medium (i2_m)</Option>
              <Option value="i2_l">Large (i2_l)</Option>
            </Select>
          </Form.Item>
          
          <Form.Item
            name="num_threads"
            label="Number of Threads"
            rules={[{ required: true, message: 'Please enter number of threads' }]}
          >
            <InputNumber min={1} max={32} style={{ width: '100%' }} />
          </Form.Item>
          
          <Form.Item
            name="context_size"
            label="Context Size"
            rules={[{ required: true, message: 'Please enter context size' }]}
          >
            <InputNumber min={512} max={8192} step={512} style={{ width: '100%' }} />
          </Form.Item>
          
          <Form.Item
            name="temperature"
            label="Temperature"
            rules={[{ required: true, message: 'Please enter temperature' }]}
          >
            <InputNumber min={0.1} max={2.0} step={0.1} style={{ width: '100%' }} />
          </Form.Item>
          
          <Form.Item
            name="top_p"
            label="Top P"
            rules={[{ required: true, message: 'Please enter top p' }]}
          >
            <InputNumber min={0.1} max={1.0} step={0.05} style={{ width: '100%' }} />
          </Form.Item>
          
          <Form.Item
            name="top_k"
            label="Top K"
            rules={[{ required: true, message: 'Please enter top k' }]}
          >
            <InputNumber min={1} max={100} style={{ width: '100%' }} />
          </Form.Item>
          
          <Form.Item
            name="repetition_penalty"
            label="Repetition Penalty"
            rules={[{ required: true, message: 'Please enter repetition penalty' }]}
          >
            <InputNumber min={1.0} max={2.0} step={0.05} style={{ width: '100%' }} />
          </Form.Item>
        </Form>
      </Modal>
    </Card>
  );
};

export default ModelCard;
