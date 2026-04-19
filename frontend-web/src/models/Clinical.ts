export type AppointmentState = 'pendiente' | 'completado' | 'cancelado';

export interface Appointment {
    id_appointment: number;
    state: AppointmentState;
    date: string;
    notes?: string;
    id_patient: number;
    id_physio: number;
}

export interface PainRecord {
    id_pain_record: number;
    level_pain: number;
    record_date: string;
    comment?: string;
    id_patient: number;
}