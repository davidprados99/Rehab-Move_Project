import React, { useState, useEffect } from 'react';
import '../index.css';
import exerciseImage from '../assets/ejercicio.jpg';
import iconCalendar from '../assets/iconoCalendario.webp';
import iconPain from '../assets/dolorFoto.jpg';
import DashboardCard from '../components/DashboardCard';
import { useNavigate } from 'react-router-dom';
import { PatientService } from '../services/patient.service';
import type { ExerciseAssignment } from '../models/Exercise';
import type { Appointment} from '../models/Clinical';



//Use const to define the component, and React.FC for type safety
const PatientDashboard: React.FC = () => {
    const navigate = useNavigate();
    const [exercissesAssigned, setExercisesAssigned] = useState<ExerciseAssignment[]>([]);
    const [appointments, setAppointments] = useState<Appointment[]>([]);
    const [loading, setLoading] = useState(true);

    const userId = localStorage.getItem('user_id');
    const userName = localStorage.getItem('name');

    useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true);
                const [exercisesData, appointmentsData] = await Promise.all([
                    PatientService.getAssignedExercises(Number(userId)),
                    PatientService.getAppointments(Number(userId))
                ]);
                setExercisesAssigned(exercisesData);
                setAppointments(appointmentsData);
            } catch (error) {
                console.error('Error fetching patient data:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [userId]);

    // Check if there are assigned exercises and upcoming appointments
    const hasExercises = exercissesAssigned.length > 0;
    const upcomingApptsCount = appointments.filter(app => new Date(app.date) > new Date()).length;

    if (loading) {
        return <div className="p-10 text-rehab-light/80">Cargando tu recuperación...</div>;
    }

    return (

        <div className="min-h-screen bg-gray-50 w-full">
            <div className="max-w-4xl mx-auto p-6">

                {/* Welcome header */}
                <header className="mt-5 mb-10 text-center">
                    <h1 className="text-3xl font-bold text-rehab-dark mb-2">¡Hola de nuevo, {userName}!</h1>
                    <p className="text-lg text-rehab-dark">Te damos la bienvenida a tu panel de paciente.</p>
                </header>

                {/* Exercise section */}
                {hasExercises ? (
                    <DashboardCard
                        title="¡A por ello!"
                        description="Hay ejercicios asignados por tu fisioterapeuta."
                        buttonText="Ver ejercicios"
                        onButtonClick={() => navigate('/exercise-assigned')}
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
                {upcomingApptsCount > 0 ? (
                    <DashboardCard
                        title="¿Cuándo nos vemos?"
                        description={`Tienes ${upcomingApptsCount} próximas citas agendadas.`}
                        buttonText="Ver citas"
                        onButtonClick={() => navigate('/appointments')}
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
                    onButtonClick={() => navigate('/pain-registry')}
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