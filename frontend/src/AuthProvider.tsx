import React, { createContext, useState, useEffect } from 'react';
import axios from 'axios';
import API_URL from './config';

export const AuthContext = createContext({});

const AuthProvider = (props: any) => {
  const [user, setUser] = useState(null);
  const [isLoading, setLoading] = useState(true);
  const [token, setToken] = useState(null)

  useEffect(() => {
    const fetchUser = async(token: string) => {
      const response = await axios.post(`${API_URL}/tokenuser`, {
        'token': token,
      }).then((response) => {
        setUser(response.data);
      }).catch((err) => {
        console.error(err);
      }).finally(() => {
        setLoading(false);
      });
    };

    let storedToken = localStorage.getItem('token');
    if (storedToken) {
      fetchUser(storedToken);
    }
  }, []);

  return (
    <AuthContext.Provider value={{ user, isLoading }}>
      {props.children}
    </AuthContext.Provider>
  );
};

export default AuthProvider;
