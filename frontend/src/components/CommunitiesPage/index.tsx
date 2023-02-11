import react, { useEffect, useState, useContext, ReactNode } from 'react';
import { PlatformUser, Community, Platform } from '../../types';
import {
    BrowserRouter, Routes, Route, Link
} from 'react-router-dom';
import authAxios from '../../utils';
import { API_URL } from '../../config';
import { AuthContext, AuthContextProps } from '../../AuthProvider';

const CommunitiesPage: React.FC = () => {
    const { user, setUser, getUser }: any = useContext(AuthContext);
    const [communities, setCommunities] = useState<Array<Community>>([])
    const [loading, setLoading] = useState<boolean | null>(null);

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
        if (loading === null) {
            setLoading(true);
        } else if (loading === true) {
            fetchCommunities().then(() => setLoading(false));
        }
    }, [communities, loading])

    const commItems = communities.map((comm) => {
        return <div key={comm.id}>{comm.id}</div>
    });

    return (
        <>
            <Link to='/communities/new'>Create Community</Link>
            {commItems}
        </>
    )
}


export default CommunitiesPage;