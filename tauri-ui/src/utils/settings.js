import { invoke } from '@tauri-apps/api/tauri';
import { Store } from 'tauri-plugin-store-api';

// Create a store
const store = new Store('settings.dat');

// Default settings
const defaultSettings = {
  apiUrl: 'http://localhost:8000',
  theme: 'light',
  autoRefresh: true,
  refreshInterval: 5,
  maxHistoryItems: 50
};

// Get all settings
export const getSettings = async () => {
  try {
    const settings = {};
    
    // Get each setting, or use default if not found
    for (const [key, defaultValue] of Object.entries(defaultSettings)) {
      settings[key] = await store.get(key) ?? defaultValue;
    }
    
    return settings;
  } catch (error) {
    console.error('Error getting settings:', error);
    return { ...defaultSettings };
  }
};

// Get a specific setting
export const getSetting = async (key, defaultValue = null) => {
  try {
    const value = await store.get(key);
    return value ?? (defaultSettings[key] ?? defaultValue);
  } catch (error) {
    console.error(`Error getting setting ${key}:`, error);
    return defaultSettings[key] ?? defaultValue;
  }
};

// Set a specific setting
export const setSetting = async (key, value) => {
  try {
    await store.set(key, value);
    await store.save();
    return true;
  } catch (error) {
    console.error(`Error setting ${key}:`, error);
    return false;
  }
};

// Set multiple settings
export const setSettings = async (settings) => {
  try {
    for (const [key, value] of Object.entries(settings)) {
      await store.set(key, value);
    }
    await store.save();
    return true;
  } catch (error) {
    console.error('Error setting settings:', error);
    return false;
  }
};

// Reset settings to defaults
export const resetSettings = async () => {
  try {
    for (const [key, value] of Object.entries(defaultSettings)) {
      await store.set(key, value);
    }
    await store.save();
    return true;
  } catch (error) {
    console.error('Error resetting settings:', error);
    return false;
  }
};

// Settings utility
const settings = {
  getSettings,
  getSetting,
  setSetting,
  setSettings,
  resetSettings,
  defaultSettings
};

export default settings;
