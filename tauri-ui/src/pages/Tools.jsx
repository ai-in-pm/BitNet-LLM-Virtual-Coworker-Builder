import React, { useState, useEffect } from 'react';
import { Typography, Button, Space, Modal, Form, Input, Select, message, Spin, Row, Col, Tabs } from 'antd';
import { PlusOutlined, AppstoreOutlined, UnorderedListOutlined } from '@ant-design/icons';
import { invoke } from '@tauri-apps/api/tauri';
import ToolCard from '../components/ToolCard';

const { Title, Text, Paragraph } = Typography;
const { TextArea } = Input;
const { Option } = Select;

const Tools = () => {
  const [tools, setTools] = useState([]);
  const [loading, setLoading] = useState(false);
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [viewMode, setViewMode] = useState('grid'); // 'grid' or 'table'
  const [loadingTools, setLoadingTools] = useState({});
  const [form] = Form.useForm();

  useEffect(() => {
    fetchTools();
  }, []);

  const fetchTools = async () => {
    setLoading(true);
    try {
      // In a real implementation, we would fetch data from the API
      // For now, we'll use mock data

      // Simulate API call delay
      await new Promise(resolve => setTimeout(resolve, 500));

      const mockTools = [
        {
          id: 1,
          name: 'web_search',
          description: 'Search the web for information',
          category: 'information',
          args_schema: {
            query: {
              type: 'string',
              description: 'Search query',
              required: true
            }
          },
          created_at: '2023-07-10 10:30:15'
        },
        {
          id: 2,
          name: 'document_reader',
          description: 'Read and extract information from documents',
          category: 'information',
          args_schema: {
            document_path: {
              type: 'string',
              description: 'Path to the document',
              required: true
            },
            page_numbers: {
              type: 'array',
              description: 'Page numbers to read (optional)',
              required: false
            }
          },
          created_at: '2023-07-10 11:45:30'
        },
        {
          id: 3,
          name: 'data_analyzer',
          description: 'Analyze data and generate insights',
          category: 'analysis',
          args_schema: {
            data: {
              type: 'string',
              description: 'Data to analyze',
              required: true
            },
            analysis_type: {
              type: 'string',
              description: 'Type of analysis to perform',
              required: false
            }
          },
          created_at: '2023-07-11 09:15:45'
        },
        {
          id: 4,
          name: 'chart_generator',
          description: 'Generate charts and visualizations from data',
          category: 'visualization',
          args_schema: {
            data: {
              type: 'string',
              description: 'Data to visualize',
              required: true
            },
            chart_type: {
              type: 'string',
              description: 'Type of chart to generate',
              required: true
            },
            title: {
              type: 'string',
              description: 'Chart title',
              required: false
            }
          },
          created_at: '2023-07-11 14:20:10'
        },
        {
          id: 5,
          name: 'grammar_checker',
          description: 'Check and correct grammar in text',
          category: 'text',
          args_schema: {
            text: {
              type: 'string',
              description: 'Text to check',
              required: true
            }
          },
          created_at: '2023-07-12 10:30:25'
        },
        {
          id: 6,
          name: 'text_summarizer',
          description: 'Summarize long texts into concise summaries',
          category: 'text',
          args_schema: {
            text: {
              type: 'string',
              description: 'Text to summarize',
              required: true
            },
            max_length: {
              type: 'number',
              description: 'Maximum length of the summary',
              required: false
            }
          },
          created_at: '2023-07-12 11:45:40'
        },
        {
          id: 7,
          name: 'code_generator',
          description: 'Generate code based on requirements',
          category: 'code',
          args_schema: {
            requirements: {
              type: 'string',
              description: 'Code requirements',
              required: true
            },
            language: {
              type: 'string',
              description: 'Programming language',
              required: true
            }
          },
          created_at: '2023-07-13 09:15:55'
        },
        {
          id: 8,
          name: 'calculator',
          description: 'Perform mathematical calculations',
          category: 'utility',
          args_schema: {
            expression: {
              type: 'string',
              description: 'Mathematical expression',
              required: true
            }
          },
          created_at: '2023-07-14 14:30:10'
        }
      ];

      setTools(mockTools);
    } catch (error) {
      console.error('Error fetching tools:', error);
      message.error('Failed to fetch tools');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTool = async () => {
    try {
      await form.validateFields();
      const values = form.getFieldsValue();

      setLoading(true);

      // Parse args schema
      let argsSchema = {};
      try {
        argsSchema = JSON.parse(values.args_schema);
      } catch (error) {
        message.error('Invalid args schema JSON');
        setLoading(false);
        return;
      }

      // In a real implementation, we would call the API
      // For now, we'll just add the tool to the local state

      // Simulate API call delay
      await new Promise(resolve => setTimeout(resolve, 1000));

      const newTool = {
        id: tools.length + 1,
        name: values.name,
        description: values.description,
        category: values.category,
        args_schema: argsSchema,
        created_at: new Date().toISOString().replace('T', ' ').substring(0, 19)
      };

      setTools([...tools, newTool]);
      message.success(`Tool ${values.name} created successfully`);
      setIsModalVisible(false);
      form.resetFields();
    } catch (error) {
      console.error('Error creating tool:', error);
      message.error('Failed to create tool');
    } finally {
      setLoading(false);
    }
  };

  const handleEditTool = async (toolName, updatedTool) => {
    try {
      setLoadingTools(prev => ({ ...prev, [toolName]: true }));

      // In a real implementation, we would call the API
      // For now, we'll just update the tool in the local state

      // Simulate API call delay
      await new Promise(resolve => setTimeout(resolve, 1000));

      setTools(tools.map(tool => {
        if (tool.name === toolName) {
          return {
            ...tool,
            ...updatedTool
          };
        }
        return tool;
      }));

      message.success(`Tool ${toolName} updated successfully`);
    } catch (error) {
      console.error('Error updating tool:', error);
      message.error('Failed to update tool');
    } finally {
      setLoadingTools(prev => ({ ...prev, [toolName]: false }));
    }
  };

  const handleDeleteTool = async (toolName) => {
    try {
      setLoadingTools(prev => ({ ...prev, [toolName]: true }));

      // In a real implementation, we would call the API
      // For now, we'll just remove the tool from the local state

      // Simulate API call delay
      await new Promise(resolve => setTimeout(resolve, 1000));

      setTools(tools.filter(tool => tool.name !== toolName));
      message.success(`Tool ${toolName} deleted successfully`);
    } catch (error) {
      console.error('Error deleting tool:', error);
      message.error('Failed to delete tool');
    } finally {
      setLoadingTools(prev => ({ ...prev, [toolName]: false }));
    }
  };

  const handleTestTool = async (toolName, args) => {
    try {
      setLoadingTools(prev => ({ ...prev, [toolName]: true }));

      // In a real implementation, we would call the API
      // For now, we'll just simulate a response

      // Simulate API call delay
      await new Promise(resolve => setTimeout(resolve, 1000));

      // Mock response based on tool name
      let result;
      if (toolName === 'web_search') {
        result = `Search results for: ${args.query}`;
      } else if (toolName === 'calculator') {
        try {
          result = eval(args.expression);
        } catch (error) {
          throw new Error(`Error evaluating expression: ${error.message}`);
        }
      } else if (toolName === 'data_analyzer') {
        result = `Analysis of data: ${args.data.substring(0, 50)}...`;
      } else {
        result = `Tool ${toolName} executed with args: ${JSON.stringify(args)}`;
      }

      return result;
    } catch (error) {
      console.error(`Error testing tool ${toolName}:`, error);
      throw error;
    } finally {
      setLoadingTools(prev => ({ ...prev, [toolName]: false }));
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

  const columns = [
    {
      title: 'Name',
      dataIndex: 'name',
      key: 'name',
      sorter: (a, b) => a.name.localeCompare(b.name)
    },
    {
      title: 'Description',
      dataIndex: 'description',
      key: 'description',
      ellipsis: true
    },
    {
      title: 'Category',
      dataIndex: 'category',
      key: 'category',
      render: (category) => getCategoryTag(category),
      filters: [
        { text: 'Information', value: 'information' },
        { text: 'Analysis', value: 'analysis' },
        { text: 'Visualization', value: 'visualization' },
        { text: 'Text', value: 'text' },
        { text: 'Code', value: 'code' },
        { text: 'Utility', value: 'utility' }
      ],
      onFilter: (value, record) => record.category === value
    },
    {
      title: 'Arguments',
      key: 'arguments',
      render: (_, record) => Object.keys(record.args_schema).length
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
            icon={<EditOutlined />}
            onClick={() => handleEditToolClick(record)}
          />
          <Button
            danger
            icon={<DeleteOutlined />}
            onClick={() => handleDeleteTool(record.id)}
          />
        </Space>
      )
    }
  ];

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
        <Title level={2}>Tools</Title>
        <Space>
          <Button
            icon={<AppstoreOutlined />}
            type={viewMode === 'grid' ? 'primary' : 'default'}
            onClick={() => setViewMode('grid')}
          >
            Grid
          </Button>
          <Button
            icon={<UnorderedListOutlined />}
            type={viewMode === 'table' ? 'primary' : 'default'}
            onClick={() => setViewMode('table')}
          >
            Table
          </Button>
          <Button
            type="primary"
            icon={<PlusOutlined />}
            onClick={() => setIsModalVisible(true)}
            disabled={loading}
          >
            Create Tool
          </Button>
        </Space>
      </div>

      {loading ? (
        <div style={{ textAlign: 'center', padding: '50px' }}>
          <Spin size="large" />
        </div>
      ) : (
        <>
          {viewMode === 'grid' ? (
            <Row gutter={[16, 16]}>
              {tools.map(tool => (
                <Col xs={24} sm={12} md={8} lg={8} xl={6} key={tool.id}>
                  <ToolCard
                    tool={tool}
                    onDelete={handleDeleteTool}
                    onEdit={handleEditTool}
                    onTest={handleTestTool}
                    loading={loadingTools[tool.name]}
                  />
                </Col>
              ))}
            </Row>
          ) : (
            <Tabs
              defaultActiveKey="all"
              items={[
                {
                  key: 'all',
                  label: 'All',
                  children: (
                    <Table
                      dataSource={tools}
                      columns={columns}
                      rowKey="id"
                      pagination={{ pageSize: 10 }}
                    />
                  )
                },
                {
                  key: 'information',
                  label: 'Information',
                  children: (
                    <Table
                      dataSource={tools.filter(tool => tool.category === 'information')}
                      columns={columns}
                      rowKey="id"
                      pagination={{ pageSize: 10 }}
                    />
                  )
                },
                {
                  key: 'analysis',
                  label: 'Analysis',
                  children: (
                    <Table
                      dataSource={tools.filter(tool => tool.category === 'analysis')}
                      columns={columns}
                      rowKey="id"
                      pagination={{ pageSize: 10 }}
                    />
                  )
                },
                {
                  key: 'visualization',
                  label: 'Visualization',
                  children: (
                    <Table
                      dataSource={tools.filter(tool => tool.category === 'visualization')}
                      columns={columns}
                      rowKey="id"
                      pagination={{ pageSize: 10 }}
                    />
                  )
                },
                {
                  key: 'text',
                  label: 'Text',
                  children: (
                    <Table
                      dataSource={tools.filter(tool => tool.category === 'text')}
                      columns={columns}
                      rowKey="id"
                      pagination={{ pageSize: 10 }}
                    />
                  )
                },
                {
                  key: 'code',
                  label: 'Code',
                  children: (
                    <Table
                      dataSource={tools.filter(tool => tool.category === 'code')}
                      columns={columns}
                      rowKey="id"
                      pagination={{ pageSize: 10 }}
                    />
                  )
                },
                {
                  key: 'utility',
                  label: 'Utility',
                  children: (
                    <Table
                      dataSource={tools.filter(tool => tool.category === 'utility')}
                      columns={columns}
                      rowKey="id"
                      pagination={{ pageSize: 10 }}
                    />
                  )
                }
              ]}
            />
          )}
        </>
      )}

      <Modal
        title="Create Tool"
        open={isModalVisible}
        onOk={handleCreateTool}
        onCancel={() => setIsModalVisible(false)}
        confirmLoading={loading}
        width={600}
      >
        <Form form={form} layout="vertical">
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
            initialValue={JSON.stringify({
              arg1: {
                type: 'string',
                description: 'Description of arg1',
                required: true
              }
            }, null, 2)}
          >
            <TextArea
              rows={10}
              placeholder="Enter arguments schema in JSON format"
            />
          </Form.Item>
        </Form>
      </Modal>

      <Modal
        title="Edit Tool"
        open={isEditModalVisible}
        onOk={handleEditTool}
        onCancel={() => setIsEditModalVisible(false)}
        confirmLoading={loading}
        width={600}
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
            />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default Tools;
