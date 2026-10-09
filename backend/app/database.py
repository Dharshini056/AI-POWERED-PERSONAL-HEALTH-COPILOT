import sqlite3
import json
import os
from typing import List, Dict, Any, Optional

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "health_copilot.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT,
        abha_id TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        id TEXT PRIMARY KEY,
        user_id TEXT,
        filename TEXT NOT NULL,
        file_path TEXT NOT NULL,
        file_type TEXT,
        file_size INTEGER,
        doc_type TEXT,
        status TEXT DEFAULT 'pending',
        detected_language TEXT,
        ocr_confidence REAL DEFAULT 0.0,
        summary_en TEXT,
        summary_ta TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ocr_results (
        id TEXT PRIMARY KEY,
        document_id TEXT NOT NULL,
        raw_text TEXT,
        cleaned_text TEXT,
        detected_language TEXT,
        confidence_score REAL DEFAULT 0.0,
        processing_time_ms INTEGER,
        engine_name TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (document_id) REFERENCES documents(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        id TEXT PRIMARY KEY,
        document_id TEXT,
        name TEXT,
        age INTEGER,
        gender TEXT,
        date_of_birth TEXT,
        patient_id_ref TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (document_id) REFERENCES documents(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS medications (
        id TEXT PRIMARY KEY,
        document_id TEXT NOT NULL,
        name TEXT NOT NULL,
        dose TEXT,
        dosage_unit TEXT,
        frequency TEXT,
        route TEXT,
        duration TEXT,
        instructions TEXT,
        before_after_food TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (document_id) REFERENCES documents(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS lab_results (
        id TEXT PRIMARY KEY,
        document_id TEXT NOT NULL,
        test_name TEXT NOT NULL,
        value TEXT NOT NULL,
        unit TEXT,
        reference_range TEXT,
        status TEXT,
        date TEXT,
        explanation_en TEXT,
        explanation_ta TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (document_id) REFERENCES documents(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS diagnoses (
        id TEXT PRIMARY KEY,
        document_id TEXT NOT NULL,
        diagnosis_name TEXT NOT NULL,
        date TEXT,
        source_document TEXT,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (document_id) REFERENCES documents(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS procedures (
        id TEXT PRIMARY KEY,
        document_id TEXT NOT NULL,
        procedure_name TEXT NOT NULL,
        date TEXT,
        hospital TEXT,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (document_id) REFERENCES documents(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS symptoms (
        id TEXT PRIMARY KEY,
        document_id TEXT NOT NULL,
        symptom_name TEXT NOT NULL,
        severity TEXT,
        duration TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (document_id) REFERENCES documents(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS medical_events (
        id TEXT PRIMARY KEY,
        document_id TEXT NOT NULL,
        event_type TEXT NOT NULL,
        title TEXT NOT NULL,
        description TEXT,
        doctor_name TEXT,
        facility_name TEXT,
        event_date TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (document_id) REFERENCES documents(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS health_timeline (
        id TEXT PRIMARY KEY,
        document_id TEXT NOT NULL,
        event_date TEXT NOT NULL,
        title TEXT NOT NULL,
        category TEXT NOT NULL,
        summary TEXT,
        details_json TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (document_id) REFERENCES documents(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_history (
        id TEXT PRIMARY KEY,
        session_id TEXT DEFAULT 'default',
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Default user if none exists
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
        INSERT INTO users (id, name, email, abha_id)
        VALUES ('usr_demo_01', 'Arun Kumar', 'arun.kumar@demo-health.org', '91-4521-8934-1022')
        """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully at:", DB_PATH)
