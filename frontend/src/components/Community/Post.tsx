import react, { useEffect, useState, useContext, ReactNode } from 'react';
import { PlatformUser, Community, Platform, Post } from '../../types';
import {
    BrowserRouter, Routes, Route, Link, useParams
} from 'react-router-dom';
import authAxios from '../../utils';
import { API_URL, BASE_URL } from '../../config';
import { AuthContext, AuthContextProps } from '../../AuthProvider';

interface Props {
    id: string | undefined;
    post: Post;
}

const CommunityPost: react.FC<Props> = ({ post }) => {
    console.log('propspost');
    console.log(post);
    const { communityName, communityId } = useParams();
    return (
        <>
            <div style={{border: '1px dashed black', margin: 4}}id={post.id}>
                <Link style={{margin: 4, fontSize: '200%'}}to={`/c/${communityName}/p/${post.id}`}>{post.title}</Link>
                <p style={{margin: 4}}>{post.text}</p>
            </div>
        </>
    )
}

export default CommunityPost;