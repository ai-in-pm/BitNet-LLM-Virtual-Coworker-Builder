import React, { useState, useEffect } from 'react';
import { Card, Typography, Button, Space, Tag, Modal, Form, Input, Select, Spin, Divider, Steps, Collapse, Timeline } from 'antd';
import { PlayCircleOutlined, PauseCircleOutlined, ReloadOutlined, CheckCircleOutlined, CloseCircleOutlined, TeamOutlined, UserOutlined, MessageOutlined } from '@ant-design/icons';
import { invoke } from '@tauri-apps/api/tauri';

const { Title, Text, Paragraph } = Typography;
const { TextArea } = Input;
const { Option } = Select;
const { Panel } = Collapse;
const { Step } = Steps;

const TeamWorkflow = ({ team, virtualCoworkers, onRunTeam }) => {
  const [currentTask, setCurrentTask] = useState(null);
  const [workflowStatus, setWorkflowStatus] = useState('idle'); // idle, running, paused, completed, failed
  const [currentStep, setCurrentStep] = useState(0);
  const [workflowSteps, setWorkflowSteps] = useState([]);
  const [workflowMessages, setWorkflowMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [form] = Form.useForm();

  // Reset workflow when team changes
  useEffect(() => {
    resetWorkflow();
  }, [team]);

  const resetWorkflow = () => {
    setCurrentTask(null);
    setWorkflowStatus('idle');
    setCurrentStep(0);
    setWorkflowSteps([]);
    setWorkflowMessages([]);
    form.resetFields();
  };

  const handleStartWorkflow = async () => {
    try {
      await form.validateFields();
      const values = form.getFieldsValue();
      
      setLoading(true);
      setCurrentTask(values.task);
      setWorkflowStatus('running');
      
      // Generate workflow steps based on collaboration mode
      const steps = generateWorkflowSteps(team, values.task);
      setWorkflowSteps(steps);
      
      // Add initial message
      addWorkflowMessage('system', `Starting workflow for task: ${values.task}`);
      
      // Start the workflow
      await executeWorkflow(steps, values.task, values.coordinator);
    } catch (error) {
      console.error('Error starting workflow:', error);
      setWorkflowStatus('failed');
      addWorkflowMessage('system', `Error: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handlePauseWorkflow = () => {
    setWorkflowStatus('paused');
    addWorkflowMessage('system', 'Workflow paused');
  };

  const handleResumeWorkflow = async () => {
    setWorkflowStatus('running');
    addWorkflowMessage('system', 'Workflow resumed');
    
    // Resume from current step
    await executeWorkflow(
      workflowSteps.slice(currentStep), 
      currentTask, 
      form.getFieldValue('coordinator')
    );
  };

  const handleRestartWorkflow = () => {
    setCurrentStep(0);
    setWorkflowStatus('idle');
    setWorkflowMessages([]);
    addWorkflowMessage('system', 'Workflow restarted');
  };

  const generateWorkflowSteps = (team, task) => {
    const { collaborationMode, virtualCoworkers } = team;
    
    if (collaborationMode === 'SEQUENTIAL') {
      // In sequential mode, each virtual co-worker works in sequence
      return virtualCoworkers.map(vcName => {
        const vc = virtualCoworkers.find(vc => vc === vcName) || { name: vcName };
        return {
          title: vc.name,
          description: `${vc.name} processes the task`,
          status: 'waiting'
        };
      });
    } else if (collaborationMode === 'HIERARCHICAL') {
      // In hierarchical mode, coordinator delegates tasks to others
      const coordinator = form.getFieldValue('coordinator') || virtualCoworkers[0];
      
      return [
        {
          title: 'Planning',
          description: `${coordinator} creates a plan`,
          status: 'waiting'
        },
        {
          title: 'Delegation',
          description: 'Tasks are assigned to virtual co-workers',
          status: 'waiting'
        },
        {
          title: 'Execution',
          description: 'Virtual co-workers execute their tasks',
          status: 'waiting'
        },
        {
          title: 'Integration',
          description: `${coordinator} integrates results`,
          status: 'waiting'
        }
      ];
    } else if (collaborationMode === 'PARALLEL') {
      // In parallel mode, all virtual co-workers work simultaneously
      return [
        {
          title: 'Task Distribution',
          description: 'Task is distributed to all virtual co-workers',
          status: 'waiting'
        },
        {
          title: 'Parallel Execution',
          description: 'All virtual co-workers work simultaneously',
          status: 'waiting'
        },
        {
          title: 'Result Collection',
          description: 'Results are collected from all virtual co-workers',
          status: 'waiting'
        },
        {
          title: 'Conflict Resolution',
          description: 'Any conflicts in results are resolved',
          status: 'waiting'
        }
      ];
    }
    
    // Default steps
    return [
      {
        title: 'Start',
        description: 'Begin task execution',
        status: 'waiting'
      },
      {
        title: 'Processing',
        description: 'Process the task',
        status: 'waiting'
      },
      {
        title: 'Completion',
        description: 'Complete the task',
        status: 'waiting'
      }
    ];
  };

  const executeWorkflow = async (steps, task, coordinator) => {
    if (workflowStatus !== 'running') return;
    
    for (let i = 0; i < steps.length; i++) {
      if (workflowStatus !== 'running') return;
      
      const stepIndex = currentStep + i;
      setCurrentStep(stepIndex);
      
      // Update step status
      const updatedSteps = [...workflowSteps];
      updatedSteps[stepIndex] = {
        ...updatedSteps[stepIndex],
        status: 'in-progress'
      };
      setWorkflowSteps(updatedSteps);
      
      // Add message for step start
      addWorkflowMessage('system', `Starting step: ${steps[i].title}`);
      
      try {
        // Simulate step execution
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        // For demonstration, we'll simulate different virtual co-workers sending messages
        if (team.collaborationMode === 'SEQUENTIAL') {
          const vcName = team.virtualCoworkers[stepIndex];
          addWorkflowMessage(vcName, `Working on task: ${task}`);
          await new Promise(resolve => setTimeout(resolve, 1500));
          addWorkflowMessage(vcName, `Completed my part of the task.`);
        } else if (team.collaborationMode === 'HIERARCHICAL') {
          if (stepIndex === 0) {
            // Planning step
            addWorkflowMessage(coordinator, `Creating a plan for task: ${task}`);
            await new Promise(resolve => setTimeout(resolve, 1500));
            addWorkflowMessage(coordinator, `I've created a plan with ${team.virtualCoworkers.length} subtasks.`);
          } else if (stepIndex === 1) {
            // Delegation step
            addWorkflowMessage(coordinator, `Delegating tasks to team members.`);
            for (const vcName of team.virtualCoworkers) {
              if (vcName !== coordinator) {
                await new Promise(resolve => setTimeout(resolve, 800));
                addWorkflowMessage(coordinator, `@${vcName} Please work on subtask: ${getRandomSubtask(task)}`);
              }
            }
          } else if (stepIndex === 2) {
            // Execution step
            for (const vcName of team.virtualCoworkers) {
              if (vcName !== coordinator) {
                await new Promise(resolve => setTimeout(resolve, 1000));
                addWorkflowMessage(vcName, `Working on my assigned subtask.`);
                await new Promise(resolve => setTimeout(resolve, 1200));
                addWorkflowMessage(vcName, `I've completed my subtask.`);
              }
            }
          } else if (stepIndex === 3) {
            // Integration step
            addWorkflowMessage(coordinator, `Integrating results from all team members.`);
            await new Promise(resolve => setTimeout(resolve, 1500));
            addWorkflowMessage(coordinator, `I've integrated all results into a final solution.`);
          }
        } else if (team.collaborationMode === 'PARALLEL') {
          if (stepIndex === 0) {
            // Task distribution
            addWorkflowMessage('system', `Distributing task to all virtual co-workers.`);
          } else if (stepIndex === 1) {
            // Parallel execution
            const promises = team.virtualCoworkers.map(async (vcName) => {
              await new Promise(resolve => setTimeout(resolve, Math.random() * 1000));
              addWorkflowMessage(vcName, `Working on task: ${task}`);
              await new Promise(resolve => setTimeout(resolve, Math.random() * 1500 + 500));
              addWorkflowMessage(vcName, `I've completed my analysis.`);
            });
            await Promise.all(promises);
          } else if (stepIndex === 2) {
            // Result collection
            addWorkflowMessage('system', `Collecting results from all virtual co-workers.`);
          } else if (stepIndex === 3) {
            // Conflict resolution
            if (Math.random() > 0.7) {
              // Simulate a conflict
              addWorkflowMessage('system', `Detected conflicting results between virtual co-workers.`);
              const vc1 = team.virtualCoworkers[0];
              const vc2 = team.virtualCoworkers[1];
              addWorkflowMessage(vc1, `I believe the answer is X because of reason A.`);
              addWorkflowMessage(vc2, `I disagree, the answer should be Y because of reason B.`);
              await new Promise(resolve => setTimeout(resolve, 1500));
              addWorkflowMessage('system', `Resolving conflict using voting mechanism.`);
              await new Promise(resolve => setTimeout(resolve, 1000));
              addWorkflowMessage('system', `Conflict resolved in favor of answer X.`);
            } else {
              addWorkflowMessage('system', `No conflicts detected in the results.`);
            }
          }
        }
        
        // Update step status to completed
        updatedSteps[stepIndex] = {
          ...updatedSteps[stepIndex],
          status: 'finished'
        };
        setWorkflowSteps(updatedSteps);
        
        // Add message for step completion
        addWorkflowMessage('system', `Completed step: ${steps[i].title}`);
      } catch (error) {
        console.error(`Error executing step ${stepIndex}:`, error);
        
        // Update step status to error
        const updatedSteps = [...workflowSteps];
        updatedSteps[stepIndex] = {
          ...updatedSteps[stepIndex],
          status: 'error'
        };
        setWorkflowSteps(updatedSteps);
        
        // Add error message
        addWorkflowMessage('system', `Error in step ${steps[i].title}: ${error.message}`);
        
        setWorkflowStatus('failed');
        return;
      }
    }
    
    // All steps completed successfully
    setWorkflowStatus('completed');
    addWorkflowMessage('system', `Workflow completed successfully`);
    
    // Call the onRunTeam callback with the final result
    const result = `Task "${task}" completed successfully by team "${team.name}" using ${team.collaborationMode} collaboration mode.`;
    onRunTeam(team.name, task, coordinator, result);
  };

  const addWorkflowMessage = (sender, message) => {
    const newMessage = {
      id: Date.now(),
      sender,
      message,
      timestamp: new Date().toISOString()
    };
    
    setWorkflowMessages(prevMessages => [...prevMessages, newMessage]);
  };

  const getRandomSubtask = (task) => {
    const subtasks = [
      `Research information about ${task}`,
      `Analyze data related to ${task}`,
      `Generate visualizations for ${task}`,
      `Write a summary of ${task}`,
      `Create a report on ${task}`
    ];
    
    return subtasks[Math.floor(Math.random() * subtasks.length)];
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'idle':
        return <ReloadOutlined />;
      case 'running':
        return <PlayCircleOutlined style={{ color: '#1890ff' }} />;
      case 'paused':
        return <PauseCircleOutlined style={{ color: '#faad14' }} />;
      case 'completed':
        return <CheckCircleOutlined style={{ color: '#52c41a' }} />;
      case 'failed':
        return <CloseCircleOutlined style={{ color: '#f5222d' }} />;
      default:
        return null;
    }
  };

  const getMessageIcon = (sender) => {
    if (sender === 'system') {
      return <TeamOutlined style={{ color: '#1890ff' }} />;
    } else {
      return <UserOutlined style={{ color: '#722ed1' }} />;
    }
  };

  return (
    <Card
      title={
        <Space>
          <Title level={4}>Team Workflow</Title>
          {getStatusIcon(workflowStatus)}
          <Tag color={
            workflowStatus === 'idle' ? 'default' :
            workflowStatus === 'running' ? 'processing' :
            workflowStatus === 'paused' ? 'warning' :
            workflowStatus === 'completed' ? 'success' :
            'error'
          }>
            {workflowStatus.charAt(0).toUpperCase() + workflowStatus.slice(1)}
          </Tag>
        </Space>
      }
      extra={
        <Space>
          {workflowStatus === 'idle' && (
            <Button
              type="primary"
              icon={<PlayCircleOutlined />}
              onClick={handleStartWorkflow}
              loading={loading}
            >
              Start Workflow
            </Button>
          )}
          {workflowStatus === 'running' && (
            <Button
              icon={<PauseCircleOutlined />}
              onClick={handlePauseWorkflow}
            >
              Pause
            </Button>
          )}
          {workflowStatus === 'paused' && (
            <Button
              type="primary"
              icon={<PlayCircleOutlined />}
              onClick={handleResumeWorkflow}
            >
              Resume
            </Button>
          )}
          {(workflowStatus === 'completed' || workflowStatus === 'failed') && (
            <Button
              icon={<ReloadOutlined />}
              onClick={handleRestartWorkflow}
            >
              Restart
            </Button>
          )}
        </Space>
      }
    >
      <Form form={form} layout="vertical">
        <Form.Item
          name="task"
          label="Task"
          rules={[{ required: true, message: 'Please enter a task' }]}
        >
          <TextArea
            rows={3}
            placeholder="Enter the task for the team..."
            disabled={workflowStatus !== 'idle'}
          />
        </Form.Item>
        
        {team.collaborationMode === 'HIERARCHICAL' && (
          <Form.Item
            name="coordinator"
            label="Coordinator"
            rules={[{ required: true, message: 'Please select a coordinator' }]}
            initialValue={team.virtualCoworkers[0]}
          >
            <Select
              placeholder="Select coordinator virtual co-worker"
              disabled={workflowStatus !== 'idle'}
            >
              {team.virtualCoworkers.map(vcName => (
                <Option key={vcName} value={vcName}>{vcName}</Option>
              ))}
            </Select>
          </Form.Item>
        )}
      </Form>
      
      {workflowSteps.length > 0 && (
        <>
          <Divider orientation="left">Workflow Steps</Divider>
          <Steps
            current={currentStep}
            status={
              workflowStatus === 'failed' ? 'error' :
              workflowStatus === 'completed' ? 'finish' :
              'process'
            }
            size="small"
            direction="vertical"
            items={workflowSteps.map(step => ({
              title: step.title,
              description: step.description,
              status: step.status
            }))}
          />
        </>
      )}
      
      {workflowMessages.length > 0 && (
        <>
          <Divider orientation="left">Messages</Divider>
          <div style={{ maxHeight: '300px', overflow: 'auto', border: '1px solid #f0f0f0', borderRadius: '4px', padding: '8px' }}>
            <Timeline mode="left">
              {workflowMessages.map(msg => (
                <Timeline.Item
                  key={msg.id}
                  dot={getMessageIcon(msg.sender)}
                  color={msg.sender === 'system' ? 'blue' : 'purple'}
                >
                  <div style={{ marginBottom: '8px' }}>
                    <Text strong>{msg.sender}</Text>
                    <Text type="secondary" style={{ marginLeft: '8px', fontSize: '12px' }}>
                      {new Date(msg.timestamp).toLocaleTimeString()}
                    </Text>
                  </div>
                  <div>
                    <Text>{msg.message}</Text>
                  </div>
                </Timeline.Item>
              ))}
            </Timeline>
          </div>
        </>
      )}
    </Card>
  );
};

export default TeamWorkflow;
