import React, { useState, useEffect } from 'react';
import '../index.css';
import ExerciseCard from '../components/ExerciseCard';
import { PatientService } from '../services/patient.service';
import { type ExerciseDone, type ExerciseAssignment } from '../models/Exercise';
import Swal from 'sweetalert2';


const ExerciseAssigned: React.FC = () => {
    // State to hold assigned exercises and exercises done today
    const [exercisesAssigned, setExercisesAssigned] = useState<ExerciseAssignment[]>([]);
    const [exerciseDoneToday, setExerciseDoneToday] = useState<ExerciseDone[]>([]);
    const [, setLoading] = useState(true);

    // Get user ID from local storage
    const userId = localStorage.getItem('user_id');

    // Function to handle marking an exercise as done
    const handleMarkAsDone = async (idAssignment: number) => {
        const result = await Swal.fire({
            title: '¿Ejercicio terminado?',
            text: "Se avisará a tu fisioterapeuta de tu progreso.",
            icon: 'question',
            showCancelButton: true,
            confirmButtonColor: '#3085d6', 
            cancelButtonColor: '#d33',
            confirmButtonText: 'Sí, terminado',
            cancelButtonText: 'No, aún no'
        });
        if (!result.isConfirmed) {
            return;
        }
        try {
            // Call the service to mark the exercise as done
            await PatientService.markExerciseAsDone(idAssignment);

            // Update local state to reflect the change immediately without needing to refetch from the server
            const newDone = { id_assignment: idAssignment, done_date: new Date().toISOString(), id_done: 0 };

            // Add the new done exercise to the state with a callback to ensure we have the latest state
            setExerciseDoneToday(prev => [...prev, newDone]);

        } catch (error) {
            console.error('Error marking exercise as done:', error);
        }
    };

    // Fetch assigned exercises and exercises done today on component mount
    useEffect(() => {
        const fetchData = async () => {
            try {
                // Fetch both assigned exercises and exercises done today in parallel
                setLoading(true);
                const [exercisesData, exerciseDoneData] = await Promise.all([
                    PatientService.getAssignedExercises(Number(userId)),
                    PatientService.getExerciseDoneToday(Number(userId))
                ]);
                // Update state with fetched data
                setExercisesAssigned(exercisesData);
                setExerciseDoneToday(exerciseDoneData || []);
            } catch (error) {
                console.error('Error fetching patient data:', error);
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    },
        [userId]);

    return (
        <div className="min-h-screen bg-gray-50 w-full">
            <div className="max-w-4xl mx-auto grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-20 p-6">
                {exercisesAssigned.map((assignment) => {
                    {/* Check if the current assignment is marked as done today */ }
                    const isDone = exerciseDoneToday.some(done => done.id_assignment === assignment.id_assignment);
                    return (
                        <ExerciseCard
                            key={assignment.id_assignment}
                            name={assignment.exercise!.name}
                            description={assignment.exercise!.description}
                            weekly_frequency={assignment.weekly_frequency}
                            series={assignment.series}
                            repetitions={assignment.repetitions}
                            start_date={assignment.start_date}
                            end_date={assignment.end_date}
                            video_url={assignment.exercise!.video_url!}
                            isCompleted={isDone}
                            onButtonClick={() => handleMarkAsDone(assignment.id_assignment)}
                        />
                    );
                })}
            </div></div>
    );
}

export default ExerciseAssigned;