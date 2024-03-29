import React, { useState } from 'react';
import Axios from 'axios';
import { API_URL } from '../../config';
import '../../styles/styles.css';

interface RegisterFormInputs {
  plat_username: string;
  password: string;
}

const RegisterForm: React.FC = () => {
  const [regUser, setRegUser] = useState<RegisterFormInputs>({
    plat_username: '',
    password: '',
  });
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    const response = await Axios.post(`${API_URL}/auth/register`, {
      plat_username: regUser.plat_username,
      password: regUser.password,
    })
      .then((resp) => {
        // Redirect to login page upon successful registration
        localStorage.setItem('token', resp.data.token)
        window.location.href = '/';
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
          id="input-register-plat_username"
          type="text"
          placeholder="Username"
          value={regUser.plat_username}
          onChange={(e) =>
            setRegUser({ ...regUser, plat_username: e.target.value })
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
