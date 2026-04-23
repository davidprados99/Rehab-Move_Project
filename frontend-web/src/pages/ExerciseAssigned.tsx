import React, { useState, useEffect } from 'react';
import '../index.css';
import ExerciseCard from '../components/ExerciseCard';
import { PatientService } from '../services/patient.service';
import { type ExerciseDone, type ExerciseAssignment } from '../models/Exercise';


const ExerciseAssigned: React.FC = () => {
    // State to hold assigned exercises and exercises done today
    const [exercisesAssigned, setExercisesAssigned] = useState<ExerciseAssignment[]>([]);
    const [exerciseDoneToday, setExerciseDoneToday] = useState<ExerciseDone[]>([]);
    const [, setLoading] = useState(true);

    // Get user ID from local storage
    const userId = localStorage.getItem('user_id');

    // Function to handle marking an exercise as done
    const handleMarkAsDone = async (idAssignment: number) => {
        try {
            // Call the service to mark the exercise as done
            await PatientService.markExerciseAsDone(idAssignment);

            // Update local state to reflect the change immediately without needing to refetch from the server
            const newDone = {id_assignment: idAssignment, done_date: new Date().toISOString(), id_done: 0};

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
        <div className = "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 p-4">
            {exercisesAssigned.map((assignment) => {
                {/* Check if the current assignment is marked as done today */}
                const isDone = exerciseDoneToday.some(done => done.id_assignment === assignment.id_assignment);
                return (
                    <ExerciseCard 
                        key={assignment.id_assignment}
                        name={assignment.exercise!.name}
                        description={assignment.exercise!.description}
                        video_url={assignment.exercise!.video_url!}
                        isCompleted={isDone}
                        onButtonClick={() => handleMarkAsDone(assignment.id_assignment)}
                    />
                );
            })}
        </div>
    );
}

export default ExerciseAssigned;