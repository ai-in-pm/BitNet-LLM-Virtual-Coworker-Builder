import React from 'react';
import { Button, Typography, Space, Tooltip } from 'antd';
import { PlayCircleOutlined, PauseCircleOutlined } from '@ant-design/icons';

const { Text } = Typography;

const ApiStatus = ({ running, port, onStart, onStop }) => {
  return (
    <div className="api-status">
      <div className={`status-indicator ${running ? 'online' : 'offline'}`} />
      <Space>
        <Text>API Server: {running ? 'Online' : 'Offline'}</Text>
        {running && <Text>Port: {port}</Text>}
        {running ? (
          <Tooltip title="Stop API Server">
            <Button
              type="primary"
              danger
              icon={<PauseCircleOutlined />}
              onClick={onStop}
              size="small"
            />
          </Tooltip>
        ) : (
          <Tooltip title="Start API Server">
            <Button
              type="primary"
              icon={<PlayCircleOutlined />}
              onClick={onStart}
              size="small"
            />
          </Tooltip>
        )}
      </Space>
    </div>
  );
};

export default ApiStatus;
