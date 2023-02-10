import axios from 'axios';
import React, { useContext, useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { PlatformUser } from '../../types';
import { AuthContext, AuthContextProps } from '../../AuthProvider';
import { API_URL, BASE_URL } from '../../config';
import authAxios from '../../utils';

const NavBar: React.FC = () => {
  const { user, isLoading, setUser }: any = useContext(AuthContext);

  const handleLogout = async () => {
    await authAxios.get(`${API_URL}/auth/logout`)
    .then((resp) => {
      setUser(null);
      localStorage.removeItem('token');
      window.location.reload();
    }).catch((err) => {
      console.error(err);
    });
  };

  return (
    <nav>
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
              <Link to='/create'>Create Community</Link>
            </li>
          </>
        )}
      </ul>
      <h1>
        User: { user?.username }
      </h1>
    </nav>
  );
};

export default NavBar;