/* eslint-disable react-refresh/only-export-components */
import { Form, Navigate, useActionData } from 'react-router-dom';
import { useAuth } from '../AuthContext';
import Wrapper from '../components/Wrapper';
import Button from '../components/Button';

import styles from './form.module.css';
import { useEffect } from 'react';

export const action = async ({ request }) => {
    const formData = await request.formData();
    const email = formData.get('email');
    const password = formData.get('password');

    const loginData = { email, password };

    try {
        const url = 'http://localhost:8000/login';
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(loginData),
        });

        const statusCode = response.status;
        const data = await response.json();

        const { access_token, refresh_token } = data;
        localStorage.clear();
        localStorage.setItem('access_token', access_token);
        localStorage.setItem('refresh_token', refresh_token);
        return statusCode === 200 ? true : false;
    } catch (error) {
        console.error('ERROR: ', error);
        return false;
    }
};

const Login = () => {
    const { isAuth, setIsAuth } = useAuth();
    const response = useActionData();

    useEffect(() => {
        setIsAuth(response);
    }, [response, setIsAuth]);

    return !isAuth ? (
        <Wrapper>
            <h1>Login</h1>
            <Form method="post" className={styles.form}>
                <label>
                    Email Address
                    <input type="email" name="email" />
                </label>
                <label>
                    Password
                    <input type="password" name="password" />
                </label>
                <Button type="submit">Login</Button>
            </Form>
        </Wrapper>
    ) : (
        <Navigate to="/" />
    );
};

export default Login;
