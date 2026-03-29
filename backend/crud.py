from datetime import date

from sqlalchemy.orm import Session
from backend.security import get_password_hash
from backend import models, schemas

# crud.py contains the functions that interact with the database using SQLAlchemy ORM. These functions are used in the API endpoints to perform operations like creating, reading, updating, and deleting records in the database.

# --- CRUD functions for Physio ---

def get_physio_by_email(db: Session, email: str):
    return db.query(models.Physio).filter(models.Physio.mail == email).first()

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


# --- CRUD functions for Patient---

def get_patients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Patient).offset(skip).limit(limit).all()

def get_patient_by_email(db: Session, email: str):
    return db.query(models.Patient).filter(models.Patient.mail == email).first()

def create_patient(db: Session, patient: schemas.PatientCreate):

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


# --- CRUD functions for pain records ---

def create_pain_record(db: Session, pain_record: schemas.PainRecordCreate):
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


# --- CRUD functions for appointments ---

def get_appointments_by_physio(db: Session, id_physio: int, date_filter: date = None):
    query = db.query(models.Appointment).filter(models.Appointment.id_physio == id_physio)
    if date_filter:
        query = query.filter(models.Appointment.date == date_filter)
    return query.all()

def update_appointment_status(db: Session, id_appointment: int, new_status: models.AppointmentState):
    appointment = db.query(models.Appointment).filter(models.Appointment.id_appointment == id_appointment).first()
    if appointment:
        appointment.state = new_status.value
        db.commit()
        db.refresh(appointment)
    return appointment

# --- CRUD functions for exercises ---

def get_exercises(db: Session):
    return db.query(models.Exercise).filter(models.Exercise.active == True).all()

def assign_exercise_to_patient(db: Session, assigment: schemas.ExerciseAssignmentCreate):
    db_assigment = models.ExerciseAssignment(
        weekly_frequency=assigment.weekly_frequency,
        series=assigment.series,
        repetitions=assigment.repetitions,
        start_date=assigment.start_date,
        end_date=assigment.end_date,
        id_patient=assigment.id_patient,
        id_exercise=assigment.id_exercise
        )
    db.add(db_assigment)
    db.commit()
    db.refresh(db_assigment)
    return db_assigment
