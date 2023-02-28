import react, { useEffect, useState, useContext, ReactNode } from 'react';
import { PlatformUser, Community, Platform, Post } from '../../types';
import {
  BrowserRouter, Routes, Route, Link, useParams
} from 'react-router-dom';
import authAxios from '../../utils';
import { API_URL, BASE_URL } from '../../config';
import { AuthContext, AuthContextProps } from '../../auth';

interface Props {
  id: string | undefined;
  post: Post;
}

const CommunityPost: react.FC<Props> = ({ post }) => {
  console.log('propspost');
  console.log(post);
  const { communityName, communityId } = useParams();
  const { user, setUser, dark }: any = useContext(AuthContext);

  var useName = communityName;

  if (post && post.community && post.community.name) {
    useName = post.community.name;
  }

  return (
    <div
      className={'community-post' + dark}
      style={{  }}
      key={post.id}>
      <Link 
        style={{fontSize: '200%' }} 
        to={`/c/${useName}/p/${post.id}`}
      >
        {post.title}
      </Link>
      <p>
        {post.author.username}
      </p>
      <p style={{

      }}>
        {post.text}
      </p>
    </div>

  )
}

export default CommunityPost;