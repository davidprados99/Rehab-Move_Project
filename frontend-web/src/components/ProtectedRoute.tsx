import {Navigate} from 'react-router-dom';
import type { JSX } from 'react/jsx-dev-runtime';

interface ProtectedRouteProps {
    children: JSX.Element;
    allowedRoles: string[];
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children, allowedRoles }) => {
    const token = localStorage.getItem('token');
    const userRole = localStorage.getItem('role');

    if (!token) {
        // No token, redirect to login
        return <Navigate to="/login" replace />;
    }

    if (allowedRoles.length > 0 && !allowedRoles.includes(userRole || '')) {
        // User role is not allowed, redirect to login or an unauthorized page
        return <Navigate to="/login" replace />;
    }

    //If all ok, render the children components
    return  children;
};

export default ProtectedRoute;