import React, { useState, useEffect } from 'react';
import { Typography, Button, Form, Input, Select, InputNumber, Switch, Tabs, Card, message, Spin, Divider } from 'antd';
import { SaveOutlined, ReloadOutlined, FolderOpenOutlined } from '@ant-design/icons';
import { invoke } from '@tauri-apps/api/tauri';
import { open } from '@tauri-apps/api/dialog';

const { Title, Text, Paragraph } = Typography;
const { Option } = Select;
const { TabPane } = Tabs;

const Settings = () => {
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [generalForm] = Form.useForm();
  const [modelForm] = Form.useForm();
  const [memoryForm] = Form.useForm();
  const [teamForm] = Form.useForm();
  const [loggingForm] = Form.useForm();
  const [uiForm] = Form.useForm();

  useEffect(() => {
    fetchSettings();
  }, []);

  const fetchSettings = async () => {
    setLoading(true);
    try {
      // In a real implementation, we would fetch data from the API
      // For now, we'll use mock data
      
      // Simulate API call delay
      await new Promise(resolve => setTimeout(resolve, 500));
      
      // General settings
      generalForm.setFieldsValue({
        host: '0.0.0.0',
        port: 8000,
        debug: false,
        workers: 4
      });
      
      // Model settings
      modelForm.setFieldsValue({
        path: null,
        models_dir: 'models',
        kernel_type: 'i2_s',
        num_threads: 4,
        context_size: 2048,
        temperature: 0.7,
        top_p: 0.9,
        top_k: 40,
        repetition_penalty: 1.1
      });
      
      // Memory settings
      memoryForm.setFieldsValue({
        max_items: 100,
        max_context_length: 2000,
        recency_bias: 0.7
      });
      
      // Team settings
      teamForm.setFieldsValue({
        default_collaboration_mode: 'SEQUENTIAL',
        max_parallel_tasks: 4,
        enable_conflict_resolution: true,
        enable_task_prioritization: true,
        enable_performance_tracking: true
      });
      
      // Logging settings
      loggingForm.setFieldsValue({
        level: 'INFO',
        format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        file: 'logs/bitnet_vc_builder.log',
        max_size: 10485760,
        backup_count: 5
      });
      
      // UI settings
      uiForm.setFieldsValue({
        theme: 'light',
        max_history_items: 50,
        auto_refresh: true,
        refresh_interval: 5
      });
    } catch (error) {
      console.error('Error fetching settings:', error);
      message.error('Failed to fetch settings');
    } finally {
      setLoading(false);
    }
  };

  const saveSettings = async (form, section) => {
    try {
      await form.validateFields();
      const values = form.getFieldsValue();
      
      setSaving(true);
      
      // In a real implementation, we would call the API
      // For now, we'll just show a success message
      
      // Simulate API call delay
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      message.success(`${section} settings saved successfully`);
    } catch (error) {
      console.error(`Error saving ${section} settings:`, error);
      message.error(`Failed to save ${section} settings`);
    } finally {
      setSaving(false);
    }
  };

  const handleBrowseModelPath = async () => {
    try {
      const selected = await open({
        directory: true,
        multiple: false,
        title: 'Select Model Directory'
      });
      
      if (selected) {
        modelForm.setFieldsValue({ path: selected });
      }
    } catch (error) {
      console.error('Error browsing for model path:', error);
    }
  };

  const handleBrowseModelsDir = async () => {
    try {
      const selected = await open({
        directory: true,
        multiple: false,
        title: 'Select Models Directory'
      });
      
      if (selected) {
        modelForm.setFieldsValue({ models_dir: selected });
      }
    } catch (error) {
      console.error('Error browsing for models directory:', error);
    }
  };

  const handleBrowseLogFile = async () => {
    try {
      const selected = await open({
        filters: [{ name: 'Log Files', extensions: ['log'] }],
        multiple: false,
        title: 'Select Log File'
      });
      
      if (selected) {
        loggingForm.setFieldsValue({ file: selected });
      }
    } catch (error) {
      console.error('Error browsing for log file:', error);
    }
  };

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
        <Title level={2}>Settings</Title>
        <Button
          icon={<ReloadOutlined />}
          onClick={fetchSettings}
          loading={loading}
        >
          Reload Settings
        </Button>
      </div>

      {loading ? (
        <div style={{ textAlign: 'center', padding: '50px' }}>
          <Spin size="large" />
        </div>
      ) : (
        <Tabs defaultActiveKey="general">
          <TabPane tab="General" key="general">
            <Card>
              <Form
                form={generalForm}
                layout="vertical"
                className="settings-form"
              >
                <Form.Item
                  name="host"
                  label="Server Host"
                  rules={[{ required: true, message: 'Please enter server host' }]}
                >
                  <Input placeholder="Enter server host" />
                </Form.Item>
                
                <Form.Item
                  name="port"
                  label="Server Port"
                  rules={[{ required: true, message: 'Please enter server port' }]}
                >
                  <InputNumber min={1024} max={65535} style={{ width: '100%' }} />
                </Form.Item>
                
                <Form.Item
                  name="debug"
                  label="Debug Mode"
                  valuePropName="checked"
                >
                  <Switch />
                </Form.Item>
                
                <Form.Item
                  name="workers"
                  label="Number of Workers"
                  rules={[{ required: true, message: 'Please enter number of workers' }]}
                >
                  <InputNumber min={1} max={32} style={{ width: '100%' }} />
                </Form.Item>
                
                <div className="settings-actions">
                  <Button
                    type="primary"
                    icon={<SaveOutlined />}
                    onClick={() => saveSettings(generalForm, 'General')}
                    loading={saving}
                  >
                    Save
                  </Button>
                </div>
              </Form>
            </Card>
          </TabPane>
          
          <TabPane tab="Model" key="model">
            <Card>
              <Form
                form={modelForm}
                layout="vertical"
                className="settings-form"
              >
                <Form.Item
                  name="path"
                  label="BitNet Path"
                >
                  <Input
                    placeholder="Path to BitNet installation (leave empty for auto-detect)"
                    addonAfter={
                      <Button size="small" onClick={handleBrowseModelPath}>
                        <FolderOpenOutlined />
                      </Button>
                    }
                  />
                </Form.Item>
                
                <Form.Item
                  name="models_dir"
                  label="Models Directory"
                  rules={[{ required: true, message: 'Please enter models directory' }]}
                >
                  <Input
                    placeholder="Directory to store BitNet models"
                    addonAfter={
                      <Button size="small" onClick={handleBrowseModelsDir}>
                        <FolderOpenOutlined />
                      </Button>
                    }
                  />
                </Form.Item>
                
                <Divider>Default Model Settings</Divider>
                
                <Form.Item
                  name="kernel_type"
                  label="Kernel Type"
                  rules={[{ required: true, message: 'Please select kernel type' }]}
                >
                  <Select placeholder="Select kernel type">
                    <Option value="i2_s">i2_s (Small)</Option>
                    <Option value="i2_m">i2_m (Medium)</Option>
                    <Option value="i2_l">i2_l (Large)</Option>
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
                
                <div className="settings-actions">
                  <Button
                    type="primary"
                    icon={<SaveOutlined />}
                    onClick={() => saveSettings(modelForm, 'Model')}
                    loading={saving}
                  >
                    Save
                  </Button>
                </div>
              </Form>
            </Card>
          </TabPane>
          
          <TabPane tab="Memory" key="memory">
            <Card>
              <Form
                form={memoryForm}
                layout="vertical"
                className="settings-form"
              >
                <Form.Item
                  name="max_items"
                  label="Maximum Items"
                  rules={[{ required: true, message: 'Please enter maximum items' }]}
                >
                  <InputNumber min={10} max={1000} style={{ width: '100%' }} />
                </Form.Item>
                
                <Form.Item
                  name="max_context_length"
                  label="Maximum Context Length"
                  rules={[{ required: true, message: 'Please enter maximum context length' }]}
                >
                  <InputNumber min={500} max={10000} step={100} style={{ width: '100%' }} />
                </Form.Item>
                
                <Form.Item
                  name="recency_bias"
                  label="Recency Bias"
                  rules={[{ required: true, message: 'Please enter recency bias' }]}
                >
                  <InputNumber min={0.0} max={1.0} step={0.1} style={{ width: '100%' }} />
                </Form.Item>
                
                <div className="settings-actions">
                  <Button
                    type="primary"
                    icon={<SaveOutlined />}
                    onClick={() => saveSettings(memoryForm, 'Memory')}
                    loading={saving}
                  >
                    Save
                  </Button>
                </div>
              </Form>
            </Card>
          </TabPane>
          
          <TabPane tab="Team" key="team">
            <Card>
              <Form
                form={teamForm}
                layout="vertical"
                className="settings-form"
              >
                <Form.Item
                  name="default_collaboration_mode"
                  label="Default Collaboration Mode"
                  rules={[{ required: true, message: 'Please select default collaboration mode' }]}
                >
                  <Select placeholder="Select default collaboration mode">
                    <Option value="SEQUENTIAL">Sequential</Option>
                    <Option value="PARALLEL">Parallel</Option>
                    <Option value="HIERARCHICAL">Hierarchical</Option>
                    <Option value="CONSENSUS">Consensus</Option>
                  </Select>
                </Form.Item>
                
                <Form.Item
                  name="max_parallel_tasks"
                  label="Maximum Parallel Tasks"
                  rules={[{ required: true, message: 'Please enter maximum parallel tasks' }]}
                >
                  <InputNumber min={1} max={32} style={{ width: '100%' }} />
                </Form.Item>
                
                <Form.Item
                  name="enable_conflict_resolution"
                  label="Enable Conflict Resolution"
                  valuePropName="checked"
                >
                  <Switch />
                </Form.Item>
                
                <Form.Item
                  name="enable_task_prioritization"
                  label="Enable Task Prioritization"
                  valuePropName="checked"
                >
                  <Switch />
                </Form.Item>
                
                <Form.Item
                  name="enable_performance_tracking"
                  label="Enable Performance Tracking"
                  valuePropName="checked"
                >
                  <Switch />
                </Form.Item>
                
                <div className="settings-actions">
                  <Button
                    type="primary"
                    icon={<SaveOutlined />}
                    onClick={() => saveSettings(teamForm, 'Team')}
                    loading={saving}
                  >
                    Save
                  </Button>
                </div>
              </Form>
            </Card>
          </TabPane>
          
          <TabPane tab="Logging" key="logging">
            <Card>
              <Form
                form={loggingForm}
                layout="vertical"
                className="settings-form"
              >
                <Form.Item
                  name="level"
                  label="Logging Level"
                  rules={[{ required: true, message: 'Please select logging level' }]}
                >
                  <Select placeholder="Select logging level">
                    <Option value="DEBUG">DEBUG</Option>
                    <Option value="INFO">INFO</Option>
                    <Option value="WARNING">WARNING</Option>
                    <Option value="ERROR">ERROR</Option>
                    <Option value="CRITICAL">CRITICAL</Option>
                  </Select>
                </Form.Item>
                
                <Form.Item
                  name="format"
                  label="Log Format"
                  rules={[{ required: true, message: 'Please enter log format' }]}
                >
                  <Input placeholder="Enter log format" />
                </Form.Item>
                
                <Form.Item
                  name="file"
                  label="Log File"
                  rules={[{ required: true, message: 'Please enter log file' }]}
                >
                  <Input
                    placeholder="Enter log file path"
                    addonAfter={
                      <Button size="small" onClick={handleBrowseLogFile}>
                        <FolderOpenOutlined />
                      </Button>
                    }
                  />
                </Form.Item>
                
                <Form.Item
                  name="max_size"
                  label="Maximum Log Size (bytes)"
                  rules={[{ required: true, message: 'Please enter maximum log size' }]}
                >
                  <InputNumber min={1024} style={{ width: '100%' }} />
                </Form.Item>
                
                <Form.Item
                  name="backup_count"
                  label="Backup Count"
                  rules={[{ required: true, message: 'Please enter backup count' }]}
                >
                  <InputNumber min={0} max={20} style={{ width: '100%' }} />
                </Form.Item>
                
                <div className="settings-actions">
                  <Button
                    type="primary"
                    icon={<SaveOutlined />}
                    onClick={() => saveSettings(loggingForm, 'Logging')}
                    loading={saving}
                  >
                    Save
                  </Button>
                </div>
              </Form>
            </Card>
          </TabPane>
          
          <TabPane tab="UI" key="ui">
            <Card>
              <Form
                form={uiForm}
                layout="vertical"
                className="settings-form"
              >
                <Form.Item
                  name="theme"
                  label="Theme"
                  rules={[{ required: true, message: 'Please select theme' }]}
                >
                  <Select placeholder="Select theme">
                    <Option value="light">Light</Option>
                    <Option value="dark">Dark</Option>
                  </Select>
                </Form.Item>
                
                <Form.Item
                  name="max_history_items"
                  label="Maximum History Items"
                  rules={[{ required: true, message: 'Please enter maximum history items' }]}
                >
                  <InputNumber min={10} max={200} style={{ width: '100%' }} />
                </Form.Item>
                
                <Form.Item
                  name="auto_refresh"
                  label="Auto Refresh"
                  valuePropName="checked"
                >
                  <Switch />
                </Form.Item>
                
                <Form.Item
                  name="refresh_interval"
                  label="Refresh Interval (seconds)"
                  rules={[{ required: true, message: 'Please enter refresh interval' }]}
                >
                  <InputNumber min={1} max={60} style={{ width: '100%' }} />
                </Form.Item>
                
                <div className="settings-actions">
                  <Button
                    type="primary"
                    icon={<SaveOutlined />}
                    onClick={() => saveSettings(uiForm, 'UI')}
                    loading={saving}
                  >
                    Save
                  </Button>
                </div>
              </Form>
            </Card>
          </TabPane>
        </Tabs>
      )}
    </div>
  );
};

export default Settings;
