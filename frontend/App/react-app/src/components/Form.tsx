import React, { useState } from "react";
import axios from "axios";
import api from "../api";
import { useNavigate } from "react-router-dom";
import { ACCESS_TOKEN } from "../constants";
import "../styles/Form.css";

interface FormProps {
    route: string;
    method: "login" | "not-found"; // Adjust the method type based on your requirements
}

const Form: React.FC<FormProps> = ({ route, method }) => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const pageName = method === "login" ? "Login" : "Not Found";

    

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        setLoading(true);
        e.preventDefault();
        
        try {
            // Send login request to backend
            const response = await api.post(route, { username, password }, {
                
              method: 'POST',
              headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'application/json',
              },
            });
            
            if (response) {
                console.log(route);
              // Handle successful login (e.g., redirect user)
              console.log(response.data.ACCESS_TOKEN)
              navigate('/');
              console.log('Login successful');
            } else {
              // Handle failed login (e.g., show error message)
              console.error('Login failed');
            }
          }catch (error) {
            alert(error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <form onSubmit={handleSubmit} className="form-container">
            <h1>{pageName}</h1>
            <input
                className="form-input"
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Username"
            />
            <input
                className="form-input"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Password"
            />
            <button className="form-button" type="submit">
                {pageName}
            </button>
        </form>
    );
};

export default Form;
