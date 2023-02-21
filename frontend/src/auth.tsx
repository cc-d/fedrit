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
  const [dark, setDark] = useState<string>(
    localStorage.getItem('dark') ? 'dark' : '')

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
    const rootElem = document.getElementById("root");

    console.log('relem')
    console.log(rootElem);
    if (token && getUser === null) {
      setGetUser(true);
    } else if (token && getUser === true) {
      fetchUser(token).then(() => setGetUser(false))
    }

    if (rootElem) {
      if (dark) {
        document.body.style.backgroundColor = '#111';
        rootElem.classList.add('dark');
      } else {
        document.body.style.backgroundColor = '#ccc';
        rootElem.classList.remove('dark')
      }
    }

  }, [getUser, dark]);

  return (
    <AuthContext.Provider value={{ user, setUser, dark, setDark}}>
      {props.children}
    </AuthContext.Provider>
  );
};

export default AuthProvider;

