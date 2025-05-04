import React, { useState } from 'react';
import { Card, Typography, Button, Space, Tag, Modal, Form, Input, Select, message, Spin, Divider } from 'antd';
import { EditOutlined, DeleteOutlined, InfoCircleOutlined, ExperimentOutlined, CodeOutlined } from '@ant-design/icons';
import { invoke } from '@tauri-apps/api/tauri';

const { Title, Text, Paragraph } = Typography;
const { TextArea } = Input;
const { Option } = Select;

const ToolCard = ({
  tool,
  onDelete,
  onEdit,
  loading
}) => {
  const [isInfoModalVisible, setIsInfoModalVisible] = useState(false);
  const [isEditModalVisible, setIsEditModalVisible] = useState(false);
  const [isTestModalVisible, setIsTestModalVisible] = useState(false);
  const [editForm] = Form.useForm();
  const [testForm] = Form.useForm();
  const [testLoading, setTestLoading] = useState(false);
  const [testResult, setTestResult] = useState(null);

  const handleEdit = async () => {
    try {
      await editForm.validateFields();
      const values = editForm.getFieldsValue();

      // Parse args schema
      let argsSchema = {};
      try {
        argsSchema = JSON.parse(values.args_schema);
      } catch (error) {
        message.error('Invalid args schema JSON');
        return;
      }

      await onEdit(tool.name, {
        name: values.name,
        description: values.description,
        category: values.category,
        args_schema: argsSchema
      });

      setIsEditModalVisible(false);
    } catch (error) {
      console.error('Error editing tool:', error);
    }
  };

  const handleDelete = async () => {
    Modal.confirm({
      title: `Delete ${tool.name}?`,
      content: 'This action cannot be undone.',
      okText: 'Delete',
      okType: 'danger',
      cancelText: 'Cancel',
      onOk: () => onDelete(tool.name)
    });
  };

  const openInfoModal = () => {
    setIsInfoModalVisible(true);
  };

  const openEditModal = () => {
    editForm.setFieldsValue({
      name: tool.name,
      description: tool.description,
      category: tool.category,
      args_schema: JSON.stringify(tool.args_schema, null, 2)
    });
    setIsEditModalVisible(true);
  };

  const openTestModal = () => {
    // Generate example args based on schema
    const exampleArgs = {};
    Object.entries(tool.args_schema || {}).forEach(([key, schema]) => {
      if (schema.type === 'string') {
        exampleArgs[key] = schema.example || 'example string';
      } else if (schema.type === 'number') {
        exampleArgs[key] = schema.example || 42;
      } else if (schema.type === 'boolean') {
        exampleArgs[key] = schema.example || true;
      } else if (schema.type === 'array') {
        exampleArgs[key] = schema.example || [];
      } else if (schema.type === 'object') {
        exampleArgs[key] = schema.example || {};
      }
    });

    testForm.setFieldsValue({
      args: JSON.stringify(exampleArgs, null, 2)
    });
    setTestResult(null);
    setIsTestModalVisible(true);
  };

  const handleTest = async () => {
    try {
      setTestLoading(true);
      setTestResult(null);

      await testForm.validateFields();
      const values = testForm.getFieldsValue();

      // Parse args
      let args = {};
      try {
        args = JSON.parse(values.args);
      } catch (error) {
        message.error('Invalid args JSON');
        setTestLoading(false);
        return;
      }

      // Call the API to test the tool
      const result = await invoke('test_tool', {
        name: tool.name,
        args: args
      }).catch(error => {
        console.error('Error testing tool:', error);
        return { error: error.toString() };
      });

      if (result.error) {
        setTestResult({
          success: false,
          error: result.error
        });
      } else {
        setTestResult({
          success: true,
          data: result
        });
      }
    } catch (error) {
      console.error('Error testing tool:', error);
      setTestResult({
        success: false,
        error: error.toString()
      });
    } finally {
      setTestLoading(false);
    }
  };

  const getCategoryTag = (category) => {
    const categoryColors = {
      information: 'blue',
      analysis: 'green',
      visualization: 'purple',
      text: 'cyan',
      code: 'magenta',
      utility: 'orange'
    };

    return <Tag color={categoryColors[category] || 'default'}>{category}</Tag>;
  };

  return (
    <Card
      style={{ marginBottom: '16px' }}
      title={
        <Space>
          <Title level={4}>{tool.name}</Title>
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
            type="primary"
            icon={<ExperimentOutlined />}
            onClick={openTestModal}
            disabled={loading}
          >
            Test
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
      <Paragraph ellipsis={{ rows: 2 }}>{tool.description}</Paragraph>

      <div style={{ marginBottom: '16px' }}>
        <Space>
          {getCategoryTag(tool.category)}
          <Tag color="blue">Args: {Object.keys(tool.args_schema).length}</Tag>
        </Space>
      </div>

      <div>
        <Text type="secondary">Created: {tool.created_at}</Text>
      </div>

      {/* Info Modal */}
      <Modal
        title={`${tool.name} Details`}
        open={isInfoModalVisible}
        onCancel={() => setIsInfoModalVisible(false)}
        footer={[
          <Button key="close" onClick={() => setIsInfoModalVisible(false)}>
            Close
          </Button>
        ]}
        width={700}
      >
        <div style={{ marginBottom: '16px' }}>
          <Text strong>Description:</Text>
          <Paragraph style={{ marginTop: '8px' }}>{tool.description}</Paragraph>
        </div>

        <div style={{ marginBottom: '16px' }}>
          <Text strong>Category:</Text> {getCategoryTag(tool.category)}
        </div>

        <div style={{ marginBottom: '16px' }}>
          <Text strong>Created At:</Text> {tool.created_at}
        </div>

        <div>
          <Text strong>Arguments Schema:</Text>
          <Card style={{ marginTop: '8px', background: '#f5f5f5' }}>
            <pre>{JSON.stringify(tool.args_schema, null, 2)}</pre>
          </Card>
        </div>
      </Modal>

      {/* Test Modal */}
      <Modal
        title={`Test ${tool.name}`}
        open={isTestModalVisible}
        onOk={handleTest}
        onCancel={() => setIsTestModalVisible(false)}
        confirmLoading={testLoading}
        width={700}
      >
        <Form form={testForm} layout="vertical">
          <Form.Item
            name="args"
            label="Arguments (JSON)"
            rules={[
              { required: true, message: 'Please enter arguments' },
              {
                validator: (_, value) => {
                  try {
                    JSON.parse(value);
                    return Promise.resolve();
                  } catch (error) {
                    return Promise.reject('Invalid JSON format');
                  }
                }
              }
            ]}
          >
            <TextArea
              rows={6}
              placeholder="Enter arguments as JSON..."
              style={{ fontFamily: 'monospace' }}
            />
          </Form.Item>

          {testResult && (
            <>
              <Divider orientation="left" plain>Result</Divider>
              {testResult.success ? (
                <div>
                  <Tag color="green">Success</Tag>
                  <div style={{ marginTop: '10px' }}>
                    <pre style={{
                      backgroundColor: '#f5f5f5',
                      padding: 10,
                      borderRadius: 4,
                      maxHeight: 300,
                      overflow: 'auto'
                    }}>
                      {typeof testResult.data === 'object'
                        ? JSON.stringify(testResult.data, null, 2)
                        : testResult.data}
                    </pre>
                  </div>
                </div>
              ) : (
                <div>
                  <Tag color="red">Error</Tag>
                  <div style={{ marginTop: '10px' }}>
                    <pre style={{
                      backgroundColor: '#fff2f0',
                      padding: 10,
                      borderRadius: 4,
                      maxHeight: 300,
                      overflow: 'auto'
                    }}>
                      {testResult.error}
                    </pre>
                  </div>
                </div>
              )}
            </>
          )}
        </Form>
      </Modal>

      {/* Edit Modal */}
      <Modal
        title={`Edit ${tool.name}`}
        open={isEditModalVisible}
        onOk={handleEdit}
        onCancel={() => setIsEditModalVisible(false)}
        width={700}
      >
        <Form form={editForm} layout="vertical">
          <Form.Item
            name="name"
            label="Name"
            rules={[
              { required: true, message: 'Please enter a name' },
              { pattern: /^[a-z0-9_]+$/, message: 'Name can only contain lowercase letters, numbers, and underscores' }
            ]}
          >
            <Input placeholder="Enter tool name" />
          </Form.Item>

          <Form.Item
            name="description"
            label="Description"
            rules={[{ required: true, message: 'Please enter a description' }]}
          >
            <Input placeholder="Enter tool description" />
          </Form.Item>

          <Form.Item
            name="category"
            label="Category"
            rules={[{ required: true, message: 'Please select a category' }]}
          >
            <Select placeholder="Select category">
              <Option value="information">Information</Option>
              <Option value="analysis">Analysis</Option>
              <Option value="visualization">Visualization</Option>
              <Option value="text">Text</Option>
              <Option value="code">Code</Option>
              <Option value="utility">Utility</Option>
            </Select>
          </Form.Item>

          <Form.Item
            name="args_schema"
            label="Arguments Schema (JSON)"
            rules={[
              { required: true, message: 'Please enter arguments schema' },
              {
                validator: (_, value) => {
                  try {
                    JSON.parse(value);
                    return Promise.resolve();
                  } catch (error) {
                    return Promise.reject('Invalid JSON format');
                  }
                }
              }
            ]}
          >
            <TextArea
              rows={10}
              placeholder="Enter arguments schema in JSON format"
              style={{ fontFamily: 'monospace' }}
            />
          </Form.Item>
        </Form>
      </Modal>
    </Card>
  );
};

export default ToolCard;
