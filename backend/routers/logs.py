from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import get_db

router = APIRouter()

@router.post("/logs", response_model=schemas.LogResponse)
def create_log(log: schemas.LogCreate, db: Session = Depends(get_db)):
    db_log = models.LogEntry(**log.model_dump())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

@router.get("/logs", response_model=List[schemas.LogResponse])
def read_logs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logs = db.query(models.LogEntry).offset(skip).limit(limit).all()
    return logs

@router.put("/logs/{log_id}", response_model=schemas.LogResponse)
def update_log(log_id: int, log: schemas.LogCreate, db: Session = Depends(get_db)):
    db_log = db.query(models.LogEntry).filter(models.LogEntry.id == log_id).first()
    if not db_log:
        raise HTTPException(status_code=404, detail="Log not found")
    
    db_log.title = log.title
    db_log.content = log.content
    db.commit()
    db.refresh(db_log)
    return db_log

@router.delete("/logs/{log_id}")
def delete_log(log_id: int, db: Session = Depends(get_db)):
    db_log = db.query(models.LogEntry).filter(models.LogEntry.id == log_id).first()
    if not db_log:
        raise HTTPException(status_code=404, detail="Log not found")
    db.delete(db_log)
    db.commit()
    return {"message": "Log deleted successfully"}
