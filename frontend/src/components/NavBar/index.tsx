import axios from 'axios';
import React, { useContext, useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { PlatformUser } from '../../types';
import { AuthContext, AuthContextProps } from '../../auth';
import { API_URL, BASE_URL } from '../../config';
import authAxios from '../../utils';

const NavBar: React.FC = () => {
  const navigate = useNavigate();
  const { user, setUser, dark, setDark }: any = useContext(AuthContext);

  const handleLogout = async () => {
    await authAxios.post(`${API_URL}/auth/logout`)
      .then((resp) => {
        setUser(null);
        localStorage.removeItem('token');
        window.location.href = `/`
      }).catch((err) => {
        console.error(err);
      });
  };

  const handleTheme = async () => {
    if (dark) {
      setDark('');
    } else {
      setDark(' dark');
    }
  }

  return (
    <nav
      className={dark}
      style={{

      }}
    >
      <Link to='/' className='navlink'>Home</Link>
      <Link to='/about' className='navlink'>About</Link>
      {!user && (
        <Link to='/login' className='navlink'>Login</Link>
      )}
      {user && (
        <>
          <Link to='/logout' className='navlink' onClick={handleLogout}>Logout</Link>
          <Link to='/community/all' className='navlink'>Communities</Link>
        </>
      )}
      <button onClick={handleTheme}>switch theme</button>
      <div className='navuser'>
        User: {user?.username}
      </div>
    </nav>
  );
};

export default NavBar;