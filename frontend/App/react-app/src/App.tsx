import React from "react";
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Home from './Home'
import Detalii from "./Detalii";
import Login from "./pages/Login";
import ProtectedRoute from "./components/ProtectedRoute";


function Logout() {
  localStorage.clear();
  return <Navigate to="/login" />
}



const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<ProtectedRoute><Home /></ProtectedRoute> } />
        <Route path='/detalii/:client_id' element={<ProtectedRoute><Detalii /></ProtectedRoute> } />
        <Route path='/login' element={<Login />} />
        <Route path='/logout' element={<Logout />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
