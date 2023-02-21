import react, { useEffect, useState, useContext, ReactNode } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Post } from '../../types';
import authAxios from '../../utils';
import { API_URL, BASE_URL } from '../../config';
import CommunityPost from '../CommunityPost';

const Community: react.FC = (() => {
  const { communityName, communityId } = useParams();
  const [posts, setPosts] = useState<Array<Post> | null>(null);
  const [getPosts, setGetPosts] = useState<boolean | null>(null);

  const fetchPosts = async() => {
    try {
      const response: any = await authAxios.get(
        `${API_URL}/community/${communityName}/posts`);
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

  console.log('isposts');
  console.log(posts);

  return (
      <>
      <Link to={`/c/${communityName}/create_post`}>New Post</Link>
        <h1>
          Community
          <>
            {communityName ? `Name: ${communityName} ${communityId}`
              : `ID: ${communityName} ${communityId}`}
          </>
        </h1>
        <h1>Posts:</h1>
        {posts && posts.map((post: Post) => {
          return (
            <CommunityPost id={post.id} post={post} />
          )
        })}
      </>
  );
})

export default Community;
