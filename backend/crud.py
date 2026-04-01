from datetime import date

from sqlalchemy.orm import Session
from backend.security import get_password_hash
from backend import models, schemas

# crud.py contains the functions that interact with the database using SQLAlchemy ORM. These functions are used in the API endpoints to perform operations like creating, reading, updating, and deleting records in the database.

# --- CRUD functions for Physio ---

def get_physio_by_id(db: Session, id_physio: int):
    return db.query(models.Physio).filter(models.Physio.id_physio == id_physio).first()

def get_physio_by_email(db: Session, email: str):
    return db.query(models.Physio).filter(models.Physio.mail == email).first()

def get_physios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Physio).offset(skip).limit(limit).all()

def create_physio(db: Session, physio: schemas.PhysioCreate):
    
    #Check if a physio with the same email already exists to avoid duplicates
    db_physio = get_physio_by_email(db, email=physio.mail)
    if db_physio:
        raise ValueError("A physio with this email already exists.")
    
    hashed_password = get_password_hash(physio.password) # Hash the password for security reasons

    db_physio = models.Physio(
        name=physio.name,
        surnames=physio.surnames,
        mail=physio.mail,
        password=hashed_password
    )
    db.add(db_physio)
    db.commit()
    db.refresh(db_physio)
    return db_physio

def update_physio(db: Session, id: int, physio_update: schemas.PhysioUpdate):
    db_physio = get_physio_by_id(db, id_physio=id)

    if not db_physio:
        raise ValueError("Physio not found.")

    #Check if the email is being updated and if the new email is not already taken by another physio
    if physio_update.mail is not None and physio_update.mail != db_physio.mail:
        existing_physio = get_physio_by_email(db, email=physio_update.mail)
        if existing_physio:
            raise ValueError("A physio with this email already exists.")
    
    update_data = physio_update.model_dump(exclude_unset=True) # Convert the Pydantic model to a dictionary, excluding fields that were not provided in the update request
    
    for key, value in update_data.items():
            if key == "password": # If the password is being updated, hash it before storing
                value = get_password_hash(value)
            setattr(db_physio, key, value)

    db.commit()
    db.refresh(db_physio)
    return db_physio

def delete_physio(db: Session, id_physio: int):
    db_physio = get_physio_by_id(db, id_physio=id_physio)
    if not db_physio:
        raise ValueError("Physio not found.")
    
    db.delete(db_physio)
    db.commit()
    return {"message": "Physio deleted successfully."}


# --- CRUD functions for Patient---

def get_patient_by_id(db: Session, id_patient: int):
    return db.query(models.Patient).filter(models.Patient.id_patient == id_patient).first()

def get_patient_by_email(db: Session, email: str):
    return db.query(models.Patient).filter(models.Patient.mail == email).first()

def get_patients_by_physio(db: Session, id_physio: int, skip: int = 0, limit: int = 100):
    return db.query(models.Patient).filter(models.Patient.id_physio == id_physio).offset(skip).limit(limit).all()

def get_patients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Patient).offset(skip).limit(limit).all()

def create_patient(db: Session, patient: schemas.PatientCreate):

    if patient.id_physio is not None:
        physio = get_physio_by_id(db, id_physio=patient.id_physio)
        if not physio:
            raise ValueError("Physio not found.")
        
    #Check if a patient with the same email already exists to avoid duplicates
    db_patient = get_patient_by_email(db, email=patient.mail)
    if db_patient:
        raise ValueError("A patient with this email already exists.")
    
    hashed_password = get_password_hash(patient.password) # Hash the password for security reasons

    db_patient = models.Patient(
        name=patient.name,
        surnames=patient.surnames,
        mail=patient.mail,
        password=hashed_password,
        id_physio=patient.id_physio
    )
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

def update_patient(db: Session, id_patient: int, patient_update: schemas.PatientUpdate):
    db_patient = get_patient_by_id(db, id_patient=id_patient)

    if not db_patient:
        raise ValueError("Patient not found.")
    
    #Check if the email is being updated and if the new email is not already taken by another patient
    if patient_update.mail is not None and patient_update.mail != db_patient.mail:
        existing_patient = get_patient_by_email(db, email=patient_update.mail)
        if existing_patient:
            raise ValueError("A patient with this email already exists.")
            
    update_data = patient_update.model_dump(exclude_unset=True) 

    for key, value in update_data.items():
            if key == "password": # If the password is being updated, hash it before storing
                value = get_password_hash(value)
            setattr(db_patient, key, value)

    db.commit()
    db.refresh(db_patient)
    return db_patient

def delete_patient(db:Session, id_patient: int):
    db_patient = get_patient_by_id(db, id_patient=id_patient)
    if not db_patient:
        raise ValueError("Patient not found.")
    db.delete(db_patient)
    db.commit()
    return {"message": "Patient deleted successfully."}


# --- CRUD functions for pain records ---

def create_pain_record(db: Session, pain_record: schemas.PainRecordCreate):

    if pain_record.id_patient is not None:
        patient = get_patient_by_id(db, id_patient=pain_record.id_patient)
        if not patient:
            raise ValueError("Patient not found.")
        
    db_pain_record = models.PainRecord(
        level_pain=pain_record.level_pain,
        comment=pain_record.comment,
        id_patient=pain_record.id_patient
    )
    db.add(db_pain_record)
    db.commit()
    db.refresh(db_pain_record)
    return db_pain_record

def get_pain_records_by_patient(db: Session, id_patient: int, skip: int = 0, limit: int = 100):
    return db.query(models.PainRecord).filter(
        models.PainRecord.id_patient == id_patient).order_by(models.PainRecord.date.desc()
        ).offset(skip).limit(limit).all()

def get_pain_record_by_id(db: Session, id_pain_record: int):
    return db.query(models.PainRecord).filter(models.PainRecord.id_pain_record == id_pain_record).first()

def update_pain_record(db: Session, id_pain_record: int, pain_record_update: schemas.PainRecordUpdate):
    db_pain_record = db.query(models.PainRecord).filter(models.PainRecord.id_pain_record == id_pain_record).first()
    if not db_pain_record:
        raise ValueError("Pain record not found.")
    
    update_data = pain_record_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_pain_record, key, value)

    db.commit()
    db.refresh(db_pain_record)
    return db_pain_record

def delete_pain_record(db: Session, id_pain_record: int):
    db_pain_record = db.query(models.PainRecord).filter(models.PainRecord.id_pain_record == id_pain_record).first()
    if not db_pain_record:
        raise ValueError("Pain record not found.")
    
    db.delete(db_pain_record)
    db.commit()
    return {"message": "Pain record deleted successfully."}


# --- CRUD functions for appointments ---

def get_appointments_by_physio(db: Session, id_physio: int, date_filter: date = None):
    query = db.query(models.Appointment).filter(models.Appointment.id_physio == id_physio)
    if date_filter:
        query = query.filter(models.Appointment.date == date_filter)
    return query.all()

def get_appointments_by_patient(db: Session, id_patient: int, date_filter: date = None):
    query = db.query(models.Appointment).filter(models.Appointment.id_patient == id_patient)
    if date_filter:
        query = query.filter(models.Appointment.date == date_filter)
    return query.all()

def get_appointment_by_id(db: Session, id_appointment: int):
    return db.query(models.Appointment).filter(models.Appointment.id_appointment == id_appointment).first()

def create_appointment(db: Session, appointment: schemas.AppointmentCreate):
    if appointment.id_patient is not None:
        patient = get_patient_by_id(db, id_patient=appointment.id_patient)
        if not patient:
            raise ValueError("Patient not found.")
    
    if appointment.id_physio is not None:
        physio = get_physio_by_id(db, id_physio=appointment.id_physio)
        if not physio:
            raise ValueError("Physio not found.")
    
    db_appointment = models.Appointment(
        date=appointment.date,
        notes=appointment.notes,
        id_patient=appointment.id_patient,
        id_physio=appointment.id_physio
    )
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

def update_appointment(db: Session, id_appointment: int, appointment_update: schemas.AppointmentUpdate):
    db_appointment = db.query(models.Appointment).filter(models.Appointment.id_appointment == id_appointment).first()
    if not db_appointment:
        raise ValueError("Appointment not found.")
    
    update_data = appointment_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_appointment, key, value)

    db.commit()
    db.refresh(db_appointment)
    return db_appointment

def delete_appointment(db: Session, id_appointment: int):
    db_appointment = db.query(models.Appointment).filter(models.Appointment.id_appointment == id_appointment).first()
    if not db_appointment:
        raise ValueError("Appointment not found.")
    
    db.delete(db_appointment)
    db.commit()
    return {"message": "Appointment deleted successfully."}


# --- CRUD functions for exercises ---


def get_exercises(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Exercise).filter(models.Exercise.active == True).offset(skip).limit(limit).all()

def get_exercise_by_id(db: Session, id_exercise: int):
    return db.query(models.Exercise).filter(models.Exercise.id_exercise == id_exercise).first()

def create_exercise(db: Session, exercise: schemas.ExerciseCreate):
    db_exercise = models.Exercise(
        name=exercise.name,
        description=exercise.description,
        video_url=exercise.video_url,
        active=exercise.active
    )
    db.add(db_exercise)
    db.commit()
    db.refresh(db_exercise)
    return db_exercise

def update_exercise(db: Session, id_exercise: int, exercise_update: schemas.ExerciseUpdate):
    db_exercise = db.query(models.Exercise).filter(models.Exercise.id_exercise == id_exercise).first()
    if not db_exercise:
        raise ValueError("Exercise not found.")
    
    update_data = exercise_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_exercise, key, value)

    db.commit()
    db.refresh(db_exercise)
    return db_exercise

def activate_exercise(db: Session, id_exercise: int):
    db_exercise = db.query(models.Exercise).filter(models.Exercise.id_exercise == id_exercise).first()
    if not db_exercise:
        raise ValueError("Exercise not found.")
    
    db_exercise.active = True
    db.commit()
    db.refresh(db_exercise)
    return db_exercise

def inactivate_exercise(db: Session, id_exercise: int):
    db_exercise = db.query(models.Exercise).filter(models.Exercise.id_exercise == id_exercise).first()
    if not db_exercise:
        raise ValueError("Exercise not found.")
    
    db_exercise.active = False
    db.commit()
    db.refresh(db_exercise)
    return db_exercise

def delete_exercise(db: Session, id_exercise: int):
    db_exercise = db.query(models.Exercise).filter(models.Exercise.id_exercise == id_exercise).first()
    if not db_exercise:
        raise ValueError("Exercise not found.")
    
    db.delete(db_exercise)
    db.commit()
    return {"message": "Exercise deleted successfully."}


# --- CRUD functions for exercises assignments ---


def assign_exercise_to_patient(db: Session, assignment: schemas.ExerciseAssignmentCreate):
    if assignment.start_date > assignment.end_date:
        raise ValueError("Start date cannot be after end date.")
    
    if assignment.weekly_frequency < 1 or assignment.weekly_frequency > 7:
        raise ValueError("Weekly frequency must be between 1 and 7.")
    
    if assignment.id_exercise is not None:
        exercise = get_exercise_by_id(db, id_exercise=assignment.id_exercise)
        if not exercise:
            raise ValueError("Exercise not found.")
        
    if assignment.id_patient is not None:
        patient = get_patient_by_id(db, id_patient=assignment.id_patient)
        if not patient:
            raise ValueError("Patient not found.")
        
    db_assignment = models.ExerciseAssignment(
        weekly_frequency=assignment.weekly_frequency,
        series=assignment.series,
        repetitions=assignment.repetitions,
        start_date=assignment.start_date,
        end_date=assignment.end_date,
        id_patient=assignment.id_patient,
        id_exercise=assignment.id_exercise
        )
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment

def get_exercise_assignments_by_patient(db: Session, id_patient: int, skip: int = 0, limit: int = 100):
    return db.query(models.ExerciseAssignment).filter(models.ExerciseAssignment.id_patient == id_patient).offset(skip).limit(limit).all()

def get_exercise_assignments_by_exercise(db: Session, id_exercise: int, skip: int = 0, limit: int = 100):
    return db.query(models.ExerciseAssignment).filter(models.ExerciseAssignment.id_exercise == id_exercise).offset(skip).limit(limit).all()

def get_exercise_assignment_by_id(db: Session, id_assignment: int):
    return db.query(models.ExerciseAssignment).filter(models.ExerciseAssignment.id_assignment == id_assignment).first()

def update_exercise_assignment(db: Session, id_assignment: int, assignment_update: schemas.ExerciseAssignmentUpdate):
    db_assignment = db.query(models.ExerciseAssignment).filter(models.ExerciseAssignment.id_assignment == id_assignment).first()
    if not db_assignment:
        raise ValueError("Exercise assignment not found.")
    
    update_data = assignment_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_assignment, key, value)

    db.commit()
    db.refresh(db_assignment)
    return db_assignment

def delete_exercise_assignment(db: Session, id_assignment: int):
    db_assignment = db.query(models.ExerciseAssignment).filter(models.ExerciseAssignment.id_assignment == id_assignment).first()
    if not db_assignment:
        raise ValueError("Exercise assignment not found.")
    
    db.delete(db_assignment)
    db.commit()
    return {"message": "Exercise assignment deleted successfully."}


# --- CRUD functions for exercises done---

def get_exercise_done_by_assignment(db: Session, id_assignment: int):
    return db.query(models.ExerciseDone).filter(models.ExerciseDone.id_assignment == id_assignment).all()   

def get_exercise_done_by_id(db: Session, id_exercise_done: int):
    return db.query(models.ExerciseDone).filter(models.ExerciseDone.id_exercise_done == id_exercise_done).first()

def mark_exercise_done(db: Session, exercise_done: schemas.ExerciseDoneCreate):

    if exercise_done.id_assignment is not None:
        assignment = get_exercise_assignment_by_id(db, id_assignment=exercise_done.id_assignment)
        if not assignment:
            raise ValueError("Exercise assignment not found.")
    
    db_exercise_done = models.ExerciseDone(
        date=exercise_done.date,
        id_assignment=exercise_done.id_assignment
    )
    db.add(db_exercise_done)
    db.commit()
    db.refresh(db_exercise_done)
    return db_exercise_done

def delete_exercise_done(db: Session, id_exercise_done: int):
    db_exercise_done = db.query(models.ExerciseDone).filter(models.ExerciseDone.id_exercise_done == id_exercise_done).first()
    if not db_exercise_done:
        raise ValueError("Exercise done record not found.")
    
    db.delete(db_exercise_done)
    db.commit()
    return {"message": "Exercise done record deleted successfully."}

def update_exercise_done(db: Session, id_exercise_done: int, exercise_done_update: schemas.ExerciseDoneUpdate):
    db_exercise_done = db.query(models.ExerciseDone).filter(models.ExerciseDone.id_exercise_done == id_exercise_done).first()
    if not db_exercise_done:
        raise ValueError("Exercise done record not found.")
    
    update_data = exercise_done_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_exercise_done, key, value)

    db.commit()
    db.refresh(db_exercise_done)
    return db_exercise_done