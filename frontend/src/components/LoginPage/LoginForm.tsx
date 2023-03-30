import React, { useState } from 'react';
import Axios from 'axios';
import { API_URL } from '../../config';
import '../../styles/styles.css';

interface LoginFormInputs {
  username: string;
  password: string;
}

const LoginForm: React.FC = () => {
  const [error, setError] = useState<string | null>(null);
  const [logUser, setLogUser] = useState<LoginFormInputs>({
    'username': '', 'password': '',
  });

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    const resp = await Axios.post(`${API_URL}/auth/login`, {
      username: logUser.username + '@fedrit',
      password: logUser.password,
    }).then(resp => {
      localStorage.setItem('token', resp.data.token);
      window.location.href = '/';
    }).catch(err => {
      setError('Failed to log in')
    });
  }

  return (
    <div className='form-wrapper'>
      <h2>Login</h2>
      <form id='form-login' onSubmit={handleSubmit}>
        <input
          id='input-login-username'
          type='text'
          placeholder='Username'
          value={logUser.username}
          onChange={e => setLogUser({ ...logUser, username: e.target.value })}
        />
        <input
          id='input-login-password'
          type='password'
          placeholder='Password'
          value={logUser.password}
          onChange={e => setLogUser({ ...logUser, password: e.target.value })}
        />
        <button type='submit'>Login</button>
      </form>
      {error && <p className='error-message'>{error}</p>}
    </div>
  )
}

export default LoginForm;