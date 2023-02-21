import axios from 'axios';
import { BASE_URL } from './config';

const getAxConfig = (): object => {
  /* gets headers config for axios */
  let utoken: string | null = localStorage.getItem('token');
  let retobj: any = {};
  if (utoken) {
    retobj['Authorization'] = `Token ${utoken}`;
  }
  return retobj;
}

const authAxios = axios.create({
  headers: getAxConfig()
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