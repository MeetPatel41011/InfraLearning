import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from database import engine, Base
from routers import health, logs, upload

load_dotenv()

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Infra-Learning Journal API")

# CORS setup
origins = [
    os.getenv("FRONTEND_URL", "http://localhost:5173"),
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api")
app.include_router(logs.router, prefix="/api")
app.include_router(upload.router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
