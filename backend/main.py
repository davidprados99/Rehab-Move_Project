from fastapi import FastAPI, Depends, HTTPException, security, status
from sqlalchemy.orm import Session
from typing import List

from backend import models, schemas, crud
from backend.database import engine, get_db
from backend.security import verify_password, create_access_token

# Main.py is the entry point of our FastAPI application. It defines the API endpoints for managing physiotherapists, patients, appointments, and pain records. It uses the CRUD functions defined in crud.py to interact with the database.

# Make the database tables based on the models defined in models.py if not already created
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Rehab & Move API",
    description="API for managing physiotherapists, patients, appointments, and pain records in the Rehab & Move application.",
    version="1.0.0"
)

#--- Authentication Endpoint ---

@app.post("/login", response_model=schemas.Token, tags=["Autenticación"])
def login(form_data: schemas.UserLogin, db: Session = Depends(get_db)):
    # 1. Try to find the user in PHYSIOS first
    user = crud.get_physio_by_email(db, email=form_data.email)
    role = "physio"
    
    # 2. If not found in PHYSIOS, try to find the user in PATIENTS
    if not user:
        user = crud.get_patient_by_email(db, email=form_data.email)
        role = "patient"
    
    # 3. Verify the password if the user exists
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )
    
    # 4. Create a JWT token with the user's email and role. 
    # It's crucial to include the 'role' in the JWT payload for proper authorization in protected endpoints.
    access_token = create_access_token(
        data={"sub": user.mail, "role": role}
    )
    
    return {
        "access_token": access_token, 
        "token_type": "bearer", 
        "role": role,
        "user_id": user.id_physio if role == "physio" else user.id_patient,
        "name": user.name
    }


#--- Physio Endpoints ---


@app.post("/physios/", response_model=schemas.Physio, status_code=status.HTTP_201_CREATED, tags=["Physios"])
def create_physio(physio: schemas.PhysioCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_physio(db=db, physio=physio)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@app.get("/physios/", response_model=List[schemas.Physio], tags=["Physios"])
def read_physios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        physios = crud.get_physios(db, skip=skip, limit=limit)
        return physios
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@app.get("/physios/{id_physio}", response_model=schemas.Physio, tags=["Physios"])
def read_physio_by_id(id_physio: int, db: Session = Depends(get_db)):
    try:
        db_physio = crud.get_physio_by_id(db, id_physio=id_physio)
        if db_physio is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Physio not found")
        return db_physio
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@app.get("/physios/mail/{email}", response_model=schemas.Physio, tags=["Physios"])
def read_physio_by_email(email: str, db: Session = Depends(get_db)):
    try:
        db_physio = crud.get_physio_by_email(db, email=email)
        if db_physio is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Physio not found")
        return db_physio
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@app.patch("/physios/{id_physio}", response_model=schemas.Physio, tags=["Physios"])
def update_physio(id_physio: int, physio_update: schemas.PhysioUpdate, db: Session = Depends(get_db)):
    try:
        db_physio = crud.update_physio(db=db, id=id_physio, physio_update=physio_update)
        return db_physio
    except ValueError as e:
        error_msg = str(e)
        if "not found" in error_msg:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error_msg)
        
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_msg)

@app.delete("/physios/{id_physio}", status_code=status.HTTP_204_NO_CONTENT, tags=["Physios"])
def delete_physio(id_physio: int, db: Session = Depends(get_db)):
    try:
        crud.delete_physio(db=db, id_physio=id_physio)
        return {"detail": "Physio deleted successfully."}
    except ValueError as e:
        error_msg = str(e)
        if "not found" in error_msg:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error_msg)
        
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_msg)


#--- Patient Endpoints ---


@app.post("/patients/", response_model=schemas.Patient, status_code=status.HTTP_201_CREATED, tags=["Patients"])
def create_patient(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_patient(db=db, patient=patient)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@app.get("/patients/{id_patient}", response_model=schemas.Patient, tags=["Patients"])
def read_patient_by_id(id_patient: int, db: Session = Depends(get_db)):
    try:
        db_patient = crud.get_patient_by_id(db, id_patient=id_patient)
        if db_patient is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
        return db_patient
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@app.get("/patients/mail/{email}", response_model=schemas.Patient, tags=["Patients"])
def read_patient_by_email(email: str, db: Session = Depends(get_db)):
    try:
        db_patient = crud.get_patient_by_email(db, email=email)
        if db_patient is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
        return db_patient
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@app.get("/physios/{id_physio}/patients", response_model=List[schemas.Patient], tags=["Patients"])
def read_patients_by_physio(id_physio: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        patients = crud.get_patients_by_physio(db, id_physio=id_physio, skip=skip, limit=limit)
        return patients
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@app.get("/patients/", response_model=List[schemas.Patient], tags=["Patients"])
def read_patients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
            patients = crud.get_patients(db, skip=skip, limit=limit)
            return patients
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@app.patch("/patients/{id_patient}", response_model=schemas.Patient, tags=["Patients"])
def update_patient(id_patient: int, patient_update: schemas.PatientUpdate, db: Session = Depends(get_db)):
    try:
        db_patient = crud.update_patient(db=db, id_patient=id_patient, patient_update=patient_update)
        return db_patient
    except ValueError as e:
        error_msg = str(e)
        if "not found" in error_msg:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error_msg)
        
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_msg)

@app.delete("/patients/{id_patient}", status_code=status.HTTP_204_NO_CONTENT, tags=["Patients"])
def delete_patient(id_patient: int, db: Session = Depends(get_db)):
    try:
        crud.delete_patient(db=db, id_patient=id_patient)
        return {"detail": "Patient deleted successfully."}
    except ValueError as e:
        error_msg = str(e)
        if "not found" in error_msg:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error_msg)
        
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_msg)


# --- Pain Record Endpoints ---


@app.post("/pain_records/", response_model=schemas.PainRecord, status_code=status.HTTP_201_CREATED, tags=["Pain Records"])
def create_pain_record(pain_record: schemas.PainRecordCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_pain_record(db=db, pain_record=pain_record)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@app.get("/pain_records/patient/{id_patient}", response_model=List[schemas.PainRecord], tags=["Pain Records"])
def read_pain_records_by_patient(id_patient: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        pain_records = crud.get_pain_records_by_patient(db, id_patient=id_patient, skip=skip, limit=limit)
        return pain_records
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@app.get("/pain_records/{id_pain_record}", response_model=schemas.PainRecord, tags=["Pain Records"])
def read_pain_record_by_id(id_pain_record: int, db: Session = Depends(get_db)):
    try:
        db_pain_record = crud.get_pain_record_by_id(db, id_pain_record=id_pain_record)
        if db_pain_record is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pain record not found")
        return db_pain_record
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@app.patch("/pain_records/{id_pain_record}", response_model=schemas.PainRecord, tags=["Pain Records"])
def update_pain_record(id_pain_record: int, pain_record_update: schemas.PainRecordUpdate, db: Session = Depends(get_db)):
    try:
        db_pain_record = crud.update_pain_record(db=db, id_pain_record=id_pain_record, pain_record_update=pain_record_update)
        return db_pain_record
    except ValueError as e:
        error_msg = str(e)
        if "not found" in error_msg:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error_msg)
        
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_msg)

@app.delete("/pain_records/{id_pain_record}", status_code=status.HTTP_204_NO_CONTENT, tags=["Pain Records"])
def delete_pain_record(id_pain_record: int, db: Session = Depends(get_db)):
    try:
        crud.delete_pain_record(db=db, id_pain_record=id_pain_record)
        return {"detail": "Pain record deleted successfully."}
    except ValueError as e:
        error_msg = str(e)
        if "not found" in error_msg:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error_msg)
        
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_msg)


# --- Appointments Endpoints ---


@app.post("/appointments/", response_model=schemas.Appointment, status_code=status.HTTP_201_CREATED, tags=["Appointments"])
def create_appointment(appointment: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_appointment(db=db, appointment=appointment)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@app.get("/appointments/{id_appointment}", response_model=schemas.Appointment, tags=["Appointments"])
def read_appointment_by_id(id_appointment: int, db: Session = Depends(get_db)):
    try:
        db_appointment = crud.get_appointment_by_id(db, id_appointment=id_appointment)
        if db_appointment is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
        return db_appointment
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@app.get("/appointments/patient/{id_patient}", response_model=List[schemas.Appointment], tags=["Appointments"])
def read_appointments_by_patient(id_patient: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        appointments = crud.get_appointments_by_patient(db, id_patient=id_patient, skip=skip, limit=limit)
        return appointments
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@app.get("/appointments/physio/{id_physio}", response_model=List[schemas.Appointment], tags=["Appointments"])
def read_appointments_by_physio(id_physio: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        appointments = crud.get_appointments_by_physio(db, id_physio=id_physio, skip=skip, limit=limit)
        return appointments
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))



@app.patch("/appointments/{id_appointment}", response_model=schemas.Appointment, tags=["Appointments"])
def update_appointment(id_appointment: int, appointment_update: schemas.AppointmentUpdate, db: Session = Depends(get_db)):
    try:
        db_appointment = crud.update_appointment(db=db, id_appointment=id_appointment, appointment_update=appointment_update)
        return db_appointment
    except ValueError as e:
        error_msg = str(e)
        if "not found" in error_msg:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error_msg)
        
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_msg)

@app.delete("/appointments/{id_appointment}", status_code=status.HTTP_204_NO_CONTENT, tags=["Appointments"])
def delete_appointment(id_appointment: int, db: Session = Depends(get_db)):
    try:
        crud.delete_appointment(db=db, id_appointment=id_appointment)
        return {"detail": "Appointment deleted successfully."}
    except ValueError as e:
        error_msg = str(e)
        if "not found" in error_msg:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error_msg)
        
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_msg)


# --- Exercises Endpoints ---


@app.post("/exercises/", response_model=schemas.Exercise, status_code=status.HTTP_201_CREATED, tags=["Exercises"])
def create_exercise(exercise: schemas.ExerciseCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_exercise(db=db, exercise=exercise)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@app.get("/exercises/", response_model=List[schemas.Exercise], tags=["Exercises"])
def read_exercises(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        exercises = crud.get_exercises(db, skip=skip, limit=limit)
        return exercises
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@app.get("/exercises/{id_exercise}", response_model=schemas.Exercise, tags=["Exercises"])
def read_exercise_by_id(id_exercise: int, db: Session = Depends(get_db)):
    try:
        db_exercise = crud.get_exercise_by_id(db, id_exercise=id_exercise)
        if db_exercise is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found")
        return db_exercise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@app.patch("/exercises/{id_exercise}", response_model=schemas.Exercise, tags=["Exercises"])
def update_exercise(id_exercise: int, exercise_update: schemas.ExerciseUpdate, db: Session = Depends(get_db)):
    try:
        db_exercise = crud.update_exercise(db=db, id_exercise=id_exercise, exercise_update=exercise_update)
        return db_exercise
    except ValueError as e:
        error_msg = str(e)
        if "not found" in error_msg:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error_msg)
        
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_msg)

@app.patch("/exercises/{id_exercise}/inactivate", response_model=schemas.Exercise, tags=["Exercises"])
def inactivate_exercise(id_exercise: int, db: Session = Depends(get_db)):
    try:
        db_exercise = crud.inactivate_exercise(db=db, id_exercise=id_exercise)
        return db_exercise
    except ValueError as e:
        error_msg = str(e)
        if "not found" in error_msg:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error_msg)
        
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_msg)

@app.patch("/exercises/{id_exercise}/activate", response_model=schemas.Exercise, tags=["Exercises"])
def activate_exercise(id_exercise: int, db: Session = Depends(get_db)):
    try:
        db_exercise = crud.activate_exercise(db=db, id_exercise=id_exercise)
        return db_exercise
    except ValueError as e:
        error_msg = str(e)
        if "not found" in error_msg:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error_msg)
        
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_msg)

@app.delete("/exercises/{id_exercise}", status_code=status.HTTP_204_NO_CONTENT, tags=["Exercises"])
def delete_exercise(id_exercise: int, db: Session = Depends(get_db)):
    try:
        crud.delete_exercise(db=db, id_exercise=id_exercise)
        return {"detail": "Exercise deleted successfully."}
    except ValueError as e:
        error_msg = str(e)
        if "not found" in error_msg:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error_msg)
        
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_msg)


# --- Exercises Assignments Endpoints ---


@app.post("/assignments/", response_model=schemas.ExerciseAssignment, status_code=status.HTTP_201_CREATED, tags=["Exercise Assignments"])
def assign_exercise_to_patient(assignment: schemas.ExerciseAssignmentCreate, db: Session = Depends(get_db)):
    try:
        return crud.assign_exercise_to_patient(db=db, assignment=assignment)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@app.get("/assignments/patient/{id_patient}", response_model=List[schemas.ExerciseAssignment], tags=["Exercise Assignments"])
def read_assignments_by_patient(id_patient: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        assignments = crud.get_exercise_assignments_by_patient(db, id_patient=id_patient, skip=skip, limit=limit)
        return assignments
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@app.get("/assignments/exercise/{id_exercise}", response_model=List[schemas.ExerciseAssignment], tags=["Exercise Assignments"])
def read_assignments_by_exercise(id_exercise: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        assignments = crud.get_exercise_assignments_by_exercise(db, id_exercise=id_exercise, skip=skip, limit=limit)
        return assignments
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@app.get("/assignments/{id_assignment}", response_model=schemas.ExerciseAssignment, tags=["Exercise Assignments"]) 
def read_assignment_by_id(id_assignment: int, db: Session = Depends(get_db)):
    try:
        db_assignment = crud.get_exercise_assignment_by_id(db, id_assignment=id_assignment)
        if db_assignment is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assignment not found")
        return db_assignment
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@app.patch("/assignments/{id_assignment}", response_model=schemas.ExerciseAssignment, tags=["Exercise Assignments"])
def update_exercise_assignment(id_assignment: int, assignment_update: schemas.ExerciseAssignmentUpdate, db: Session = Depends(get_db)):
    try:
        db_assignment = crud.update_exercise_assignment(db=db, id_assignment=id_assignment, assignment_update=assignment_update)
        return db_assignment
    except ValueError as e:
        error_msg = str(e)
        if "not found" in error_msg:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error_msg)
        
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_msg)

@app.delete("/assignments/{id_assignment}", status_code=status.HTTP_204_NO_CONTENT, tags=["Exercise Assignments"])
def delete_exercise_assignment(id_assignment: int, db: Session = Depends(get_db)):
    try:
        crud.delete_exercise_assignment(db=db, id_assignment=id_assignment)
        return {"detail": "Exercise Assignment deleted successfully."}
    except ValueError as e:
        error_msg = str(e)
        if "not found" in error_msg:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error_msg)
        
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_msg)


# --- Exercises Done Endpoints ---


@app.post("/exercises_done/", response_model=schemas.ExerciseDone, status_code=status.HTTP_201_CREATED, tags=["Exercises Done"])
def mark_exercise_done(exercise_done: schemas.ExerciseDoneCreate, db: Session = Depends(get_db)):
    try:
        return crud.mark_exercise_done(db=db, exercise_done=exercise_done)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@app.get("/exercises_done/{id_exercise_done}", response_model=schemas.ExerciseDone, tags=["Exercises Done"])
def read_exercise_done_by_id(id_exercise_done: int, db: Session = Depends(get_db)):
    try:
        db_exercise_done = crud.get_exercise_done_by_id(db, id_exercise_done=id_exercise_done)
        if db_exercise_done is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exercise done record not found")
        return db_exercise_done
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@app.get("/exercises_done/assignment/{id_assignment}", response_model=List[schemas.ExerciseDone], tags=["Exercises Done"])
def read_exercises_done_by_assignment(id_assignment: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        exercises_done = crud.get_exercise_done_by_assignment(db, id_assignment=id_assignment)
        return exercises_done
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@app.patch("/exercises_done/{id_exercise_done}", response_model=schemas.ExerciseDone, tags=["Exercises Done"])
def update_exercise_done(id_exercise_done: int, exercise_done_update: schemas.ExerciseDoneUpdate, db: Session = Depends(get_db)):
    try:
        db_exercise_done = crud.update_exercise_done(db=db, id_exercise_done=id_exercise_done, exercise_done_update=exercise_done_update)
        return db_exercise_done
    except ValueError as e:
        error_msg = str(e)
        if "not found" in error_msg:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error_msg)
        
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_msg)

@app.delete("/exercises_done/{id_exercise_done}", status_code=status.HTTP_204_NO_CONTENT, tags=["Exercises Done"])
def delete_exercise_done(id_exercise_done: int, db: Session = Depends(get_db)):
    try:
        crud.delete_exercise_done(db=db, id_exercise_done=id_exercise_done)
        return {"detail": "Exercise done record deleted successfully."}
    except ValueError as e:
        error_msg = str(e)
        if "not found" in error_msg:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error_msg)
        
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_msg)


#--- Health Check Endpoint ---


@app.get("/health", tags=["Health Check"])
def health_check():
    return {"status": "ok", "message": "Rehab & Move API is running and healthy."}