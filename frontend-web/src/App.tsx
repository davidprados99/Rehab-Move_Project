import Login from './pages/Login';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import PhysioDashboard from './pages/PhysioDashboard';
import PatientDashboard from './pages/PatientDashboard';


function App() {
  return (
    <Router>
      <Routes>
        {/* Declare routes */}
        <Route path="/" element={<Login />} />

        {/* Temporary routes */}
        <Route path="/physio-dashboard" element={<PhysioDashboard />} />
        <Route path="/patient-dashboard" element={<PatientDashboard />} />

        {/* Redirection for any other path */}
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </Router>
  );
}

export default App
