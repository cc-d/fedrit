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
  const [getUser, setGetUser] = useState<boolean | null>(null);
  //const [token, setToken] = useState<string | null | boolean>(false);
  const token = localStorage.getItem('token');


  const fetchUser =  async(token: string) => {
    const response =  await axios.post(`${API_URL}/tokenuser`, {
      'token': token,
    }).then((response) => {
      console.log('then fetchuser');
      setUser(response.data);
    }).catch((err) => {
      console.error(err);
    }).finally(() => {
      console.log('finalyl fetchuser');
    });
  };

  console.log('outside useffect');

  useEffect(() => {
    console.log(`inside useffect setloading ${isLoading} ${token} ${user}`);
    if (token && getUser === null) {
      setGetUser(true);
    } else if (token && getUser === true) {
      setGetUser(false);
      setLoading(true)
      console.log('storedtoken and user calling fetchuser');
      fetchUser(token).then(() => setLoading(false));
    }
  }, [getUser]);

  console.log('before return');
  
  return (
    <AuthContext.Provider value={{ user, setUser, isLoading }}>
      {props.children}
    </AuthContext.Provider>
  );
};

export default AuthProvider;

