import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import App from './App.jsx'
import ResetPassword from './pages/ResetPassword'
import ActivateStand from './pages/ActivateStand'
import './styles/global.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/reset-password" element={<ResetPassword />} />
        <Route path="/activate-stand/:id" element={<ActivateStand />} />
        <Route path="*" element={<App />} />
      </Routes>
    </BrowserRouter>
  </React.StrictMode>,
)
