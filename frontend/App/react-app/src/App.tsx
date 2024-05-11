import React from "react";
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './Home'
import Detalii from "./Detalii";
import DownloadFileButton from "./components/DownloadFileButton";

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<Home />} />
        <Route path='/detalii/:client_id' element={<Detalii />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;