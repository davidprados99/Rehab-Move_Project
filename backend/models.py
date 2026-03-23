import enum

from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, Text, Boolean, CheckConstraint
from sqlalchemy.orm import relationship
from database import Base
import datetime

# Models.py define how the data will be stored in the database using SQLAlchemy ORM.

# Class of the database
class Physio(Base):
    __tablename__ = "physio"
    id_physio = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    surnames = Column(String(100), nullable=False)
    mail = Column(String(150), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(50), default="physio")

    # Relation with the other tables we use back_populates to create a bidirectional relationship
    patients = relationship("Patient", back_populates="assigned_physio")
    appointments = relationship("Appointment", back_populates="physio")


class Patient(Base):
    __tablename__ = "patient"
    id_patient = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    surnames = Column(String(100), nullable=False)
    mail = Column(String(150), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    start_date = Column(Date, default=datetime.date.today)
    role = Column(String(50), default="patient")
    id_physio = Column(Integer, ForeignKey("physio.id_physio", ondelete="SET NULL"))

    assigned_physio = relationship("Physio", back_populates="patients")
    appointments = relationship("Appointment", back_populates="patient")
    pain_records = relationship("PainRecord", back_populates="patient")
    assignments = relationship("ExerciseAssignment", back_populates="patient")


class Appointment(Base):
    __tablename__ = "appointment"
    id_appointment = Column(Integer, primary_key=True, index=True)
    state = Column(String(50), default="pendiente")
    date = Column(DateTime, nullable=False)
    notes = Column(Text)
    id_patient = Column(Integer, ForeignKey("patient.id_patient", ondelete="CASCADE"))
    id_physio = Column(Integer, ForeignKey("physio.id_physio", ondelete="CASCADE"))

    
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

    
    patient = relationship("Patient", back_populates="pain_records")
    __table_args__ = (CheckConstraint('level_pain >= 0 AND level_pain <= 10'),)


class Exercise(Base):
    __tablename__ = "exercise"
    id_exercise = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    description = Column(Text)
    video_url = Column(String(255))
    active = Column(Boolean, default=True)

    
    assignments = relationship("ExerciseAssignment", back_populates="exercise")


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

    
    patient = relationship("Patient", back_populates="assignments")
    exercise = relationship("Exercise", back_populates="assignments")
    completions = relationship("ExerciseDone", back_populates="assignment")


class ExerciseDone(Base):
    __tablename__ = "exercise_done"
    id_done = Column(Integer, primary_key=True, index=True)
    done_date = Column(DateTime, default=datetime.datetime.utcnow)
    id_assignment = Column(Integer, ForeignKey("exercise_assignment.id_assignment", ondelete="CASCADE"))

    
    assignment = relationship("ExerciseAssignment", back_populates="completions")