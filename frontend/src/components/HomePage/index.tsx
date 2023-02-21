import react, { useEffect, useState, useContext, ReactNode } from 'react';
import { useParams, Link } from 'react-router-dom';
import {
  PlatformUser, Post, Platform, Community
} from '../../types';
import authAxios from '../../utils';
import { API_URL, BASE_URL } from '../../config';
import CommunityPost from '../Post';

const HomePage: react.FC = (): any => {
  const [posts, setPosts] = useState<Array<Post> | null>(null);
  const [getPosts, setGetPosts] = useState<boolean | null>(null);

  const fetchPosts = async () => {
    try {
      const response: any = await authAxios.get(
        `${API_URL}/community/test/posts`);
      return response.data;
    } catch (err) {
      console.error(err);
    }
  }

  return (
    <div id="HomePage">
      Home Page Works
    </div>
  )
}

export default HomePage;