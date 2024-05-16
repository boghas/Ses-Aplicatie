import React, { useState } from 'react';
import { useNavigate } from "react-router-dom";
import { ACCESS_TOKEN } from '../constants';

const LoginForm: React.FC = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate()

  const submitLogin = async () => {
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: JSON.stringify({
        grant_type: `grant_type=&username=${username}&password=${password}&scope=&client_id=&client_secret=`,
      }),
    };

    console.log('req opt', requestOptions);
    const response = await fetch(`${import.meta.env.VITE_API_URL}/token`, requestOptions);
    console.log(response);
    const data = await response.json();
    console.log('data', data);

    if (response.ok) {
      // Handle successful login (e.g., redirect user)
      console.log('Login successful');
      localStorage.setItem(ACCESS_TOKEN, data.access_token);
      console.log(localStorage.getItem(ACCESS_TOKEN));
      navigate('/');
    } else {
      // Handle failed login (e.g., show error message)
      console.error('Login failed');
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await submitLogin();
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        required
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        required
      />
      <button type="submit">Login</button>
    </form>
  );
};

export default LoginForm;
