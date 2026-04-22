import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import logo from '../assets/logo_Rehab_Move.png';
import '../index.css';

const NavBar: React.FC = () => {
    const navigate = useNavigate();
    const UserName = localStorage.getItem('name') || 'Paciente';
    const UserRole = localStorage.getItem('role');

    const handleLogout = () => {
        localStorage.clear();
        navigate("/login");
    };

    // Link styles
    const linkStyles = ({ isActive }: { isActive: boolean }) =>
        `px-3 py-2 rounded-md text-sm font-medium transition-all ${isActive
            ? 'text-rehab-primary border-b-2 border-rehab-primary'
            : 'text-gray-600 hover:text-rehab-primary hover:bg-gray-50'
        }`;

    return (
        <nav className="bg-white shadow-sm border-b border-gray-100 sticky top-0 z-50">
            <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between h-16 items-center">

                    {/* Left side: logo */}
                    <div className="flex items-center gap-4 cursor-pointer" onClick={() => navigate(UserRole === 'physio' ? '/physio-dashboard' : '/patient-dashboard')}>
                        <img src={logo} alt="Logo" className="h-10 w-auto" />
                        <span className="text-rehab-dark font-bold text-lg hidden md:block">Rehab & Move</span>
                    </div>

                    {/* Center: Navigation */}
                    <div className="hidden sm:flex sm:space-x-8">
                        <NavLink title="Inicio" to={UserRole === 'patient' ? '/patient-dashboard' : '/physio-dashboard'} className={linkStyles}>Home</NavLink>
                        {UserRole === 'patient' && (
                            <>
                                <NavLink title="Mis Ejercicios" to="/exercise-assigned" className={linkStyles}>Mis Ejercicios</NavLink>
                                <NavLink title="Mis Citas" to="/appointments" className={linkStyles}>Mis Citas</NavLink>
                                <NavLink title="Registros de Dolor" to="/pain-registry" className={linkStyles}>Registros de Dolor</NavLink>
                            </>
                        )}
                    </div>

                    {/* Right side: User and Logout */}
                    <div className="flex items-center gap-4">
                        <span className="text-sm text-gray-500 hidden lg:block italic">Hola {UserName}</span>
                        <button
                            onClick={handleLogout}
                            className="bg-red-50 text-red-600 px-4 py-2 rounded-lg text-sm font-semibold hover:bg-red-100 transition-colors"
                        >
                            Salir
                        </button>
                    </div>
                </div>
            </div>
        </nav>
    );
};

export default NavBar;