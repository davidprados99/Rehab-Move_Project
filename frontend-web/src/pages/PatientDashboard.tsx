import React from 'react';
import '../index.css';
import exerciseImage from '../assets/ejercicio.jpg';
import iconCalendar from '../assets/iconoCalendario.webp';
import iconPain from '../assets/dolorFoto.jpg';
import logo from '../assets/logo_Rehab_Move.png';

//Mock data
const patientData = {
    name: 'Lucía',
    tieneEjercicios: true,
    proximasCitas: 2
};

//Use const to define the component, and React.FC for type safety
const PatientDashboard: React.FC = () => {
    return (

        <div className="min-h-screen bg-gray-50 w-full">
            <div className="max-w-4xl mx-auto p-6">

                {/* Welcome header */}
                <header className="mt-5 mb-10 text-center">
                    <h1 className="text-3xl font-bold text-rehab-dark mb-2">¡Hola de nuevo, {patientData.name}!</h1>
                    <p className="text-lg text-rehab-dark">Te damos la bienvenida a tu panel de paciente.</p>
                </header>

                {/* Exercise section */}
                <div className="bg-rehab-dark text-white rounded-rehab shadow-lg overflow-hidden flex flex-col md:flex-row items-center">
                    {patientData.tieneEjercicios ? (
                        /* Text container*/
                        <div className="p-8 flex-1">
                            <h2 className="text-2xl font-bold mb-2">¡A por ello!</h2>
                            <p className="text-rehab-light/80 mb-6">Tu fisioterapeuta ha preparado una rutina nueva para ti.</p>
                            <button className="bg-rehab-primary hover:bg-rehab-primary/90 text-white font-bold px-6 py-2 rounded-lg transition-all">
                                Ver ejercicios
                            </button>
                        </div>
                    ) : (
                        <div className="p-8 flex-1">
                            <h2 className="text-2xl font-bold mb-2">¡Sin ejercicios por ahora!</h2>
                            <p className="text-rehab-light/80 mb-6">Tu fisioterapeuta no ha asignado ejercicios todavía. ¡Mantente atento!</p>
                        </div>
                    )}
                    {/* Image container */}
                    <div className="w-full md:w-1/3 h-48 md:h-full min-h-[200px] relative">
                        <img
                            src={exerciseImage}
                            alt="Paciente haciendo ejercicio"
                            className="absolute inset-0 w-full h-full object-cover opacity-80 hover:opacity-100 transition-opacity duration-500"
                        />
                        {/* A gradient to blend the image with the dark background */}
                        <div className="absolute inset-0 bg-gradient-to-t md:bg-gradient-to-l from-rehab-dark/0 to-rehab-dark" />
                    </div>
                </div>

                {/* Upcoming appointments section */}
                <div className="mt-10 mb-10 bg-rehab-dark text-white rounded-rehab shadow-lg overflow-hidden flex flex-col md:flex-row items-center">
                    {patientData.proximasCitas > 0 ? (
                        /* Text container */
                        <div className="p-8 flex-1">
                            <h2 className="text-2xl font-semibold mb-2">¿Cuándo nos vemos?</h2>
                            <p className="text-rehab-light/80 mb-6">Tienes {patientData.proximasCitas} próximas citas con tu fisioterapeuta.</p>
                            <button className="bg-rehab-primary hover:bg-rehab-primary/90 text-white font-bold px-6 py-2 rounded-lg transition-all">
                                Ver citas
                            </button>
                        </div>
                    ) : (
                        <div className="p-8 flex-1">
                            <p className="text-rehab-light/80 mb-6">Actualmente no tienes citas programadas.</p>
                        </div>
                    )}
                    {/* Image container */}
                    <div className="w-full md:w-1/3 h-48 md:h-full min-h-[200px] relative">
                        <img
                            src={iconCalendar}
                            alt="Icono de calendario"
                            className="absolute inset-0 w-full h-full object-cover opacity-80 hover:opacity-100 transition-opacity duration-500"
                        />
                        {/* A gradient to blend the image with the dark background */}
                        <div className="absolute inset-0 bg-gradient-to-t md:bg-gradient-to-l from-rehab-dark/0 to-rehab-dark" />
                    </div>
                </div>
                {/*Pain Registry section */}
                <div className="mt-10 mb-10 bg-rehab-dark text-white rounded-rehab shadow-lg overflow-hidden flex flex-col md:flex-row items-center">
                    <div className="p-8 flex-1">
                        <h2 className="text-2xl font-semibold mb-2">¿Cómo te sientes hoy?</h2>
                        <p className="text-rehab-light/80 mb-6">Lleva un registro de tu dolor para poder ajustar tu tratamiento.</p>
                        <button className="bg-rehab-primary hover:bg-rehab-primary/90 text-white font-bold px-6 py-2 rounded-lg transition-all">
                            Realizar registro
                        </button>
                    </div>
                    {/* Image container */}
                    <div className="w-full md:w-1/3 h-48 md:h-full min-h-[200px] relative">
                        <img
                            src={iconPain}
                            alt="Imagen de dolor"
                            className="absolute inset-0 w-full h-full object-cover opacity-80 hover:opacity-100 transition-opacity duration-500"
                        />
                        {/* A gradient to blend the image with the dark background */}
                        <div className="absolute inset-0 bg-gradient-to-t md:bg-gradient-to-l from-rehab-dark/0 to-rehab-dark" />
                    </div>
                </div>

                {/*Logo of the web*/}
                <div className="flex justify-center my-10">
                    <img
                        src={logo}
                        alt="Logo de Rehab & Move"
                        className="h-16"
                    />
                </div>

                {/* Footer */}
                <footer className="text-center mt-10 text-sm text-gray-500">
                    &copy; 2026 Rehab & Move. Todos los derechos reservados.
                </footer>
            </div>

        </div >
    )

};

export default PatientDashboard;