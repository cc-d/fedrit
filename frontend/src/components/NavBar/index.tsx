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
    <nav className={dark}>
      <ul>
        <li>
          <Link to='/'>Home</Link>
        </li>
        <li>
          <Link to='/about'>About</Link>
        </li>
        {!user && (
          <li>
            <Link to='/login'>Login</Link>
          </li>
        )}
        {user && (
          <>
            <li>
              <Link to='/logout' onClick={handleLogout}>Logout</Link>
            </li>
            <li>
              <Link to='/community/all'>Communities</Link>
            </li>
          </>
        )}
        <li>
          <button onClick={handleTheme}>switch theme</button>
        </li>
      </ul>
      <h1>
        User: { user?.username }
      </h1>
    </nav>
  );
};

export default NavBar;