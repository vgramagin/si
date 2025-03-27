import React, { useState } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';

function LoginForm({ onLogin }) {
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('/auth', { password });
            const { token } = response.data;
            Cookies.set('authToken', token);
            sessionStorage.setItem('authToken', token);
            onLogin();
        } catch (err) {
            setError('Invalid password');
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter password"
            />
            <button type="submit">Login</button>
            {error && <p>{error}</p>}
        </form>
    );
}

export default LoginForm;