import api from './api';
import type { ExerciseAssignment } from '../models/Exercise';
import type { Appointment } from '../models/Clinical';
import type { PainRecord } from '../models/Clinical';
import type { ExerciseDone } from '../models/Exercise';

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

    getExerciseDoneToday: async (patientId: number): Promise<ExerciseDone[]> => {
        try {
            const response = await api.get(`/exercises_done/patient/${patientId}/today`);
            return response.data;
        } catch (error) {
            console.error('Error fetching exercises done today:', error);
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
    //Get pain records of a patient
    getPainRecords: async (patientId: number): Promise<PainRecord[]> => {
        try {
            const response = await api.get(`/pain_records/patient/${patientId}`);
            return response.data;
        } catch (error) {
            console.error('Error fetching pain records:', error);
            throw error;
        }
    },
    
    //Registry pain of a patient
    postRegistryPain: async (patientId: number, painLevel: number, comment?: string): Promise<PainRecord> => {
        try {
            const response = await api.post(`/pain_records`, {
                level_pain: painLevel,
                comment: comment || '',
                id_patient: patientId
            });
            return response.data;
        } catch (error) {
            console.error('Error posting pain registry:', error);
            throw error;
        }
    },

    markExerciseAsDone: async (assignmentId: number): Promise<ExerciseDone> => {
        try {
            const response = await api.post(`/exercises_done`, {
                id_assignment: assignmentId,
                done_date: new Date().toISOString()
            });
            return response.data;
        } catch (error) {
            console.error('Error marking exercise as done:', error);
            throw error;
        }
    }

};