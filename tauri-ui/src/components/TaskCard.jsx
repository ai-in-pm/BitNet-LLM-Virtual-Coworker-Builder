import React, { useState } from 'react';
import { Card, Typography, Button, Space, Tag, Modal, Spin } from 'antd';
import { EyeOutlined, DeleteOutlined, SyncOutlined } from '@ant-design/icons';

const { Title, Text, Paragraph } = Typography;

const TaskCard = ({ 
  task, 
  onDelete, 
  onRefresh,
  loading 
}) => {
  const [isViewModalVisible, setIsViewModalVisible] = useState(false);

  const handleDelete = async () => {
    Modal.confirm({
      title: `Delete Task ${task.id}?`,
      content: 'This action cannot be undone.',
      okText: 'Delete',
      okType: 'danger',
      cancelText: 'Cancel',
      onOk: () => onDelete(task.id)
    });
  };

  const openViewModal = () => {
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

  return (
    <Card
      style={{ marginBottom: '16px' }}
      title={
        <Space>
          <Title level={4}>Task {task.id}</Title>
          {loading && <Spin size="small" />}
        </Space>
      }
      extra={
        <Space>
          <Button
            icon={<EyeOutlined />}
            onClick={openViewModal}
          >
            View
          </Button>
          <Button
            icon={<SyncOutlined />}
            onClick={() => onRefresh(task.id)}
            loading={loading}
          >
            Refresh
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
      <Paragraph ellipsis={{ rows: 2 }}>{task.description}</Paragraph>
      
      <div style={{ marginBottom: '16px' }}>
        <Space>
          {getStatusTag(task.status)}
          {getAssignedToTag(task.assigned_to, task.assigned_type)}
        </Space>
      </div>
      
      <div>
        <Text type="secondary">Created: {task.created_at}</Text>
        {task.completed_at && (
          <div>
            <Text type="secondary">Completed: {task.completed_at}</Text>
          </div>
        )}
      </div>

      {/* View Modal */}
      <Modal
        title={`Task ${task.id} Details`}
        open={isViewModalVisible}
        onCancel={() => setIsViewModalVisible(false)}
        footer={[
          <Button key="close" onClick={() => setIsViewModalVisible(false)}>
            Close
          </Button>
        ]}
        width={700}
      >
        <div style={{ marginBottom: '16px' }}>
          <Text strong>Description:</Text>
          <Paragraph style={{ marginTop: '8px' }}>{task.description}</Paragraph>
        </div>
        
        <div style={{ marginBottom: '16px' }}>
          <Text strong>Status:</Text> {getStatusTag(task.status)}
        </div>
        
        <div style={{ marginBottom: '16px' }}>
          <Text strong>Assigned To:</Text> {getAssignedToTag(task.assigned_to, task.assigned_type)}
          <Text> ({task.assigned_type === 'virtual_coworker' ? 'Virtual Co-worker' : 'Team'})</Text>
        </div>
        
        <div style={{ marginBottom: '16px' }}>
          <Text strong>Created At:</Text> {task.created_at}
        </div>
        
        {task.completed_at && (
          <div style={{ marginBottom: '16px' }}>
            <Text strong>Completed At:</Text> {task.completed_at}
          </div>
        )}
        
        {task.result && (
          <div>
            <Text strong>Result:</Text>
            <Card style={{ marginTop: '8px', background: '#f5f5f5' }}>
              <pre style={{ whiteSpace: 'pre-wrap', wordBreak: 'break-word' }}>
                {task.result}
              </pre>
            </Card>
          </div>
        )}
      </Modal>
    </Card>
  );
};

export default TaskCard;
