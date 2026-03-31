import os
import shutil
from typing import List
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

# --- DATABASE SETUP ---
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./dev.db")
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class LogEntry(Base):
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- SCHEMAS ---
class LogCreate(BaseModel):
    title: str
    content: str

class LogResponse(BaseModel):
    id: int
    title: str
    content: str
    class Config:
        from_attributes = True

# --- APP SETUP ---
app = FastAPI(title="Infra-Learning Journal API")

# Middleware for logging
@app.middleware("http")
async def log_requests(request, call_next):
    print(f"DEBUG: {request.method} {request.url}")
    response = await call_next(request)
    print(f"DEBUG status: {response.status_code}")
    return response

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all origins for local testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ROUTES ---
@app.get("/")
def read_root():
    return {"message": "Infra-Learning API is running! Use /api/health/ to check status."}

@app.get("/api/health/")
def health_check():
    return {"status": "ok"}

@app.get("/api/logs/", response_model=List[LogResponse])
def read_logs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logs = db.query(LogEntry).offset(skip).limit(limit).all()
    return logs

@app.post("/api/logs/", response_model=LogResponse)
def create_log(log: LogCreate, db: Session = Depends(get_db)):
    db_log = LogEntry(title=log.title, content=log.content)
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

@app.delete("/api/logs/{log_id}/")
def delete_log(log_id: int, db: Session = Depends(get_db)):
    db_log = db.query(LogEntry).filter(LogEntry.id == log_id).first()
    if not db_log:
        raise HTTPException(status_code=404, detail="Log not found")
    db.delete(db_log)
    db.commit()
    return {"message": "Log deleted successfully"}

UPLOAD_DIR = "tmp/uploads"
@app.post("/api/upload/")
def upload_image(file: UploadFile = File(...)):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename, "saved_path": file_path}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8888))
    print(f"Starting server on http://127.0.0.1:{port}...")
    uvicorn.run(app, host="127.0.0.1", port=port)
