from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from database import engine, get_db, Base
import models

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Caya Asset Integrity API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class FluidCreate(BaseModel):
    fluid_id: str
    name: str
    description: Optional[str] = ""
    status: Optional[str] = "Active"

class FluidOut(BaseModel):
    id: int
    fluid_id: str
    name: str
    description: str
    status: str
    revision: int

    class Config:
        from_attributes = True

class ServiceCreate(BaseModel):
    service_id: str
    name: str
    description: Optional[str] = ""
    fluid_id: Optional[str] = None
    status: Optional[str] = "Active"

class ServiceOut(BaseModel):
    id: int
    service_id: str
    name: str
    description: str
    fluid_id: Optional[str]
    status: str
    revision: int

    class Config:
        from_attributes = True

@app.get("/")
def root():
    return {"message": "Caya API is running", "version": "0.1.0"}

@app.get("/api/fluids", response_model=List[FluidOut])
def list_fluids(db: Session = Depends(get_db)):
    return db.query(models.Fluid).all()

@app.post("/api/fluids", response_model=FluidOut)
def create_fluid(payload: FluidCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Fluid).filter(models.Fluid.fluid_id == payload.fluid_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Fluid ID already exists")
    fluid = models.Fluid(**payload.dict())
    db.add(fluid)
    db.commit()
    db.refresh(fluid)
    return fluid

@app.get("/api/services", response_model=List[ServiceOut])
def list_services(db: Session = Depends(get_db)):
    return db.query(models.Service).all()

@app.post("/api/services", response_model=ServiceOut)
def create_service(payload: ServiceCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Service).filter(models.Service.service_id == payload.service_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Service ID already exists")
    service = models.Service(**payload.dict())
    db.add(service)
    db.commit()
    db.refresh(service)
    return service
