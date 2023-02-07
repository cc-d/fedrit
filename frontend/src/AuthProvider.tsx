import React, { createContext, useState, useEffect } from 'react';
import axios from 'axios';
import API_URL from './config';
import { PlatformUser } from './types';

export const AuthContext = createContext({});

export interface AuthContextProps {
  user: PlatformUser | null,
  isLoading: boolean;
}

const AuthProvider = (props: any) => {
  const [user, setUser] = useState<PlatformUser | null>(null);
  const [isLoading, setLoading] = useState<boolean>(false);

  const logout = () => {
    setUser(null);
    localStorage.removeItem('token');
    window.location.reload();
  };

  useEffect(() => {
    const fetchUser = async(token: string) => {
      setLoading(true);
      const response = await axios.post(`${API_URL}/tokenuser`, {
        'token': token,
      }).then((response) => {
        console.log('useeffect');
        setUser(response.data);
      }).catch((err) => {
        console.error(err);
      }).finally(() => {
        setLoading(false);
        console.log('FINALLY');
      });
    };

    let storedToken = localStorage.getItem('token');
    if (storedToken && user === null && !isLoading) { 
      fetchUser(storedToken);
    }
  }, [user]);

  return (
    <AuthContext.Provider value={{ setUser, isLoading }}>
      {props.children}
    </AuthContext.Provider>
  );
};

export default AuthProvider;

