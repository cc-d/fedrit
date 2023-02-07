import axios from 'axios';
import React, { useContext, useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { PlatformUser } from '../../types';
import { AuthContext, AuthContextProps } from '../../AuthProvider';

const NavBar: React.FC = () => {
  const { user, isLoading }: any = useContext(AuthContext);

  return (
    <nav>
      <ul>
        <li>
          <Link to='/'>Home</Link>
        </li>
        <li>
          <Link to='/about'>About</Link>
        </li>
        <li>
          <Link to='/login'>Login</Link>
        </li>
      </ul>
      <h1>
        User: { user?.username }
      </h1>
    </nav>
  );
};

export default NavBar;