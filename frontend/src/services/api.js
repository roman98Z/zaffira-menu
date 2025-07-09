import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor for logging
apiClient.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// Add response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => {
    console.log(`API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error('API Response Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// Menu API functions
export const menuApi = {
  // Get all menu items
  getMenuItems: async (category = null) => {
    try {
      const params = category ? { category } : {};
      const response = await apiClient.get('/menu', { params });
      return response.data;
    } catch (error) {
      console.error('Error fetching menu items:', error);
      throw error;
    }
  },

  // Get menu organized by categories
  getMenuByCategories: async () => {
    try {
      const response = await apiClient.get('/menu/categories');
      return response.data;
    } catch (error) {
      console.error('Error fetching menu categories:', error);
      throw error;
    }
  },

  // Get single menu item
  getMenuItem: async (itemId) => {
    try {
      const response = await apiClient.get(`/menu/${itemId}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching menu item:', error);
      throw error;
    }
  },

  // Create new menu item
  createMenuItem: async (itemData) => {
    try {
      const response = await apiClient.post('/menu', itemData);
      return response.data;
    } catch (error) {
      console.error('Error creating menu item:', error);
      throw error;
    }
  },

  // Update menu item
  updateMenuItem: async (itemId, updateData) => {
    try {
      const response = await apiClient.put(`/menu/${itemId}`, updateData);
      return response.data;
    } catch (error) {
      console.error('Error updating menu item:', error);
      throw error;
    }
  },

  // Delete menu item
  deleteMenuItem: async (itemId) => {
    try {
      const response = await apiClient.delete(`/menu/${itemId}`);
      return response.data;
    } catch (error) {
      console.error('Error deleting menu item:', error);
      throw error;
    }
  },

  // Initialize menu with sample data
  initializeMenu: async () => {
    try {
      const response = await apiClient.post('/menu/init');
      return response.data;
    } catch (error) {
      console.error('Error initializing menu:', error);
      throw error;
    }
  }
};

export default apiClient;