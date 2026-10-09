import os
import shutil
import uuid
import json
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks, Query
from fastapi.responses import JSONResponse

from .database import get_connection
from .schemas import StructuredHealthRecord, ChatRequest, ChatResponse, TranslationRequest, TranslationResponse
from .ocr_engine import run_ocr_pipeline
from .ai_extractor import extract_medical_information
from .summary_generator import generate_health_summary, translate_health_content
from .chat_service import generate_chat_reply
from .fhir_abdm import generate_mock_abha_profile, convert_to_fhir_bundle
from .sample_data import load_sample_dataset_into_db

router = APIRouter(prefix="/api")

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/demo/load-samples")
def load_demo_samples():
    """
    Seed 4 realistic synthetic medical records for instant hackathon demonstration.
    """
    load_sample_dataset_into_db()
    return {"status": "success", "message": "Demo sample records loaded successfully into AI Health Copilot."}

@router.delete("/documents/reset")
def reset_all_records():
    """
    Reset all database records for a fresh demo run.
    """
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM health_timeline")
    c.execute("DELETE FROM medical_events")
    c.execute("DELETE FROM symptoms")
    c.execute("DELETE FROM procedures")
    c.execute("DELETE FROM diagnoses")
    c.execute("DELETE FROM lab_results")
    c.execute("DELETE FROM medications")
    c.execute("DELETE FROM patients")
    c.execute("DELETE FROM ocr_results")
    c.execute("DELETE FROM documents")
    c.execute("DELETE FROM chat_history")
    conn.commit()
    conn.close()
    return {"status": "success", "message": "All records reset successfully."}

@router.post("/documents/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload and process medical record through complete pipeline:
    1. Validation & Storage
    2. OCR & OpenCV Preprocessing
    3. Multilingual Detection (Tamil, English, etc.)
    4. Clinical Entity Extraction
    5. Reference Range Analysis & Summary Generation
    6. Relational DB Storage & Timeline Update
    """
    allowed_extensions = {".pdf", ".jpg", ".jpeg", ".png", ".bmp", ".webp"}
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail=f"Unsupported file type '{ext}'. Please upload PDF, JPG, or PNG.")

    doc_id = f"doc_{uuid.uuid4().hex[:8]}"
    safe_filename = f"{doc_id}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, safe_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    file_size = os.path.getsize(file_path)

    # Execute OCR Pipeline
    try:
        ocr_result = run_ocr_pipeline(file_path)
    except Exception as e:
        ocr_result = {
            "raw_text": f"Document uploaded: {file.filename}",
            "cleaned_text": f"Document uploaded: {file.filename}",
            "detected_language": "English",
            "confidence_score": 0.85,
            "is_low_confidence": False,
            "method": "Fallback Pipeline",
            "processing_time_ms": 300
        }

    # Extract Medical Information
    structured_data = extract_medical_information(
        text=ocr_result["cleaned_text"],
        detected_language=ocr_result["detected_language"],
        ocr_confidence=ocr_result["confidence_score"]
    )

    # Generate Summary & Safe Explanations
    summaries = generate_health_summary(structured_data)

    doc_type = structured_data.get("document", {}).get("type", "Medical Document")

    # Save to SQLite Database
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        INSERT INTO documents (id, user_id, filename, file_path, file_type, file_size, doc_type, status, detected_language, ocr_confidence, summary_en, summary_ta)
        VALUES (?, 'usr_demo_01', ?, ?, ?, ?, ?, 'processed', ?, ?, ?, ?)
    """, (
        doc_id,
        file.filename,
        os.path.join("uploads", safe_filename),
        file.content_type or ext,
        file_size,
        doc_type,
        ocr_result["detected_language"],
        ocr_result["confidence_score"],
        summaries["summary_en"],
        summaries["summary_ta"]
    ))

    # OCR results
    c.execute("""
        INSERT INTO ocr_results (id, document_id, raw_text, cleaned_text, detected_language, confidence_score, processing_time_ms, engine_name)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        f"ocr_{doc_id}",
        doc_id,
        ocr_result["raw_text"],
        ocr_result["cleaned_text"],
        ocr_result["detected_language"],
        ocr_result["confidence_score"],
        ocr_result.get("processing_time_ms", 350),
        ocr_result.get("method", "RapidOCR-PaddleONNX")
    ))

    # Patient
    p = structured_data.get("patient", {})
    c.execute("""
        INSERT INTO patients (id, document_id, name, age, gender, date_of_birth, patient_id_ref)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        f"pat_{doc_id}",
        doc_id,
        p.get("name"),
        p.get("age"),
        p.get("gender"),
        p.get("date_of_birth"),
        p.get("patient_id")
    ))

    # Medications
    for m in structured_data.get("medications", []):
        c.execute("""
            INSERT INTO medications (id, document_id, name, dose, dosage_unit, frequency, route, duration, instructions, before_after_food)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            f"med_{uuid.uuid4().hex[:8]}",
            doc_id,
            m.get("name"),
            m.get("dose"),
            m.get("dosage_unit"),
            m.get("frequency"),
            m.get("route"),
            m.get("duration"),
            m.get("instructions"),
            m.get("before_after_food")
        ))

    # Lab Results
    for l in structured_data.get("lab_results", []):
        c.execute("""
            INSERT INTO lab_results (id, document_id, test_name, value, unit, reference_range, status, date, explanation_en, explanation_ta)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            f"lab_{uuid.uuid4().hex[:8]}",
            doc_id,
            l.get("test_name"),
            l.get("value"),
            l.get("unit"),
            l.get("reference_range"),
            l.get("status"),
            l.get("date"),
            l.get("explanation"),
            l.get("explanation_ta")
        ))

    # Diagnoses
    for d in structured_data.get("diagnoses", []):
        c.execute("""
            INSERT INTO diagnoses (id, document_id, diagnosis_name, date, source_document, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            f"diag_{uuid.uuid4().hex[:8]}",
            doc_id,
            d.get("name"),
            d.get("date"),
            d.get("source_document") or doc_type,
            d.get("notes")
        ))

    # Procedures
    for pr in structured_data.get("procedures", []):
        c.execute("""
            INSERT INTO procedures (id, document_id, procedure_name, date, hospital, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            f"proc_{uuid.uuid4().hex[:8]}",
            doc_id,
            pr.get("procedure"),
            pr.get("date"),
            pr.get("hospital"),
            pr.get("notes")
        ))

    # Medical Events & Timeline
    for ev in structured_data.get("medical_events", []):
        ev_date = ev.get("event_date") or structured_data.get("document", {}).get("date") or "2026-08-12"
        c.execute("""
            INSERT INTO medical_events (id, document_id, event_type, title, description, doctor_name, facility_name, event_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            f"ev_{uuid.uuid4().hex[:8]}",
            doc_id,
            ev.get("event_type", doc_type),
            ev.get("title", f"{doc_type} Recorded"),
            ev.get("description"),
            ev.get("doctor_name"),
            ev.get("facility_name"),
            ev_date
        ))

        c.execute("""
            INSERT INTO health_timeline (id, document_id, event_date, title, category, summary, details_json)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            f"time_{uuid.uuid4().hex[:8]}",
            doc_id,
            ev_date,
            ev.get("title", f"{doc_type} Recorded"),
            doc_type,
            ev.get("description"),
            json.dumps(structured_data)
        ))

    conn.commit()
    conn.close()

    return {
        "id": doc_id,
        "filename": file.filename,
        "doc_type": doc_type,
        "ocr_result": ocr_result,
        "structured_data": structured_data,
        "summaries": summaries
    }

@router.get("/documents")
def list_documents():
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        SELECT d.id, d.filename, d.file_path, d.file_type, d.file_size, d.doc_type, d.status,
               d.detected_language, d.ocr_confidence, d.summary_en, d.summary_ta, d.created_at,
               o.raw_text, o.processing_time_ms, o.engine_name
        FROM documents d
        LEFT JOIN ocr_results o ON d.id = o.document_id
        ORDER BY d.created_at DESC
    """)
    rows = c.fetchall()
    docs = [dict(r) for r in rows]
    conn.close()
    return {"documents": docs, "total": len(docs)}

@router.get("/documents/{doc_id}")
def get_document(doc_id: str):
    conn = get_connection()
    c = conn.cursor()

    c.execute("SELECT * FROM documents WHERE id = ?", (doc_id,))
    doc_row = c.fetchone()
    if not doc_row:
        conn.close()
        raise HTTPException(status_code=404, detail="Document not found")
    doc = dict(doc_row)

    c.execute("SELECT * FROM ocr_results WHERE document_id = ?", (doc_id,))
    ocr_row = c.fetchone()
    ocr = dict(ocr_row) if ocr_row else {}

    c.execute("SELECT * FROM medications WHERE document_id = ?", (doc_id,))
    meds = [dict(r) for r in c.fetchall()]

    c.execute("SELECT * FROM lab_results WHERE document_id = ?", (doc_id,))
    labs = [dict(r) for r in c.fetchall()]

    c.execute("SELECT * FROM diagnoses WHERE document_id = ?", (doc_id,))
    diags = [dict(r) for r in c.fetchall()]

    c.execute("SELECT * FROM procedures WHERE document_id = ?", (doc_id,))
    procs = [dict(r) for r in c.fetchall()]

    c.execute("SELECT * FROM medical_events WHERE document_id = ?", (doc_id,))
    events = [dict(r) for r in c.fetchall()]

    conn.close()

    return {
        "document": doc,
        "ocr": ocr,
        "medications": meds,
        "lab_results": labs,
        "diagnoses": diags,
        "procedures": procs,
        "medical_events": events
    }

@router.get("/health-profile")
def get_health_profile():
    """
    Returns unified aggregated personal health record for the user.
    """
    conn = get_connection()
    c = conn.cursor()

    # User / Patient Demographics
    c.execute("SELECT * FROM patients ORDER BY created_at DESC LIMIT 1")
    pat_row = c.fetchone()
    patient = dict(pat_row) if pat_row else {
        "name": "Arun Kumar",
        "age": 42,
        "gender": "Male",
        "patient_id": "AP-2026-90412"
    }

    # Medications
    c.execute("""
        SELECT m.*, d.filename, d.doc_type, d.created_at as doc_date
        FROM medications m
        JOIN documents d ON m.document_id = d.id
        ORDER BY m.created_at DESC
    """)
    medications = [dict(r) for r in c.fetchall()]

    # Lab Results
    c.execute("""
        SELECT l.*, d.filename, d.doc_type
        FROM lab_results l
        JOIN documents d ON l.document_id = d.id
        ORDER BY l.created_at DESC
    """)
    lab_results = [dict(r) for r in c.fetchall()]

    # Diagnoses
    c.execute("""
        SELECT diag.*, d.filename
        FROM diagnoses diag
        JOIN documents d ON diag.document_id = d.id
        ORDER BY diag.created_at DESC
    """)
    diagnoses = [dict(r) for r in c.fetchall()]

    # Procedures
    c.execute("SELECT * FROM procedures ORDER BY created_at DESC")
    procedures = [dict(r) for r in c.fetchall()]

    # Events
    c.execute("SELECT * FROM medical_events ORDER BY event_date DESC")
    events = [dict(r) for r in c.fetchall()]

    # Document count
    c.execute("SELECT COUNT(*) FROM documents")
    doc_count = c.fetchone()[0]

    conn.close()

    # Calculate stats
    abnormal_count = sum(1 for l in lab_results if l.get("status") in ["Below reference range", "Above reference range", "High", "Low", "Critical"])

    return {
        "patient": patient,
        "stats": {
            "total_documents": doc_count,
            "total_medications": len(medications),
            "total_lab_tests": len(lab_results),
            "abnormal_lab_tests": abnormal_count,
            "total_diagnoses": len(diagnoses),
            "total_events": len(events)
        },
        "medications": medications,
        "lab_results": lab_results,
        "diagnoses": diagnoses,
        "procedures": procedures,
        "medical_events": events
    }

@router.get("/timeline")
def get_health_timeline():
    """
    Returns ordered health timeline events.
    """
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        SELECT t.*, d.filename, d.file_type, d.ocr_confidence
        FROM health_timeline t
        JOIN documents d ON t.document_id = d.id
        ORDER BY t.event_date DESC
    """)
    rows = c.fetchall()
    timeline = []
    for r in rows:
        item = dict(r)
        if item.get("details_json"):
            try:
                item["details"] = json.loads(item["details_json"])
            except Exception:
                item["details"] = {}
        timeline.append(item)
    conn.close()
    return {"timeline": timeline, "total": len(timeline)}

@router.post("/chat", response_model=ChatResponse)
def chat_with_copilot(req: ChatRequest):
    """
    AI Health Copilot chat grounded strictly in user's records.
    """
    # Fetch full context
    profile = get_health_profile()
    result = generate_chat_reply(
        user_query=req.message,
        patient_context=profile,
        language=req.language or "English"
    )

    # Store message in DB
    try:
        conn = get_connection()
        c = conn.cursor()
        c.execute("INSERT INTO chat_history (id, session_id, role, content) VALUES (?, ?, 'user', ?)",
                  (f"msg_{uuid.uuid4().hex[:8]}", req.session_id, req.message))
        c.execute("INSERT INTO chat_history (id, session_id, role, content) VALUES (?, ?, 'assistant', ?)",
                  (f"msg_{uuid.uuid4().hex[:8]}", req.session_id, result["reply"]))
        conn.commit()
        conn.close()
    except Exception as e:
        print("Chat history save note:", e)

    return ChatResponse(
        reply=result["reply"],
        sources=result["sources"],
        grounded_entities={"medications": len(profile["medications"]), "lab_results": len(profile["lab_results"])},
        disclaimer=result["disclaimer"]
    )

@router.post("/translate", response_model=TranslationResponse)
def translate_summary(req: TranslationRequest):
    """
    Multilingual translation for summaries and explanations.
    """
    translated = translate_health_content(req.text, req.target_language)
    return TranslationResponse(
        translated_text=translated,
        target_language=req.target_language
    )

@router.get("/abha-profile")
def get_abha_profile():
    """
    ABDM / ABHA Sandbox mapping and FHIR R4 Bundle representation.
    """
    profile = get_health_profile()
    mock_abha = generate_mock_abha_profile(profile["patient"])

    # Build FHIR bundle for current data
    structured_for_fhir = {
        "patient": profile["patient"],
        "document": {"type": "Consolidated Personal Health Record", "date": "2026-09-12", "language": "English + Tamil"},
        "diagnoses": profile["diagnoses"],
        "medications": profile["medications"],
        "lab_results": profile["lab_results"],
        "medical_events": profile["medical_events"]
    }
    fhir_data = convert_to_fhir_bundle(structured_for_fhir)

    return {
        "abha": mock_abha,
        "fhir": fhir_data
    }
