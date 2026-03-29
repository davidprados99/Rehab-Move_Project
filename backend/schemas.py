from pydantic import BaseModel, EmailStr, Field
from datetime import date, datetime
from typing import List, Optional

from backend.models import AppointmentState

#Schemas.py describe how the data will be sent and received in JSON format between the frontend and backend using Pydantic.

#--- Physio Schemas ---
class PhysioBase(BaseModel):
    name: str
    surnames: str
    mail: EmailStr
    role: str = "physio"

class PhysioCreate(PhysioBase):
    password: str  # Only needed when creating a new physio

class Physio(PhysioBase):
    id_physio: int
    class Config:
        from_attributes = True # Allow Pydantic to read data from SQLAlchemy models using attributes

#--- Patient Schemas ---
class PatientBase(BaseModel):
    name: str
    surnames: str
    mail: EmailStr
    start_date: date
    id_physio: Optional[int] = None
    role: str = "patient"

class PatientCreate(PatientBase):
    password: str

class Patient(PatientBase):
    id_patient: int
    class Config:
        from_attributes = True

#--- Pain Record Schemas ---
class PainRecordBase(BaseModel):
    level_pain: int = Field(ge=0, le=10) # Validation to ensure pain level is between 0 and 10
    comment: Optional[str] = None
    record_date: date = Field(default_factory=date.today)

class PainRecordCreate(PainRecordBase):
    id_patient: int

class PainRecord(PainRecordBase):
    id_pain_record: int
    class Config:
        from_attributes = True

#--- Exercise Schemas ---
class ExerciseBase(BaseModel):
    name: str
    description: Optional[str] = None
    video_url: Optional[str] = None
    active: bool = True

class ExerciseCreate(ExerciseBase):
    pass

class Exercise(ExerciseBase):
    id_exercise: int
    class Config:
        from_attributes = True

#--- Exercise Assignment Schemas ---
class ExerciseAssignmentBase(BaseModel):
    weekly_frequency: int
    series: int
    repetitions: int
    start_date: date
    end_date: date
    id_patient: int
    id_exercise: int

class ExerciseAssignmentCreate(ExerciseAssignmentBase):
    pass

class ExerciseAssignment(ExerciseAssignmentBase):
    id_assignment: int
    class Config:
        from_attributes = True

#--- Appointment Schemas ---
class AppointmentBase(BaseModel):
    date: datetime
    state: AppointmentState = AppointmentState.PENDIENTE
    notes: Optional[str] = None
    id_patient: int
    id_physio: int

class AppointmentCreate(AppointmentBase):
    pass

class Appointment(AppointmentBase):
    id_appointment: int
    class Config:
        from_attributes = True