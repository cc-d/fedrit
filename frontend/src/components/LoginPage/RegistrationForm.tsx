import React, { useState } from 'react';
import Axios from 'axios';
import { API_URL } from '../../config';
import '../../styles/styles.css';

interface RegisterFormInputs {
  username: string;
  password: string;
}

const RegisterForm: React.FC = () => {
  const [regUser, setRegUser] = useState<RegisterFormInputs>({
    username: '',
    password: '',
  });
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    const response = await Axios.post(`${API_URL}/auth/register`, {
      username: regUser.username,
      password: regUser.password,
    })
      .then((response) => {
        // Redirect to login page upon successful registration
        window.location.href = '/login';
      })
      .catch((err) => {
        setError('Registration failed');
      });
  };

  return (
    <div className="form-wrapper">
      <h2>Register</h2>
      <form id="form-register" onSubmit={handleSubmit}>
        <input
          id="input-register-username"
          type="text"
          placeholder="Username"
          value={regUser.username}
          onChange={(e) =>
            setRegUser({ ...regUser, username: e.target.value })
          }
        />
        <input
          id="input-register-password"
          type="password"
          placeholder="Password"
          value={regUser.password}
          onChange={(e) =>
            setRegUser({ ...regUser, password: e.target.value })
          }
        />
        <button type="submit">Register</button>
      </form>
      {error && <p className="error-message">{error}</p>}
    </div>
  );
};

export default RegisterForm;
