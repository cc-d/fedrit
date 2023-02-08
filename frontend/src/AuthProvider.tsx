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
  const [getUser, setGetUser] = useState<boolean | null>(null);
  const token = localStorage.getItem('token');

  const fetchUser =  async(token: string) => {
    const response =  await axios.post(`${API_URL}/tokenuser`, {
      'token': token,
    }).then((response) => {
      setUser(response.data);
    }).catch((err) => {
      console.error(err);
    }).finally(() => {
    });
  };

  useEffect(() => {
    if (token && getUser === null) {
      setGetUser(true);
    } else if (token && getUser === true) {
      fetchUser(token).then(() => setGetUser(false))
    }
  }, [getUser]);

  return (
    <AuthContext.Provider value={{ user, setUser,  }}>
      {props.children}
    </AuthContext.Provider>
  );
};

export default AuthProvider;

