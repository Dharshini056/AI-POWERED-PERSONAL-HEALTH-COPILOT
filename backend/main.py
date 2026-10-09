import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.database import init_db
from app.api import router, UPLOAD_DIR
from app.sample_data import load_sample_dataset_into_db

app = FastAPI(
    title="AI Personal Health Copilot API",
    description="Backend API for Multilingual Medical Document OCR, Clinical Entity Extraction, AI Summarization, and ABDM/FHIR Data Standardization",
    version="1.0.0"
)

# Enable CORS for Vite frontend (localhost:5173 / localhost:3000 / localhost:8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount uploads directory for previewing documents
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# Include API Router
app.include_router(router)

@app.on_event("startup")
def startup_event():
    init_db()
    # Pre-populate sample demo dataset on startup so judges have immediate data
    try:
        load_sample_dataset_into_db()
        print("Database initialized and demo dataset loaded successfully!")
    except Exception as e:
        print("Startup warning:", e)

@app.get("/")
def root():
    return {
        "status": "online",
        "service": "AI Personal Health Copilot",
        "version": "1.0.0",
        "docs_url": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
