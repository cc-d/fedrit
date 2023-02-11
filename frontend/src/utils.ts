import axios from 'axios';
import { BASE_URL } from './config';

const authAxios = axios.create({
  headers: {
    'Authorization': `Token ${localStorage.getItem('token')}`
  }
});

authAxios.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Token ${token}`;
    }
    return config;
  },
  error => Promise.reject(error)
);

export default authAxios;