import api from './api';
import type { ExerciseAssignment } from '../models/Exercise';
import type { Appointment } from '../models/Clinical';
import type { PainRecord } from '../models/Clinical';

export const PatientService = {

    //Get exercises assigned to a patient
    getAssignedExercises: async (patientId: number): Promise<ExerciseAssignment[]> => {
        try {
            const response = await api.get(`/assignments/patient/${patientId}`);
            return response.data;
        } catch (error) {
            console.error('Error fetching assigned exercises:', error);
            throw error;
        }
    },

    //Get appointments of a patient
    getAppointments: async (patientId: number): Promise<Appointment[]> => {
        try {
            const response = await api.get(`/appointments/patient/${patientId}`);
            return response.data;
        } catch (error) {
            console.error('Error fetching appointments:', error);
            throw error;
        }
    },

    //Registry pain of a patient
    postRegistryPain: async (patientId: number, painLevel: number, comment: string): Promise<PainRecord> => {
        try {
            const response = await api.post(`/pain-records`, {
                painLevel,
                comment,
                record_date: new Date().toISOString(),
                patientId
            });
            return response.data;
        } catch (error) {
            console.error('Error posting pain registry:', error);
            throw error;
        }
    }
};