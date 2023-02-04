import axios from 'axios';
import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { PlatformUser } from '../../types';

const NavBar: React.FC = () => {
  const [user, setUser] = useState<PlatformUser | null>(null);

  useEffect(() => {
    // Make API request to /user here
    axios.get('/user')
      .then(response => {
        setUser(response.data);
      })
      .catch(error => {
        console.error(error);
      });
  }, []);
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
    </nav>
  );
};

export default NavBar;