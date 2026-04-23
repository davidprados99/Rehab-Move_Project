export interface Exercise {
    id_exercise: number;
    name: string;
    description: string;
    video_url: string;
    active: boolean;
}

export interface ExerciseAssignment {
    id_assignment: number;
    weekly_frequency: number;
    series: number;
    repetitions: number;
    start_date: string;
    end_date: string;
    id_patient: number;
    id_exercise: number;
    exercise?: Exercise;
}

export interface ExerciseDone {
    id_done: number;
    done_date: string;
    id_assignment: number;
}