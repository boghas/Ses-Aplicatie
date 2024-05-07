import React from "react"
import {BrowserRouter, Routes, Route} from 'react-router-dom'
import Home from './CRUD/Home'
import Detalii from "./CRUD/Detalii"

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<Home />} ></Route>
        <Route path='/detalii/:client_id' element={<Detalii />} ></Route>
      </Routes>
      </BrowserRouter>
  )
}

export default App