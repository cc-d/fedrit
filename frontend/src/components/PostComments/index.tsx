import react, { useEffect, useState, useContext, ReactNode } from 'react';
import { PlatformUser, Community, Platform, Post, Comment } from '../../types';
import {
    BrowserRouter, Routes, Route, Link, useParams
} from 'react-router-dom';
import authAxios from '../../utils';
import { API_URL, BASE_URL } from '../../config';
import { AuthContext, AuthContextProps } from '../../auth';

interface PC {
    post: Post,
    comments: Array<Comment>
}

const PostComments: react.FC<any> = () => {
    const { communityName, communityId, postId } = useParams();
    const [post, setPost] = useState<Post | null>(null);
    const [comms, setComms] = useState<Array<Comment> | null>(null);
    const [getPCs, setGetPCs] = useState<boolean | null>(null);

    const [newComm, setNewComm] = useState<string | null>(null);

    const fetchPCs = async () => {
        try {
            const response: any = await authAxios.get(
                `${API_URL}/post/${postId}/comments`);
            return response.data;
        } catch (err) {
            console.error(err);
        }
    }

    const handleNewComm = async () => {
        
    }

    useEffect(() => {
        if (getPCs === null) {
            setGetPCs(true);
        } else if (getPCs === true) {
            fetchPCs().then((data: PC) => {
                setGetPCs(false);
                setPost(data?.post);
                setComms(data?.comments);
            });
        }
    }, [getPCs, post, comms])

    return (
        <>
        <div>
            <h2>Post:</h2>
                <>
                {post &&
                    <div style={{border: '1px dashed black', margin: 4}}>
                            <h3>Title: {post.title}</h3>
                            <p>Text: {post.text}</p>
                    </div>
                }
                </>
        </div>
        <div>
            <h1>create post for {communityId} {communityName}</h1>
            <form id="form-new-comm" onSubmit={(e) => handleNewComm()}>
                <input id="input-new-comm"
                    type="text"
                    placeholder="new comment text"
                    onChange={e => setNewComm(e.target.value)}
                />
                <button type="submit">Comment</button>
            </form>
            <h2>Comments:</h2>
            <>
                {comms && 
                    comms.map((comm: Comment) => {
                        <p>{comm.id}</p>
                    })
                }
            </>
        </div>
        </>
    )
}

export default PostComments;