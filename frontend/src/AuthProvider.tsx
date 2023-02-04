import React, { createContext, useState, useEffect } from 'react';
import axios from 'axios';
import API_URL from './config';

export const AuthContext = createContext({});

const AuthProvider = (props: any) => {
  const [user, setUser] = useState(null);
  const [isLoading, setLoading] = useState(true);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const response = await axios.get('/user');
        setUser(response.data);
        setLoading(false);
      } catch (err) {
        setLoading(false);
      }
    };
    fetchUser();
  }, []);

  const login = async (username: string, password: string) => {
    try {
      const response = await axios.post(`${API_URL}auth/login`, {
        username,
        password,
      });
      setUser(response.data);
    } catch (err) {
      console.error(err);
    }
  };

  const logout = () => {
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, isLoading }}>
      {props.children}
    </AuthContext.Provider>
  );
};

export default AuthProvider;
