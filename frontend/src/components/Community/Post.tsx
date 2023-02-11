import react, { useEffect, useState, useContext, ReactNode } from 'react';
import { PlatformUser, Community, Platform } from '../../types';
import {
    BrowserRouter, Routes, Route, Link
} from 'react-router-dom';
import authAxios from '../../utils';
import { API_URL, BASE_URL } from '../../config';
import { AuthContext, AuthContextProps } from '../../AuthProvider';

const CommunityPost: react.FC = () => {
    return (
        <>
            <div className='compost'>
                <p className="compost-title"></p>
            </div>
        </>
    )
}

export {CommunityPost};