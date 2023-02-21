import react, { useEffect, useState, useContext, ReactNode } from 'react';
import { useParams, Link } from 'react-router-dom';
import {
  PlatformUser, Post, Platform, Community
} from '../../types';
import authAxios from '../../utils';
import { API_URL, BASE_URL } from '../../config';
import CommunityPost from '../CommunityPost';
import { AuthContext, AuthContextProps } from '../../auth';

const HomePage: react.FC = (): any => {
  const [posts, setPosts] = useState<Array<Post> | null>(null);
  const [getPosts, setGetPosts] = useState<boolean | null>(null);
  const { user, setUser, dark }: any = useContext(AuthContext);

  const fetchPosts = async () => {
    try {
      const response: any = await authAxios.get(
        `${API_URL}/post/all`);
      return response.data;
    } catch (err) {
      console.error(err);
    }
  }

  useEffect(() => {
    if (getPosts === null) {
      setGetPosts(true);
    } else if (getPosts === true) {
      fetchPosts().then((data: Array<Post>) => {
        console.log('fetchposthten');
        console.log(data);
        setPosts(data);
      }).finally(() => {
        setGetPosts(false);
      });
    }
  }, [getPosts])

  return (
    <div id="HomePage" className={dark}>
      Home Page Works
      <>  
        <h1>All Posts:</h1>
        {posts && posts.map((post: Post) => {
          return (
            <CommunityPost id={post.id} key={post.id} post={post} />
          )
        })}
      </>
    </div>
  )
}

export default HomePage;