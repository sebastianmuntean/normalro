import axios from 'axios';
import API_BASE_URL from '../config/api';

export const login = (username, password) =>
  axios.post(`${API_BASE_URL}/auth/login`, { username, password });

export const register = (username, email, password) =>
  axios.post(`${API_BASE_URL}/auth/register`, { username, email, password });

export const getProfile = (token) =>
  axios.get(`${API_BASE_URL}/auth/me`, {
    headers: { Authorization: `Bearer ${token}` }
  });

export const getPages = () =>
  axios.get(`${API_BASE_URL}/pages`);

export const updateProfile = (token, data) =>
  axios.put(`${API_BASE_URL}/auth/me`, data, {
    headers: { Authorization: `Bearer ${token}` }
  }); 