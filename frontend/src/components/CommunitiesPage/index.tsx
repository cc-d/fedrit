import react, { useEffect, useState, useContext, ReactNode } from 'react';
import { PlatformUser, Community, Platform } from '../../types';
import {
    BrowserRouter, Routes, Route, Link
} from 'react-router-dom';
import authAxios from '../../utils';
import { API_URL, BASE_URL } from '../../config';
import { AuthContext, AuthContextProps } from '../../AuthProvider';

const CommunitiesPage: React.FC = () => {
    const { user, setUser, getUser }: any = useContext(AuthContext);
    const [communities, setCommunities] = useState<Array<Community>>([])
    const [getData, setGetData] = useState<boolean | null>(null);

    const fetchCommunities = async() => {
        try {
            const response = await authAxios.get(`${API_URL}/community/all`);
            setCommunities(response.data);
        } catch (err) {
            console.error(err);
        }
    }

    useEffect(() => {
        console.log(communities);
        if (getData === null) {
            setGetData(true);
        } else if (getData === true) {
            fetchCommunities().then(() => setGetData(false));
        }
    }, [communities, getData])

    const commItems = communities.map((comm: Community) => {
        return (
            <div style={{display: 'block'}}>
                <Link key={comm.id} to={`/c/${comm.name}`} style={{}}>
                    <p style={{ display: 'inline-block', marginRight: 4 }}>{comm.id}</p>
                    <p style={{ display: 'inline-block', fontWeight: 600 }}>{comm.name}</p>
                </Link>
            </div>
        )
    });

    return (
        <>
            <Link to='/community/new'>Create Community</Link>
            {commItems}
        </>
    )
}


export default CommunitiesPage;