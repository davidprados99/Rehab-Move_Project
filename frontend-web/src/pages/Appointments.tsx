import React, { useState, useEffect } from "react";
import Calendar from 'react-calendar';
import 'react-calendar/dist/Calendar.css';
import '../index.css';
import { PatientService } from '../services/patient.service';
import type { Appointment } from '../models/Clinical';

const Appointments: React.FC = () => {
    // State to hold appointments, selected date, and loading status
    const [appointments, setAppointments] = useState<Appointment[]>([]);
    const [selectedDate, setSelectedDate] = useState(new Date());
    const [loading, setLoading] = useState(true);

    // Get user ID from localStorage
    const userId = localStorage.getItem('user_id');

    // Type for Calendar's onChange value
    type CalendarValuePiece = Date | Date[] | null;
    type CalendarValue = CalendarValuePiece | [CalendarValuePiece, CalendarValuePiece];

    // Handle date change from the calendar
    const handleDateChange = (value: CalendarValue) => {
        if (value instanceof Date) {
            setSelectedDate(value);
        } else if (Array.isArray(value) && value[0] instanceof Date) {
            setSelectedDate(value[0]);
        }
    };

    // Fetch appointments when component mounts or userId changes
    useEffect(() => {
        const fetchAppointments = async () => {
            try {
                setLoading(true);
                const appointmentsData = await PatientService.getAppointments(Number(userId));
                setAppointments(appointmentsData);
            }
            catch (error) {
                console.error('Error fetching patient data:', error);
            }
            finally {
                setLoading(false);
            }
        };
        fetchAppointments();
    }, [userId]);

    // Function to filter appointments for the selected date
    const getAppointmentsForDate = (date: Date) => {
        return appointments.filter(app => {
            const appDate = new Date(app.date);
            return appDate.toDateString() === date.toDateString();
        });
    };

    if (loading) {
        return <div className="p-10 text-rehab-dark">Cargando tus citas...</div>;
    }
    // Get appointments for the currently selected date
    const appointmentsDay = getAppointmentsForDate(selectedDate);

    return (
        <div className="min-h-screen bg-gray-50 w-full grid place-items-center">
            <div className="max-w-5xl max-h-5xl w-full h-full grid md:grid-cols-2 gap-8 p-6">

                {/* Left column: Calendar */}
                <div className="bg-white rounded-2xl shadow-sm border-t-4 border-rehab-primary p-6 h-fit sticky top-6">
                    <h1 className="text-2xl font-bold text-rehab-dark mb-6">Mis Citas</h1>
                    <div className="bg-white rounded-2xl shadow-sm border-gray-100 justify-center p-4">
                        <Calendar
                            onChange={handleDateChange}
                            value={selectedDate}
                            tileContent={({ date, view }: { date: Date; view: string }) => {
                                if (view === 'month' && getAppointmentsForDate(date).length > 0) {
                                    return (<div className="flex justify-center">
                                        <div className="h-2 w-2 bg-rehab-primary rounded-full mt-1"></div>
                                    </div>);
                                }
                                return null;
                            }}
                        />
                    </div>
                </div>

                {/* Right column: Details of selected date's appointments */}
                <div className="bg-white rounded-2xl shadow-sm border-t-4 border-rehab-primary p-6 h-fit sticky top-6">
                    <h2 className="text-2xl font-bold text-rehab-dark mb-6">
                        {selectedDate.toLocaleDateString('es-ES', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}
                    </h2>
                    {loading ? (
                        <p className="text-rehab-dark">Cargando citas...</p>
                    ) : appointmentsDay.length > 0 ? (
                        appointmentsDay.map((app, index) => (
                            <div key={index} className="mb-4 p-4 border border-gray-100 rounded-xl bg-rehab-light/50">
                                <p className="text-rehab-dark font-semibold text-sm mb-2">Fisioterapeuta: {app.physio.name} {app.physio.surnames}</p>
                                <p className="text-rehab-dark text-xs mb-1">Hora: {new Date(app.date).toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' })}</p>
                                <p className="text-rehab-dark opacity-90 text-xs italic">Comentarios: {app.notes ? app.notes : 'Sin notas'}</p>
                            </div>
                        ))
                        ) : (
                            <div className="flex flex-col items-left h-full">
                                <p className="text-rehab-dark">No tienes citas para este día.</p>
                            </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Appointments;