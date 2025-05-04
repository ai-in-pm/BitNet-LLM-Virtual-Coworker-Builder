import { invoke } from '@tauri-apps/api/tauri';
import { fetch } from '@tauri-apps/api/http';

// Default API URL
let API_URL = 'http://localhost:8000';

// Set API URL
export const setApiUrl = (url) => {
  API_URL = url;
};

// Get API URL
export const getApiUrl = () => {
  return API_URL;
};

// Generic API request function
const apiRequest = async (method, endpoint, data = null) => {
  try {
    const url = `${API_URL}${endpoint}`;
    
    const options = {
      method,
      headers: {
        'Content-Type': 'application/json',
      }
    };
    
    if (data && (method === 'POST' || method === 'PUT' || method === 'PATCH')) {
      options.body = JSON.stringify(data);
    }
    
    const response = await fetch(url, options);
    
    if (response.status >= 400) {
      throw new Error(`API Error: ${response.status} ${response.statusText}`);
    }
    
    return response.data;
  } catch (error) {
    console.error(`API Error (${method} ${endpoint}):`, error);
    throw error;
  }
};

// Models API
export const modelsApi = {
  getAll: () => apiRequest('GET', '/models'),
  get: (name) => apiRequest('GET', `/models/${name}`),
  create: (model) => apiRequest('POST', '/models', model),
  delete: (name) => apiRequest('DELETE', `/models/${name}`)
};

// Virtual Co-workers API
export const virtualCoworkersApi = {
  getAll: () => apiRequest('GET', '/virtual-coworkers'),
  get: (name) => apiRequest('GET', `/virtual-coworkers/${name}`),
  create: (virtualCoworker) => apiRequest('POST', '/virtual-coworkers', virtualCoworker),
  delete: (name) => apiRequest('DELETE', `/virtual-coworkers/${name}`),
  run: (name, task) => apiRequest('POST', `/virtual-coworkers/${name}/run`, { task })
};

// Teams API
export const teamsApi = {
  getAll: () => apiRequest('GET', '/teams'),
  get: (name) => apiRequest('GET', `/teams/${name}`),
  create: (team) => apiRequest('POST', '/teams', team),
  delete: (name) => apiRequest('DELETE', `/teams/${name}`),
  run: (name, task, coordinator_agent_name = null) => apiRequest('POST', `/teams/${name}/run`, { task, coordinator_agent_name })
};

// Tasks API
export const tasksApi = {
  getAll: () => apiRequest('GET', '/tasks'),
  get: (id) => apiRequest('GET', `/tasks/${id}`)
};

// Tools API
export const toolsApi = {
  getAll: () => apiRequest('GET', '/tools'),
  get: (name) => apiRequest('GET', `/tools/${name}`)
};

// Config API
export const configApi = {
  get: () => apiRequest('GET', '/config'),
  update: (config) => apiRequest('POST', '/config', config)
};

// Health API
export const healthApi = {
  check: () => apiRequest('GET', '/health')
};

// API client
const api = {
  models: modelsApi,
  virtualCoworkers: virtualCoworkersApi,
  teams: teamsApi,
  tasks: tasksApi,
  tools: toolsApi,
  config: configApi,
  health: healthApi,
  setApiUrl,
  getApiUrl
};

export default api;
