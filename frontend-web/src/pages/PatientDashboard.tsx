import React from 'react';
import '../index.css';
import exerciseImage from '../assets/ejercicio.jpg';
import iconCalendar from '../assets/iconoCalendario.webp';
import iconPain from '../assets/dolorFoto.jpg';
import logo from '../assets/logo_Rehab_Move.png';
import DashboardCard from '../components/DashboardCard';

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
                {patientData.tieneEjercicios ? (
                    <DashboardCard
                        title="¡A por ello!"
                        description="Tienes ejercicios asignados por tu fisioterapeuta."
                        buttonText="Ver ejercicios"
                        imageSrc={exerciseImage}
                        imageAlt="Persona haciendo ejercicio"
                        className="mb-10"
                    />
                ): (
                    <DashboardCard
                        title= "No hay ejercicios asignados."
                        description= "Ponte en contacto con tu fisioterapeuta para que te asigne ejercicios personalizados."
                        imageSrc={exerciseImage}
                        imageAlt="Persona haciendo ejercicio"
                        className="mb-10"
                    />
                )}

                {/* Upcoming appointments section */}
                {patientData.proximasCitas > 0 ? (
                    <DashboardCard
                        title="¿Cuándo nos vemos?"
                        description={`Tienes ${patientData.proximasCitas} próximas citas con tu fisioterapeuta.`}
                        buttonText="Ver citas"
                        imageSrc={iconCalendar}
                        imageAlt="Icono de calendario"
                        className="mb-10"
                    />
                ) : (
                    <DashboardCard
                        title="No tienes citas próximas."
                        description="Ponte en contacto con tu fisioterapeuta para programar tus próximas citas."
                        imageSrc={iconCalendar}
                        imageAlt="Icono de calendario"
                        className="mb-10"
                    />
                )}
                {/*Pain Registry section */}
                <DashboardCard
                    title="Cuéntanos cómo te sientes"
                    description="Lleva un seguimiento de tu dolor para poder ajustar tu tratamiento."
                    buttonText="Registrar dolor"
                    imageSrc={iconPain}
                    imageAlt="Icono de dolor"
                />

                {/* Footer */}
                <footer className="text-center mt-10 text-sm text-gray-500">
                    &copy; 2026 Rehab & Move. Todos los derechos reservados.
                </footer>
            </div>

        </div >
    )

};

export default PatientDashboard;