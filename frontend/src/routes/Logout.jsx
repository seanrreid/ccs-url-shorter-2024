import { useEffect } from 'react';
import { useLoaderData, useNavigate } from 'react-router-dom';
import { useAuth } from '../AuthContext';

export async function loader() {
    const url = 'http://localhost:8000/logout/';
    // const refresh_token = localStorage.getItem('refresh_token');
    const access_token = localStorage.getItem('access_token');

    const response = await fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${access_token}`,
        },
    });
    const statusCode = response.status;
    return statusCode === 200 ? true : false;
}

const Logout = () => {
    const response = useLoaderData();
    const navigate = useNavigate();
    const { setIsAuth } = useAuth();

    if (response) {
        localStorage.clear();
        setIsAuth(false);
    } else {
        alert('PROBLEM LOGGING OUT');
    }

    useEffect(() => {
        return navigate(`/login`);
    }, [response, navigate]);
};

export default Logout;