import React from 'react';
import LoginForm from './LoginForm';
import RegistrationForm from './RegistrationForm';
import '../../styles/styles.css';

const LoginPage: React.FC = () => {
  return (
    <div className="login-page">
      <div className="forms-container">
        <LoginForm />
        <RegistrationForm />
      </div>
    </div>
  );
};

export default LoginPage;