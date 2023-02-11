import React from 'react';
import logo from './logo.svg';
import './App.css';
import { 
  BrowserRouter, Routes, Route, Link,
} from 'react-router-dom';

import AuthProvider from './AuthProvider';

import AboutPage from './components/AboutPage';
import CommunitiesPage from './components/CommunitiesPage';
import CreateCommunityPage from './components/CreateCommunityPage';
import LoginPage from './components/LoginPage';
import HomePage from './components/HomePage';
import NavBar from './components/NavBar';


function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <NavBar />
        <Routes>
          <Route path='/' element={<HomePage />} />
          <Route path='/about' element={<AboutPage />} />
          <Route path='/login' element={<LoginPage />} />
          <Route path='/communities' element={<CommunitiesPage />} />
          <Route path='/communities/new' element={<CreateCommunityPage />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
