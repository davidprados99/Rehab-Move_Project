import React, { useRef, useEffect, useState } from "react";
import '../index.css';
import { PatientService } from '../services/patient.service';
import type { PainRecord } from '../models/Clinical';
import Swal from 'sweetalert2';
import tick from '../assets/tick.png';
import RehabLoader from '../components/RehabLoading';

const PainRegistry: React.FC = () => {
    const [loading, setLoading] = useState(true);
    const [, setPainRecords] = useState<PainRecord[]>([]);
    const [painRecordToday, setPainRecordToday] = useState<PainRecord | null>(null);

    const [levelPain, setLevelPain] = useState<number>(5);
    const commentRef = useRef<HTMLTextAreaElement>(null);

    const userId = localStorage.getItem('user_id');

    const getPainColor = (level: number) => {
        if (level <= 3) return 'text-green-500';
        if (level <= 7) return 'text-yellow-500';
        return 'text-red-500';
    };

    const handleFormSubmit = (e: React.FormEvent) => {
        e.preventDefault();

        const comment = commentRef.current?.value || '';

        handleSubmitPainRecord(levelPain, comment);
    };

    // Function to fetch pain records and check for today's record
    const fetchPainRecords = async () => {
        try {
            setLoading(true);
            const records = await PatientService.getPainRecords(Number(userId));
            setPainRecords(records);
            // Check if there's a pain record for today
            const todayString = new Date().toISOString().split('T')[0];
            const todayRecord = records.find(record => record.record_date.startsWith(todayString));
            setPainRecordToday(todayRecord || null);
        } catch (error) {
            console.error('Error fetching pain records:', error);
        } finally {
            setLoading(false);
        }
    };

    // Fetch pain records on component mount and whenever the user ID changes
    useEffect(() => {
        if (userId) {
            fetchPainRecords();
        }
    }, [userId]);

    if (loading) {
        return <RehabLoader />;
    }

    const handleSubmitPainRecord = async (levelPain: number, comment?: string) => {
        // Show confirmation dialog before submitting the pain record
        const result = await Swal.fire({
            title: '¿Registrar nivel de dolor?',
            text: "Se guardará tu nivel de dolor para que tu fisioterapeuta pueda revisarlo.",
            icon: 'question',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Sí, registrar',
            cancelButtonText: 'No, cancelar'
        });
        if (!result.isConfirmed) {
            return;
        }
        try {
            // Call the service to post the pain record
            await PatientService.postRegistryPain(Number(userId), levelPain, comment);

            // Optionally, you can update the local state to reflect the new pain record without needing to refetch from the server
            const newRecord: PainRecord = {
                id_pain_record: 0,
                level_pain: levelPain,
                record_date: new Date().toISOString(),
                comment,
                id_patient: Number(userId)
            };
            // Add the new record to the state (you might want to refetch from the server instead if you need the ID or other generated fields)
            setPainRecordToday(newRecord);
            Swal.fire('¡Registrado!', 'Tu nivel de dolor ha sido registrado.', 'success');
        } catch (error) {
            console.error('Error posting pain record:', error);
            Swal.fire('Error', 'Hubo un problema al registrar tu nivel de dolor. Por favor, intenta de nuevo.', 'error');
        }
    };

    return (
        <div className="min-h-screen bg-gray-50 w-full">

            <div className="max-w-4xl mx-auto p-6">

                <header className="mt-5 mb-10 text-center">
                    <h1 className="text-3xl font-bold text-rehab-dark mb-5">Registro de dolor</h1>
                    <p className="text-lg text-rehab-dark mb-5">Aquí puedes registrar tu nivel de dolor para que tu fisioterapeuta pueda monitorear tu progreso.</p>
                </header>

                <div className="flex flex-col items-center p-4">

                    {painRecordToday ? (

                        <div className="w-full max-w-md bg-green-50 border-l-4 border-green-500 text-green-700 p-6 mb-6 rounded-xl shadow-sm">
                            <h2 className="text-lg font-bold mb-2 text-center">Registro realizado:</h2>
                            <p>Nivel de dolor: {painRecordToday.level_pain}</p>
                            {painRecordToday.comment && <p>Comentario: {painRecordToday.comment}</p>}
                            <p className="mt-4 text-xs text-green-600 opacity-75 text-center">Mañana podrás realizar un nuevo registro.</p>
                            <img src={tick} alt="Tick" className="mx-auto mt-4 w-6 h-6" />
                        </div>

                    ) : (

                        <form onSubmit={handleFormSubmit} className="bg-white rounded-2xl shadow-sm border-t-4 border-rehab-primary p-6 top-6 w-full max-w-md">
                            <h2 className="text-xl font-bold text-rehab-dark mb-6 text-center">¿Cómo te sientes hoy?</h2>

                            <div className="mb-8">
                                {/* Visualización del número grande */}
                                <div className="flex flex-col items-center mb-6">
                                    <span className={`text-6xl font-black transition-colors duration-300 ${getPainColor(levelPain)}`}>
                                        {levelPain}
                                    </span>
                                    <span className="text-gray-400 font-medium text-sm mt-2 uppercase tracking-widest"> Escala de dolor </span>
                                </div>

                                {/* El Slider */}
                                <input
                                    type="range"
                                    min="0"
                                    max="10"
                                    value={levelPain}
                                    onChange={(e) => setLevelPain(parseInt(e.target.value))}
                                    className="w-full h-3 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-rehab-primary"
                                />

                                {/* Etiquetas de ayuda */}
                                <div className="flex justify-between mt-3 text-xs font-bold text-gray-400 px-1">
                                    <span>SIN DOLOR</span>
                                    <span>MODERADO</span>
                                    <span>MÁXIMO</span>
                                </div>
                            </div>

                            <div className="mb-6">
                                <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="comment">
                                    ¿Algún comentario para tu fisio?
                                </label>
                                <textarea
                                    ref={commentRef}
                                    id="comment"
                                    className="w-full p-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-rehab-primary focus:border-transparent outline-none transition-all"
                                    rows={3}
                                    placeholder="Ej: Me ha molestado más cuando llevaba un rato sentado..."
                                ></textarea>
                            </div>

                            <button
                                type="submit"
                                className="w-full bg-rehab-primary hover:bg-rehab-primary/90 text-white font-bold py-3 rounded-xl transition-all shadow-lg active:scale-95 tracking-wider"
                            >
                                Registrar dolor diario
                            </button>
                        </form>
                    )}
                </div>
                <footer className="text-center mt-10 text-sm text-gray-500">
                    &copy; 2026 Rehab & Move. Todos los derechos reservados.
                </footer>
            </div>


        </div>
    );
};

export default PainRegistry;