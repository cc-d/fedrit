import react, { useEffect, useState, useContext, ReactNode } from 'react';
import { PlatformUser, Community, Platform } from '../../types';
import {
    BrowserRouter, Routes, Route, Link, useParams, useNavigate
} from 'react-router-dom';
import authAxios from '../../utils';
import { API_URL, BASE_URL } from '../../config';
import { AuthContext, AuthContextProps } from '../../AuthProvider';

const CreatePost: react.FC = (() => {
  const { communityName, communityId } = useParams();
  const [ title, setTitle ] = useState<string>('');
  const [ text, setText ] = useState<string>('');
  const navigate = useNavigate();

  const handleSubmit = async (
      event: react.FormEvent<HTMLFormElement>
    ) => {
        event.preventDefault();
        try {
            const response = await authAxios.post(`${API_URL}/post/create_post`, {
                community_id: communityId,
                community_name: communityName,
                title: title,
                text: text,
            });
            navigate(`${BASE_URL}/c/${communityName}`);

        } catch (err) {
            console.error(err);
        }
  };

  return (
    <>
      <h1>create post for {communityId} {communityName}</h1>
      <form id="form-create-post" onSubmit={e => handleSubmit(e)}>
        <input id="input-post-title" 
          type="text" 
          placeholder="title" 
          value={title} 
          onChange={e => setTitle(e.target.value)}
        />
        <input id="input-post-text"
            type="text"
            placeholder="text"
            value={text}
            onChange={e => setText(e.target.value)}
        />
        <button type="submit">Create Post</button>
      </form>
    </>
  )
})

export default CreatePost;