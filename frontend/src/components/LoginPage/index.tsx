import React, { useState } from 'react';
import axios from 'axios';
import API_URL from '../../config';
import { PlatformUser } from '../../types';

interface LoginRegister {
  username: string;
  password: string;
}

const LoginPage: React.FC = () => {
  const [logUser, setLogUser] = useState<LoginRegister>({
    username: '', password: '' 
  });
  const [regUser, setRegUser] = useState<LoginRegister>({
    username: '', password: ''
  });
  const [user, setUser] = useState<PlatformUser>();
  const [error, setError] = useState<string>('');

  const handleSubmit = async (
    event: React.FormEvent<HTMLFormElement>,
    action: string
    ) => {
    event.preventDefault();
    try {
      let response;
      let formUser = action == 'login' ? logUser : regUser;
      let fullUsername = action != 'register' ? 
                      formUser.username + '@fedrit' : formUser.username


      response = await axios.post(`${API_URL}auth/${action}`, {
        username: fullUsername,
        password: formUser.password
      })
      .then(response => {
        localStorage.setItem('access_token', response.data.token)
      })
      .catch(err => {
        setError(`failed ${action}`)
      })
    } catch (err) {
      setError(`failed ${action}`);
    }
  };

  return (
    <div>
      <div>
        <form onSubmit={e => handleSubmit(e, 'login')}>
          <input
            type="text"
            placeholder="Username"
            value={logUser.username}
            onChange={e => setLogUser({ ...logUser, username: e.target.value })}
          />
          <input
            type="password"
            placeholder="Password"
            value={logUser.password}
            onChange={e => setLogUser({ ...logUser, password: e.target.value })}
          />
          <button type="submit">Login</button>
        </form>
        {error && <p>{error}</p>}
      </div>
      <div>
        <form onSubmit={e => handleSubmit(e, 'register')}>
          <input
            type="text"
            placeholder="Username"
            value={regUser.username}
            onChange={e => setRegUser({ ...regUser, username: e.target.value })}
          />
          <input
            type="password"
            placeholder="Password"
            value={regUser.password}
            onChange={e => setRegUser({ ...regUser, password: e.target.value })}
          />
          <button type="submit">Register</button>
        </form>
        {error && <p>{error}</p>}
      </div>
    </div>
  );

};

export default LoginPage;