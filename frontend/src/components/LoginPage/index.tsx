import React, { useState } from 'react';
import Axios from 'axios';
import { API_URL, BASE_URL } from '../../config';
import { PlatformUser } from '../../types';
import { useNavigate } from 'react-router';

interface LoginFormInputs {
  username: string;
  password: string;
}

const LoginPage: React.FC = () => {
  const [user, setUser] = useState<PlatformUser | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [logUser, setLogUser] = useState<LoginFormInputs>({
    'username': '', 'password': '',
  })
  const [regUser, setRegUser] = useState<LoginFormInputs>({
    'username': '', 'password': '',
  })
  const navigate = useNavigate();

  const handleSubmit = async (
    event: React.FormEvent<HTMLFormElement>,
    action: string
    ) => {
    event.preventDefault();

    let response;
    let formUser = action == 'login' ? logUser : regUser;
    let fullUsername = action != 'register' 
      ? formUser.username + '@fedrit' : formUser.username

    response = await Axios.post(`${API_URL}/auth/${action}`, {
      username: fullUsername,
      password: formUser.password
    }).then(response => {
      // set token in localstorage and navigate to home
      localStorage.setItem('token', response.data.token)
      window.location.href = '/'
    }).catch(err => {
      setError(`failed ${action}`)
    })

  };

  return (
    <div>
      <div>
        <form id="form-login" onSubmit={e => handleSubmit(e, 'login')}>
          <input
            id="input-login-username"
            type="text"
            placeholder="Username"
            value={logUser.username}
            onChange={e => setLogUser({ ...logUser, username: e.target.value })}
          />
          <input
            id="input-login-password"
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
        <form id="form-register" autoComplete="off" onSubmit={e => handleSubmit(e, 'register')}>
          <input
            id="input-register-username"
            type="text"
            placeholder="Username"
            value={regUser.username}
            onChange={e => setRegUser({ ...regUser, username: e.target.value })}
          />
          <input
            id="input-register-password"
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