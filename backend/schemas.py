from pydantic import BaseModel, EmailStr, Field
from datetime import date, datetime
from typing import List, Optional

from backend.models import AppointmentState

#Schemas.py describe how the data will be sent and received in JSON format between the frontend and backend using Pydantic.


#--- Authentication Schemas ---
class UserLogin(BaseModel):
    mail: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    role: str 
    user_id: int
    name: str

class TokenData(BaseModel):
    mail: Optional[str] = None
    role: Optional[str] = None

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

class PhysioUpdate(BaseModel):
    name: Optional[str] = None
    surnames: Optional[str] = None
    mail: Optional[EmailStr] = None
    password: Optional[str] = None

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

class PatientUpdate(BaseModel):
    name: Optional[str] = None
    surnames: Optional[str] = None
    mail: Optional[EmailStr] = None
    password: Optional[str] = None
    start_date: Optional[date] = None
    id_physio: Optional[int] = None

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

class PainRecordUpdate(BaseModel):
    level_pain: Optional[int] = Field(ge=0, le=10)
    comment: Optional[str] = None
    record_date: Optional[date] = None

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
    
class ExerciseUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    video_url: Optional[str] = None
    active: Optional[bool] = None

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

class ExerciseAssignmentUpdate(BaseModel):
    weekly_frequency: Optional[int] = None
    series: Optional[int] = None
    repetitions: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    id_patient: Optional[int] = None
    id_exercise: Optional[int] = None

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
    
class AppointmentUpdate(BaseModel):
    date: Optional[datetime] = None
    state: Optional[AppointmentState] = None
    notes: Optional[str] = None
    id_patient: Optional[int] = None
    id_physio: Optional[int] = None

#--- Exercise Done Schemas ---
class ExerciseDoneBase(BaseModel):
    date: datetime
    id_assignment: int

class ExerciseDoneCreate(ExerciseDoneBase):
    pass

class ExerciseDone(ExerciseDoneBase):
    id_done: int
    class Config:  
        from_attributes = True

class ExerciseDoneUpdate(BaseModel):
    date: Optional[datetime] = None
    id_assignment: Optional[int] = None