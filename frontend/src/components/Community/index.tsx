import react, { useEffect, useState, useContext, ReactNode } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Post } from '../../types';
import authAxios from '../../utils';
import { API_URL, BASE_URL } from '../../config';
import { CommunityPost } from './Post';

const Community: react.FC = (() => {
  const { communityName, communityId } = useParams();
  const [posts, setPosts] = useState<Array<Post> | null>(null);
  const [getPosts, setGetPosts] = useState<boolean | null>(null);

  const fetchPosts = async() => {
    try {
      const response = await authAxios.get(`${API_URL}/community/${communityName}/posts`);
    } catch (err) {
      console.error(err);
    }
  }

  useEffect(() => {
    if (getPosts === null) {
      setGetPosts(true);
    } else if (getPosts === true) {
      fetchPosts().then(() => setGetPosts(false));
    }
  }, [posts, getPosts])

  return (
    <>
        <Link to={`/c/${communityName}/create_post`}>New Post</Link>
      <div>
        <h1>
          Community
          {communityName ? `Name: ${communityName} ${communityId}`
            : `ID: ${communityName} ${communityId}`}
        </h1>
        <h1>Posts:</h1>
        <>
          {posts && posts.map((post) => {
            <CommunityPost key={post.id} />
          })}
        </>
      </div>
    </>
  );
})

export default Community;
