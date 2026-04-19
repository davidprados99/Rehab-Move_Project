import React , { useState } from 'react';
import type { SyntheticEvent } from 'react';
import { authService } from '../services/auth.service';
import '../index.css'
import logo from '../assets/logo_Rehab_Move.png';
import { useNavigate } from 'react-router-dom';


function Login() {
    //States for get the user inputs
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleLogin = async (e: SyntheticEvent<HTMLFormElement>) => {
        e.preventDefault();
        setLoading(true);
        try {
            // Call the login function from authService
            const data = await authService.login(email, password);

            console.log('Server response:', data);

            // Store the token and user info in localStorage
            localStorage.setItem('token', data.access_token);
            localStorage.setItem('role', data.role);
            localStorage.setItem('user_id', data.user_id.toString());
            localStorage.setItem('name', data.name);

            alert(`¡Hola ${data.name}!`);
            
            // Redirect based on user role
            if (data.role == 'physio') {
                navigate('/physio-dashboard');
            } else {
                navigate('/patient-dashboard');
            } 

        } catch (error: any) {
            console.error('Login error:', error);
            alert('Error al iniciar sesión. Por favor, inténtelo de nuevo.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-rehab-light flex items-center justify-center p-4 font-sans">

            <div className="max-w-md w-full bg-white rounded-rehab shadow-xl p-10">

                <div className="text-center mb-8">

                    <div className="w-[120px] h-[120px] mx-auto rounded-full overflow-hidden bg-transparent">

                        <img
                            src={logo}
                            alt="Rehab & Move Logo"
                            className="w-full h-full object-cover scale-90"
                        />

                    </div>

                    <h1 className="text-rehab-primary text-[22px] font-bold tracking-wide mt-4">
                        ¡Bienvenido!
                    </h1>

                </div>

                <form onSubmit={handleLogin} className="space-y-5">
                    <div>
                        <label className="block text-sm font-semibold text-gray-500 mb-1 ml-1">Email</label>
                        <input
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            className="w-full px-4 py-3 bg-[#FAFAFA] border-2 border-[#E0E0E0] rounded-[10px] focus:border-rehab-accent outline-none transition-all"
                            placeholder="correo@ejemplo.com"
                            required
                        />
                    </div>

                    <div>
                        <label className="block text-sm font-semibold text-gray-500 mb-1 ml-1">Contraseña</label>
                        <input
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className="w-full px-4 py-3 bg-[#FAFAFA] border-2 border-[#E0E0E0] rounded-[10px] focus:border-rehab-accent outline-none transition-all"
                            placeholder="••••••••"
                            required
                        />
                    </div>

                    <div className="flex flex-col gap-3 pt-2">
                        <button
                            type="submit"
                            disabled={loading}
                            className="w-full bg-rehab-primary hover:brightness-90 text-[white] font-bold py-3 rounded-[10px] transition-all shadow-md active:scale-[0.98]"
                        >
                            {/* Show loading text when the login process is ongoing, otherwise show "Entrar" */}
                            {loading ? 'CARGANDO...' : 'Entrar'}
                        </button>

                        <button
                            type="button"
                            className="w-full bg-[#E0E0E0] hover:bg-[#D1D8D7] text-[#333333] font-bold py-3 rounded-[10px] transition-colors"
                        >
                            Cancelar
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}

export default Login
