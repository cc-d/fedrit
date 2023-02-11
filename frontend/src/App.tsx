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
import Community from './components/Community';
import CreatePost from './components/CreatePost';


function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <NavBar />
        <Routes>
          <Route path='/' element={<HomePage />} />
          <Route path='/about' element={<AboutPage />} />
          <Route path='/login' element={<LoginPage />} />
          <Route path='/community/all' element={<CommunitiesPage />} />
          <Route path='/community/new' element={<CreateCommunityPage />} />
          <Route path='/c/:communityName/:communityId?' element={<Community />} />
          <Route path='/c/:communityName/:communityId?/create_post' element={<CreatePost />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
