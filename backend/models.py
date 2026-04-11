import enum

from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, Text, Boolean, CheckConstraint
from sqlalchemy.orm import relationship
from backend.database import Base
import datetime

# Models.py define how the data will be stored in the database using SQLAlchemy ORM.

# Class of the database
class Physio(Base):
    __tablename__ = "physio"
    id_physio = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    surnames = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    phone = Column(String(20), nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(50), default="physio")

    # Relation with the other tables we use back_populates to create a bidirectional relationship
    # Father of patients and appointments, if a physio is deleted, all their patients and appointments will be deleted too (cascade delete)
    patients = relationship("Patient", back_populates="assigned_physio", cascade="all, delete-orphan", passive_deletes=True)
    appointments = relationship("Appointment", back_populates="physio", cascade="all, delete-orphan", passive_deletes=True)


class Patient(Base):
    __tablename__ = "patient"
    id_patient = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    surnames = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    phone = Column(String(20), nullable=False)
    password = Column(String(255), nullable=False)
    start_date = Column(Date, default=datetime.date.today)
    role = Column(String(50), default="patient")
    id_physio = Column(Integer, ForeignKey("physio.id_physio", ondelete="CASCADE"))

    # Son of physio, if the assigned physio is deleted, the patient will be deleted too (cascade delete)
    assigned_physio = relationship("Physio", back_populates="patients")

    # Father of appointments, pain records and exercise assignments, if a patient is deleted, all their appointments, pain records and exercise assignments will be deleted too (cascade delete)
    appointments = relationship("Appointment", back_populates="patient", cascade="all, delete-orphan", passive_deletes=True)
    pain_records = relationship("PainRecord", back_populates="patient", cascade="all, delete-orphan", passive_deletes=True)
    assignments = relationship("ExerciseAssignment", back_populates="patient", cascade="all, delete-orphan", passive_deletes=True)


class Appointment(Base):
    __tablename__ = "appointment"
    id_appointment = Column(Integer, primary_key=True, index=True)
    state = Column(String(50), default="pendiente")
    date = Column(DateTime, nullable=False)
    notes = Column(Text)
    id_patient = Column(Integer, ForeignKey("patient.id_patient", ondelete="CASCADE"))
    id_physio = Column(Integer, ForeignKey("physio.id_physio", ondelete="CASCADE"))

    # Son of both patient and physio
    patient = relationship("Patient", back_populates="appointments")
    physio = relationship("Physio", back_populates="appointments")

class AppointmentState(str, enum.Enum):
    PENDIENTE = "pendiente"
    COMPLETADO = "completado"
    CANCELADO = "cancelado"


class PainRecord(Base):
    __tablename__ = "pain_record"
    id_pain_record = Column(Integer, primary_key=True, index=True)
    level_pain = Column(Integer)
    date = Column(Date, default=datetime.date.today)
    comment = Column(Text)
    id_patient = Column(Integer, ForeignKey("patient.id_patient", ondelete="CASCADE"))

    # Son of patient, if the patient is deleted, all their pain records will be deleted too (cascade delete)
    patient = relationship("Patient", back_populates="pain_records")
    __table_args__ = (CheckConstraint('level_pain >= 0 AND level_pain <= 10'),)


class Exercise(Base):
    __tablename__ = "exercise"
    id_exercise = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    description = Column(Text)
    video_url = Column(String(255))
    active = Column(Boolean, default=True)

    # Father of exercise assignments, if an exercise is deleted, all its assignments will be deleted too (cascade delete)
    assignments = relationship("ExerciseAssignment", back_populates="exercise", cascade="all, delete-orphan", passive_deletes=True)


class ExerciseAssignment(Base):
    __tablename__ = "exercise_assignment"
    id_assignment = Column(Integer, primary_key=True, index=True)
    weekly_frequency = Column(Integer)
    series = Column(Integer)
    repetitions = Column(Integer)
    start_date = Column(Date)
    end_date = Column(Date)
    id_patient = Column(Integer, ForeignKey("patient.id_patient", ondelete="CASCADE"))
    id_exercise = Column(Integer, ForeignKey("exercise.id_exercise", ondelete="CASCADE"))

    # Son of both patient and exercise, if either is deleted, the assignment will be deleted too (cascade delete)
    patient = relationship("Patient", back_populates="assignments")
    exercise = relationship("Exercise", back_populates="assignments")
    completions = relationship("ExerciseDone", back_populates="assignment")


class ExerciseDone(Base):
    __tablename__ = "exercise_done"
    id_done = Column(Integer, primary_key=True, index=True)
    done_date = Column(DateTime, default=datetime.datetime.utcnow)
    id_assignment = Column(Integer, ForeignKey("exercise_assignment.id_assignment", ondelete="CASCADE"))

    # Son of exercise assignment, if the assignment is deleted, the completion will be deleted too (cascade delete)
    assignment = relationship("ExerciseAssignment", back_populates="completions")