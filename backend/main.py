from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

import models, schemas, crud
from database import engine, get_db

# Main.py is the entry point of our FastAPI application. It defines the API endpoints for managing physiotherapists, patients, appointments, and pain records. It uses the CRUD functions defined in crud.py to interact with the database.

# Make the database tables based on the models defined in models.py if not already created
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Rehab & Move API",
    description="API for managing physiotherapists, patients, appointments, and pain records in the Rehab & Move application.",
    version="1.0.0"
)

#--- Physio Endpoints ---

@app.post("/physios/", response_model=schemas.Physio, status_code=status.HTTP_201_CREATED)
def create_physio(physio: schemas.PhysioCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_physio(db=db, physio=physio)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    

#--- Patient Endpoints ---

@app.get("/patients/", response_model=List[schemas.Patient])
def read_patients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
            patients = crud.get_patients(db, skip=skip, limit=limit)
            return patients
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@app.post("/patients/", response_model=schemas.Patient, status_code=status.HTTP_201_CREATED)
def create_patient(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_patient(db=db, patient=patient)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
# --- Pain Record Endpoints ---

@app.post("/pain_records/", response_model=schemas.PainRecord, status_code=status.HTTP_201_CREATED)
def create_pain_record(pain_record: schemas.PainRecordCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_pain_record(db=db, pain_record=pain_record)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@app.get("/pain_records/", response_model=List[schemas.PainRecord])
def read_pain_records(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        pain_records = crud.get_pain_records_by_patient(db, skip=skip, limit=limit)
        return pain_records
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
#--- Health Check Endpoint ---
@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Rehab & Move API is running smoothly!"}