import React, { useState } from 'react';
import { PlatformUser } from '../../types';
import { Link, useNavigate } from 'react-router-dom';
import authAxios from '../../utils';
import { BASE_URL } from '../../config';
import { createBrowserRouter } from 'react-router-dom';

interface CreateCommunityFormData {
  community_type: string;
  name: string;
}

const CreateCommunityPage: React.FC = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState<CreateCommunityFormData>({
    community_type: 'SUB',
    name: '',
  });

  const handleChange = (
    event: React.ChangeEvent<HTMLSelectElement | HTMLInputElement>
  ) => {
    setFormData({
        ...formData, [event.target.name]: event.target.value
    });
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    
    const { community_type, name } = formData;
    const body = JSON.stringify({community_type, name});

    try {
      const response = await authAxios.post(
        `${BASE_URL}/api/community/create_community`, formData);
      navigate('/communities');
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div id="CreateCommunityPage">
      <h2>Create Community</h2>
      <form onSubmit={handleSubmit}>
        <label>
          Community Type:
          <select
            name="communityType"
            value={formData.community_type}
            onChange={handleChange}
          >
            <option value="">Select community type</option>
            <option value="SUB">Subreddit</option>
            <option value="IMGBOARD">ImageBoard</option>
            <option value="FORUM">Forum</option>
          </select>
        </label>
        <br />
        <label>
          Name:
          <input
            type="text"
            name="name"
            value={formData.name}
            onChange={handleChange}
          />
        </label>
        <br />
        <button type="submit">Create Community</button>
      </form>
    </div>
  )
}

export default CreateCommunityPage;