import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://backend:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      if (window.location.pathname !== '/auth') {
        window.location.href = '/auth';
      }
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  login: async (username, password) => {
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);
    
    const response = await api.post('/auth/token', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    });
    return response.data;
  },
};

export const usersAPI = {
  register: async (email, login, password) => {
    const response = await api.post('/users', { email, login, password });
    return response.data;
  },
  
  getMe: async () => {
    const response = await api.get('/users/me');
    return response.data;
  },
  
  updateMe: async (data) => {
    const response = await api.put('/users/me', data);
    return response.data;
  },
  
  getUser: async (userId) => {
    const response = await api.get(`/users/${userId}`);
    return response.data;
  },
  
  getUserPosts: async (userId) => {
    const response = await api.get(`/users/${userId}/posts`);
    return response.data;
  },
};

export const postsAPI = {
  getAll: async () => {
    const response = await api.get('/posts');
    return response.data;
  },
  
  getMy: async () => {
    const response = await api.get('/posts/my');
    return response.data;
  },
  
  getOne: async (postId) => {
    const response = await api.get(`/posts/${postId}`);
    return response.data;
  },
  
  create: async (title, content) => {
    const response = await api.post('/posts', { title, content });
    return response.data;
  },
  
  update: async (postId, title, content) => {
    const response = await api.put(`/posts/${postId}`, { title, content });
    return response.data;
  },
  
  delete: async (postId) => {
    const response = await api.delete(`/posts/${postId}`);
    return response.data;
  },
  
  rate: async (postId, value) => {
    const response = await api.post(`/posts/${postId}/rate`, { value });
    return response.data;
  },
};

export const commentsAPI = {
  getAll: async (postId) => {
    const response = await api.get(`/posts/${postId}/comments`);
    return response.data;
  },
  
  create: async (postId, content) => {
    const response = await api.post(`/posts/${postId}/comments`, { content });
    return response.data;
  },
  
  delete: async (postId, commentId) => {
    const response = await api.delete(`/posts/${postId}/comments/${commentId}`);
    return response.data;
  },
};

export const favoritesAPI = {
  getAll: async () => {
    const response = await api.get('/favorites');
    return response.data;
  },
  
  add: async (postId) => {
    const response = await api.post(`/favorites/${postId}`);
    return response.data;
  },
  
  remove: async (postId) => {
    const response = await api.delete(`/favorites/${postId}`);
    return response.data;
  },
};

export const searchAPI = {
  posts: async (query) => {
    const response = await api.get('/search/posts', { params: { q: query } });
    return response.data;
  },
  
  users: async (query) => {
    const response = await api.get('/search/users', { params: { q: query } });
    return response.data;
  },
};

export const uploadsAPI = {
  avatar: async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await api.post('/uploads/avatar', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },
  
  image: async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await api.post('/uploads/image', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },
};

export default api;
