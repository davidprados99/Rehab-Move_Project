import Login from './pages/Login';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import PhysioDashboard from './pages/PhysioDashboard';
import PatientDashboard from './pages/PatientDashboard';
import NavBar from './components/NavBar';
import ExerciseAssigned from './pages/ExerciseAssigned';
import Appointments from './pages/Appointments';
import PainRegistry from './pages/PainRegistry';
import ProtectedRoute from './components/ProtectedRoute';



function App() {
  return (
    <Router>
      <Routes>
            {/* Public routes */}
            <Route path="/login" element={<Login />} />

            {/* Patient routes */}
            <Route path="/patient-dashboard"
              element={<ProtectedRoute allowedRoles={['patient']}>
                <><NavBar /><PatientDashboard /></>
              </ProtectedRoute>}
            />
            <Route path="/exercise-assigned"
              element={<ProtectedRoute allowedRoles={['patient']}>
                <><NavBar /><ExerciseAssigned /></>
              </ProtectedRoute>}
            />

            <Route path="/appointments"
              element={<ProtectedRoute allowedRoles={['patient']}>
                <><NavBar /><Appointments /></>
              </ProtectedRoute>}
            />

            <Route path="/pain-registry"
              element={<ProtectedRoute allowedRoles={['patient']}>
                <><NavBar /><PainRegistry /></>
              </ProtectedRoute>}
            />

            {/* Physio routes */}
            <Route path="/physio-dashboard"
              element={<ProtectedRoute allowedRoles={['physio']}>
                <><NavBar /><PhysioDashboard /></>
              </ProtectedRoute>}
            />

            {/* Catch-all route */}
            <Route path="*" element={<Navigate to="/login" />} />

      </Routes>
    </Router>
  );
}

export default App
