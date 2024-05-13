import { Navigate } from "react-router-dom";
import { jwtDecode } from "jwt-decode";
import api from "../api";
import { ACCESS_TOKEN } from "../constants";
import { useState, useEffect } from "react";

function ProtectedRoute({ children }: { children: React.ReactNode }) {
    const [isAuthorized, setIsAuthorized] = useState<boolean | null>(null);

    console.log('here')

    useEffect(() => {
        auth().catch(() => setIsAuthorized(false));
    }, []);

    const auth = async () => {
        const token = localStorage.getItem(ACCESS_TOKEN);
        console.log(token)
        if (!token) {
            console.log('true');
            setIsAuthorized(false);
            return;
        }
        const decoded: any = jwtDecode(token);
        const tokenExpiration: number = decoded.exp;
        const now: number = Date.now() / 1000;

        console.log(token);
        console.log(tokenExpiration);
        console.log(now);
        //console.log(token);

        if (tokenExpiration < now) {
            console.log('truee')
            return <Navigate to="/login" />;
        } else {
            setIsAuthorized(true);
            console.log('????')
        }
    };

    if (isAuthorized === null) {
        return <div>Loading...</div>;
    }

    return isAuthorized ? <>{children}</> : <Navigate to="/login" />;
}

export default ProtectedRoute;
