import os
import uuid
import json
from typing import Dict, Any, List

SAMPLE_DOCUMENTS = [
    {
        "id": "sample-doc-01",
        "filename": "Prescription_Metformin_2026.pdf",
        "file_type": "application/pdf",
        "doc_type": "Prescription",
        "detected_language": "English",
        "ocr_confidence": 0.96,
        "date": "2026-08-12",
        "raw_text": """APOLLO MULTISPECIALITY HOSPITALS
DEPARTMENT OF INTERNAL MEDICINE
Dr. S. Ramanathan, MD (Gen Med)
Registration No: TN-MC-48291
Date: 12 Aug 2026

PATIENT DETAILS:
Patient Name: Arun Kumar
Age: 42 Years    Gender: Male
Patient ID / UHID: AP-2026-90412

DIAGNOSIS / IMPRESSION:
Type 2 Diabetes Mellitus with Essential Hypertension

Rx (PRESCRIPTION):
1. Tab. Metformin 500 mg
   Dosage: 500 mg
   Frequency: Twice daily (1-0-1)
   Duration: 30 days
   Timing: After food (PC)

2. Tab. Telmisartan 40 mg
   Dosage: 40 mg
   Frequency: Once daily (1-0-0)
   Duration: 30 days
   Timing: Morning after food

3. Cap. Vitamin D3 60,000 IU
   Dosage: 60,000 IU
   Frequency: Once weekly
   Duration: 8 weeks
   Timing: After dinner with milk

ADVICE:
- Restrict refined carbohydrates and dietary salt.
- Daily 30 mins brisk walking.
- Review after 1 month with Fasting Blood Sugar and HbA1c reports.

Dr. S. Ramanathan, MD
Internal Medicine Specialist""",
        "structured_data": {
            "patient": {
                "name": "Arun Kumar",
                "age": 42,
                "gender": "Male",
                "date_of_birth": "1984-05-14",
                "patient_id": "AP-2026-90412"
            },
            "document": {
                "type": "Prescription",
                "language": "English",
                "date": "2026-08-12",
                "ocr_confidence": 0.96
            },
            "diagnoses": [
                {"name": "Type 2 Diabetes Mellitus", "date": "2026-08-12", "source_document": "Prescription", "notes": "Under medical management"},
                {"name": "Essential Hypertension", "date": "2026-08-12", "source_document": "Prescription", "notes": "Mild elevated BP"}
            ],
            "medications": [
                {
                    "name": "Metformin",
                    "dose": "500 mg",
                    "dosage_unit": "mg",
                    "frequency": "Twice daily",
                    "route": "Oral",
                    "duration": "30 days",
                    "instructions": "After food",
                    "before_after_food": "After food",
                    "source_document": "Prescription — 12 Aug 2026"
                },
                {
                    "name": "Telmisartan",
                    "dose": "40 mg",
                    "dosage_unit": "mg",
                    "frequency": "Once daily",
                    "route": "Oral",
                    "duration": "30 days",
                    "instructions": "Morning after food",
                    "before_after_food": "After food",
                    "source_document": "Prescription — 12 Aug 2026"
                },
                {
                    "name": "Vitamin D3",
                    "dose": "60,000 IU",
                    "dosage_unit": "IU",
                    "frequency": "Once weekly",
                    "route": "Oral",
                    "duration": "8 weeks",
                    "instructions": "After dinner with milk",
                    "before_after_food": "After food",
                    "source_document": "Prescription — 12 Aug 2026"
                }
            ],
            "lab_results": [],
            "procedures": [],
            "symptoms": [
                {"symptom": "Fatigue", "severity": "Mild", "duration": "2 weeks"}
            ],
            "medical_events": [
                {
                    "event_type": "Prescription",
                    "title": "Outpatient Prescription Issued",
                    "description": "Prescription issued for Glycemic and Blood Pressure management by Dr. S. Ramanathan.",
                    "doctor_name": "Dr. S. Ramanathan, MD",
                    "facility_name": "Apollo Multispeciality Hospitals",
                    "event_date": "2026-08-12"
                }
            ],
            "important_findings": [
                "Prescribed Metformin 500mg twice daily and Telmisartan 40mg daily",
                "Follow-up advised with HbA1c and Blood Sugar tests"
            ]
        }
    },
    {
        "id": "sample-doc-02",
        "filename": "Lab_Report_Biochemistry_CBC.pdf",
        "file_type": "application/pdf",
        "doc_type": "Laboratory Report",
        "detected_language": "English",
        "ocr_confidence": 0.98,
        "date": "2026-08-18",
        "raw_text": """METROPOLIS HEALTHCARE CLINICAL LABORATORY
ACCREDITED BY NABL & CAP
Patient Name: Arun Kumar        Age/Sex: 42 Y / Male
Referred By: Dr. S. Ramanathan  Lab Ref: MET-78401
Sample Collected: 18-Aug-2026   Report Date: 18-Aug-2026

COMPLETE BLOOD COUNT & BIOCHEMISTRY REPORT

TEST NAME                     RESULT     UNIT       REFERENCE RANGE   STATUS
-----------------------------------------------------------------------------
Hemoglobin                    10.2       g/dL       12.0 - 16.0       Below reference range
Fasting Blood Sugar           142.0      mg/dL      70.0 - 100.0      Above reference range
HbA1c Glycated Hemoglobin     7.4        %          4.0 - 5.7         Above reference range
Serum Creatinine              0.95       mg/dL      0.6 - 1.2         Normal
Total Cholesterol             186.0      mg/dL      125.0 - 200.0     Normal
WBC Count                     6800       /mcL       4000 - 11000      Normal
Platelet Count                240000     /mcL       150000 - 450000   Normal

CLINICAL NOTES:
Hemoglobin is mildly below the reference interval.
Fasting plasma glucose and HbA1c reflect elevated glycemic status.

Pathologist: Dr. K. Meenakshi, MD (Path)""",
        "structured_data": {
            "patient": {
                "name": "Arun Kumar",
                "age": 42,
                "gender": "Male",
                "date_of_birth": "1984-05-14",
                "patient_id": "AP-2026-90412"
            },
            "document": {
                "type": "Laboratory Report",
                "language": "English",
                "date": "2026-08-18",
                "ocr_confidence": 0.98
            },
            "diagnoses": [],
            "medications": [],
            "lab_results": [
                {
                    "test_name": "Hemoglobin",
                    "value": "10.2",
                    "unit": "g/dL",
                    "reference_range": "12.0 – 16.0 g/dL",
                    "status": "Below reference range",
                    "date": "2026-08-18",
                    "explanation": "Hemoglobin measures oxygen-carrying proteins in your red blood cells. This value (10.2 g/dL) is below the reference range (12.0 – 16.0 g/dL) shown in the report. There can be several reasons for this result, including mild nutritional iron deficiency, and a healthcare professional should interpret it in context.",
                    "explanation_ta": "ஹீமோகுளோபின் என்பது இரத்த சிவப்பணுக்களில் உள்ள ஆக்ஸிஜன் தாங்கும் புரதமாகும். அறிக்கையில் கொடுக்கப்பட்டுள்ள reference range (12.0 – 16.0 g/dL)-ஐ விட இந்த மதிப்பு (10.2 g/dL) குறைவாக உள்ளது. இதற்கான காரணத்தை மருத்துவர் உங்கள் மற்ற மருத்துவ தகவல்களுடன் சேர்த்து மதிப்பீடு செய்ய வேண்டும்."
                },
                {
                    "test_name": "Fasting Blood Sugar",
                    "value": "142.0",
                    "unit": "mg/dL",
                    "reference_range": "70.0 – 100.0 mg/dL",
                    "status": "Above reference range",
                    "date": "2026-08-18",
                    "explanation": "Fasting Blood Sugar measures glucose levels after an overnight fast. This value (142.0 mg/dL) is above the reference range (70.0 – 100.0 mg/dL). There can be several reasons for this result, and your doctor should evaluate it in context.",
                    "explanation_ta": "இரத்த சர்க்கரை அளவு (Fasting Blood Sugar) 142.0 mg/dL என பதிவாகியுள்ளது, இது பரிந்துரைக்கப்பட்ட வரம்பை விட அதிகமாக உள்ளது. மருத்துவர் மூலம் மதிப்பாய்வு செய்ய பரிந்துரைக்கப்படுகிறது."
                },
                {
                    "test_name": "HbA1c",
                    "value": "7.4",
                    "unit": "%",
                    "reference_range": "4.0 – 5.7 %",
                    "status": "Above reference range",
                    "date": "2026-08-18",
                    "explanation": "HbA1c measures 3-month average blood glucose. This value (7.4%) is above the non-diabetic reference range (4.0 – 5.7%). A healthcare professional should interpret it in context of your treatment plan.",
                    "explanation_ta": "HbA1c (சராசரி இரத்த சர்க்கரை அளவு) 7.4% ஆக உள்ளது. இது நிர்ணயிக்கப்பட்ட வரம்பை விட அதிகமாக உள்ளது. மருத்துவருடன் பரிசீலிக்கவும்."
                },
                {
                    "test_name": "Serum Creatinine",
                    "value": "0.95",
                    "unit": "mg/dL",
                    "reference_range": "0.6 – 1.2 mg/dL",
                    "status": "Normal",
                    "date": "2026-08-18",
                    "explanation": "Serum Creatinine is an indicator of kidney filtration health and is within standard normal limits.",
                    "explanation_ta": "சீரம் கிரியேட்டினின் அளவு 0.95 mg/dL என இயல்பான வரம்பிற்குள் உள்ளது."
                },
                {
                    "test_name": "Total Cholesterol",
                    "value": "186.0",
                    "unit": "mg/dL",
                    "reference_range": "125.0 – 200.0 mg/dL",
                    "status": "Normal",
                    "date": "2026-08-18",
                    "explanation": "Total Cholesterol is within the optimal standard reference range.",
                    "explanation_ta": "மொத்த கொலஸ்ட்ரால் அளவு 186.0 mg/dL என இயல்பான வரம்பிற்குள் உள்ளது."
                }
            ],
            "procedures": [],
            "symptoms": [],
            "medical_events": [
                {
                    "event_type": "Laboratory Report",
                    "title": "Comprehensive Blood Panel Completed",
                    "description": "CBC, Fasting Blood Sugar, HbA1c, Renal function, and Lipid profile processed by Metropolis Healthcare.",
                    "doctor_name": "Dr. K. Meenakshi, MD",
                    "facility_name": "Metropolis Healthcare Diagnostics",
                    "event_date": "2026-08-18"
                }
            ],
            "important_findings": [
                "Hemoglobin: 10.2 g/dL (Below reference range)",
                "Fasting Blood Sugar: 142.0 mg/dL (Above reference range)",
                "HbA1c: 7.4% (Above reference range)"
            ]
        }
    },
    {
        "id": "sample-doc-03",
        "filename": "Discharge_Summary_DayCare.pdf",
        "file_type": "application/pdf",
        "doc_type": "Discharge Summary",
        "detected_language": "English",
        "ocr_confidence": 0.94,
        "date": "2026-09-03",
        "raw_text": """CITY HEALTH MULTISPECIALITY HOSPITAL
DAY CARE DISCHARGE SUMMARY
Admission Date: 03-Sep-2026 (08:30 AM)
Discharge Date: 03-Sep-2026 (05:00 PM)

Patient Name: Arun Kumar        Age: 42 Y    Sex: Male
Consultant: Dr. V. Sundaram, MS, MCh (Surgical Gastroenterology)
IP No: IP-2026-44189

DIAGNOSIS AT DISCHARGE:
Symptomatic Cholelithiasis (Gallbladder calculus)

PROCEDURE PERFORMED:
Diagnostic Ultrasound & Elective Pre-op Evaluation
Date of Procedure: 03-Sep-2026
Facility: City Health Multispeciality Hospital

SUMMARY OF CLINICAL COURSE:
Patient admitted for routine day-care abdominal evaluation. Vital parameters stable.
ECG and chest radiography within normal physiological limits.
Discharged in clinically stable status.

DISCHARGE MEDICATIONS:
1. Tab. Pantoprazole 40 mg — Once daily (1-0-0) before breakfast for 14 days.
2. Tab. Paracetamol 650 mg — As needed (SOS) for mild abdominal discomfort.

FOLLOW-UP ADVICE:
Follow up in Surgical OPD on 15-Sep-2026.""",
        "structured_data": {
            "patient": {
                "name": "Arun Kumar",
                "age": 42,
                "gender": "Male",
                "date_of_birth": "1984-05-14",
                "patient_id": "AP-2026-90412"
            },
            "document": {
                "type": "Discharge Summary",
                "language": "English",
                "date": "2026-09-03",
                "ocr_confidence": 0.94
            },
            "diagnoses": [
                {"name": "Symptomatic Cholelithiasis", "date": "2026-09-03", "source_document": "Discharge Summary", "notes": "Under conservative observation"}
            ],
            "medications": [
                {
                    "name": "Pantoprazole",
                    "dose": "40 mg",
                    "dosage_unit": "mg",
                    "frequency": "Once daily",
                    "route": "Oral",
                    "duration": "14 days",
                    "instructions": "Before breakfast",
                    "before_after_food": "Before food",
                    "source_document": "Discharge Summary — 03 Sep 2026"
                },
                {
                    "name": "Paracetamol",
                    "dose": "650 mg",
                    "dosage_unit": "mg",
                    "frequency": "As needed (SOS)",
                    "route": "Oral",
                    "duration": "5 days",
                    "instructions": "After food if pain occurs",
                    "before_after_food": "After food",
                    "source_document": "Discharge Summary — 03 Sep 2026"
                }
            ],
            "lab_results": [],
            "procedures": [
                {
                    "procedure": "Diagnostic Ultrasound & Pre-op Evaluation",
                    "date": "2026-09-03",
                    "hospital": "City Health Multispeciality Hospital",
                    "notes": "Uneventful day-care evaluation"
                }
            ],
            "symptoms": [
                {"symptom": "Mild Epigastric Discomfort", "severity": "Mild", "duration": "Resolved"}
            ],
            "medical_events": [
                {
                    "event_type": "Discharge Summary",
                    "title": "Day Care Clinical Evaluation",
                    "description": "Patient evaluated for cholelithiasis, advised lifestyle modifications and review.",
                    "doctor_name": "Dr. V. Sundaram, MS",
                    "facility_name": "City Health Multispeciality Hospital",
                    "event_date": "2026-09-03"
                }
            ],
            "important_findings": [
                "Diagnosed with Symptomatic Cholelithiasis",
                "Prescribed Pantoprazole 40mg and Paracetamol SOS"
            ]
        }
    },
    {
        "id": "sample-doc-04",
        "filename": "Tamil_English_Bilingual_Prescription.png",
        "file_type": "image/png",
        "doc_type": "Prescription",
        "detected_language": "Bilingual (English + Tamil)",
        "ocr_confidence": 0.92,
        "date": "2026-09-12",
        "raw_text": """சாந்தி நல்வாழ்வு மையம் (SANTHI HEALTH CLINIC)
மருத்துவர்: டாக்டர். ஆர். கார்த்திக், MBBS, MD
Dr. R. Karthik, MBBS, MD
தேதி / Date: 12-Sep-2026

நோயாளி விவரங்கள் / Patient Info:
பெயர் / Name: அருண் குமார் (Arun Kumar)
வயது / Age: 42 ஆண்டுகள்    பாலினம் / Sex: ஆண் (Male)

மருத்துவக் குறிப்பு / Diagnosis:
நீரிழிவு நோய் மற்றும் இரத்த அழுத்தம் (Type 2 Diabetes & Hypertension)

மருந்து விவரங்கள் / Medication Orders:
1. மருந்து: Metformin 500 mg
   அளவு: 500 mg
   மாத்திரை உட்கொள்ளும் முறை: காலை 1 / இரவு 1 (Twice daily, 1-0-1)
   கால அளவு: 30 நாட்கள் (30 days)
   குறிப்பு: உணவுக்குப் பின் (After food)

2. மருந்து: Atorvastatin 10 mg
   அளவு: 10 mg
   மாத்திரை உட்கொள்ளும் முறை: இரவு 1 (Once daily at night, 0-0-1)
   கால அளவு: 30 நாட்கள் (30 days)
   குறிப்பு: உணவுக்குப் பின் (After dinner)

3. மருந்து: Pantoprazole 40 mg
   அளவு: 40 mg
   மாத்திரை உட்கொள்ளும் முறை: காலை 1 (Once daily morning)
   கால அளவு: 15 நாட்கள் (15 days)
   குறிப்பு: உணவுக்கு முன் (Before food)

மருத்துவர் கையொப்பம் / Doctor Signature:
Dr. R. Karthik, MD""",
        "structured_data": {
            "patient": {
                "name": "Arun Kumar (அருண் குமார்)",
                "age": 42,
                "gender": "Male",
                "date_of_birth": "1984-05-14",
                "patient_id": "SHC-2026-118"
            },
            "document": {
                "type": "Prescription",
                "language": "Bilingual (English + Tamil)",
                "date": "2026-09-12",
                "ocr_confidence": 0.92
            },
            "diagnoses": [
                {"name": "Type 2 Diabetes & Hypertension (நீரிழிவு நோய் மற்றும் இரத்த அழுத்தம்)", "date": "2026-09-12", "source_document": "Bilingual Prescription", "notes": "Tamil-English bilingual consult"}
            ],
            "medications": [
                {
                    "name": "Metformin",
                    "dose": "500 mg",
                    "dosage_unit": "mg",
                    "frequency": "Twice daily",
                    "route": "Oral",
                    "duration": "30 days",
                    "instructions": "After food (உணவுக்குப் பின்)",
                    "before_after_food": "After food",
                    "source_document": "Bilingual Prescription — 12 Sep 2026"
                },
                {
                    "name": "Atorvastatin",
                    "dose": "10 mg",
                    "dosage_unit": "mg",
                    "frequency": "Once daily at night",
                    "route": "Oral",
                    "duration": "30 days",
                    "instructions": "After dinner (இரவு உணவுக்குப் பின்)",
                    "before_after_food": "After food",
                    "source_document": "Bilingual Prescription — 12 Sep 2026"
                },
                {
                    "name": "Pantoprazole",
                    "dose": "40 mg",
                    "dosage_unit": "mg",
                    "frequency": "Once daily",
                    "route": "Oral",
                    "duration": "15 days",
                    "instructions": "Before food (உணவுக்கு முன்)",
                    "before_after_food": "Before food",
                    "source_document": "Bilingual Prescription — 12 Sep 2026"
                }
            ],
            "lab_results": [],
            "procedures": [],
            "symptoms": [],
            "medical_events": [
                {
                    "event_type": "Prescription",
                    "title": "Bilingual Consultation & Refill",
                    "description": "Prescription issued in English and Tamil for metabolic care by Dr. R. Karthik.",
                    "doctor_name": "Dr. R. Karthik, MD",
                    "facility_name": "Santhi Health Clinic, Chennai",
                    "event_date": "2026-09-12"
                }
            ],
            "important_findings": [
                "Bilingual Tamil + English Prescription parsed accurately",
                "Metformin 500mg, Atorvastatin 10mg, Pantoprazole 40mg extracted"
            ]
        }
    }
]

def load_sample_dataset_into_db():
    """
    Seeds database with the 4 synthetic medical records.
    """
    from .database import get_connection
    from .summary_generator import generate_health_summary

    conn = get_connection()
    cursor = conn.cursor()

    for sample in SAMPLE_DOCUMENTS:
        doc_id = sample["id"]
        # Check if already exists
        cursor.execute("SELECT id FROM documents WHERE id = ?", (doc_id,))
        if cursor.fetchone():
            continue

        raw_text = sample["raw_text"]
        struct = sample["structured_data"]
        summaries = generate_health_summary(struct)

        cursor.execute("""
            INSERT INTO documents (id, user_id, filename, file_path, file_type, file_size, doc_type, status, detected_language, ocr_confidence, summary_en, summary_ta)
            VALUES (?, 'usr_demo_01', ?, ?, ?, ?, ?, 'processed', ?, ?, ?, ?)
        """, (
            doc_id,
            sample["filename"],
            os.path.join("uploads", sample["filename"]),
            sample["file_type"],
            len(raw_text.encode('utf-8')),
            sample["doc_type"],
            sample["detected_language"],
            sample["ocr_confidence"],
            summaries["summary_en"],
            summaries["summary_ta"]
        ))

        # OCR result
        cursor.execute("""
            INSERT INTO ocr_results (id, document_id, raw_text, cleaned_text, detected_language, confidence_score, processing_time_ms, engine_name)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            f"ocr-{doc_id}",
            doc_id,
            raw_text,
            raw_text,
            sample["detected_language"],
            sample["ocr_confidence"],
            420,
            "RapidOCR-PaddleONNX + OpenCV CLAHE"
        ))

        # Patient
        p = struct["patient"]
        cursor.execute("""
            INSERT INTO patients (id, document_id, name, age, gender, date_of_birth, patient_id_ref)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            f"pat-{doc_id}",
            doc_id,
            p.get("name"),
            p.get("age"),
            p.get("gender"),
            p.get("date_of_birth"),
            p.get("patient_id")
        ))

        # Diagnoses
        for d in struct.get("diagnoses", []):
            cursor.execute("""
                INSERT INTO diagnoses (id, document_id, diagnosis_name, date, source_document, notes)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                f"diag-{uuid.uuid4().hex[:8]}",
                doc_id,
                d.get("name"),
                d.get("date"),
                d.get("source_document"),
                d.get("notes")
            ))

        # Medications
        for m in struct.get("medications", []):
            cursor.execute("""
                INSERT INTO medications (id, document_id, name, dose, dosage_unit, frequency, route, duration, instructions, before_after_food)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                f"med-{uuid.uuid4().hex[:8]}",
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

        # Lab results
        for l in struct.get("lab_results", []):
            cursor.execute("""
                INSERT INTO lab_results (id, document_id, test_name, value, unit, reference_range, status, date, explanation_en, explanation_ta)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                f"lab-{uuid.uuid4().hex[:8]}",
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

        # Procedures
        for pr in struct.get("procedures", []):
            cursor.execute("""
                INSERT INTO procedures (id, document_id, procedure_name, date, hospital, notes)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                f"proc-{uuid.uuid4().hex[:8]}",
                doc_id,
                pr.get("procedure"),
                pr.get("date"),
                pr.get("hospital"),
                pr.get("notes")
            ))

        # Medical events & Timeline
        for ev in struct.get("medical_events", []):
            ev_id = f"ev-{uuid.uuid4().hex[:8]}"
            cursor.execute("""
                INSERT INTO medical_events (id, document_id, event_type, title, description, doctor_name, facility_name, event_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                ev_id,
                doc_id,
                ev.get("event_type"),
                ev.get("title"),
                ev.get("description"),
                ev.get("doctor_name"),
                ev.get("facility_name"),
                ev.get("event_date")
            ))

            cursor.execute("""
                INSERT INTO health_timeline (id, document_id, event_date, title, category, summary, details_json)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                f"time-{uuid.uuid4().hex[:8]}",
                doc_id,
                ev.get("event_date") or sample["date"],
                ev.get("title"),
                sample["doc_type"],
                ev.get("description"),
                json.dumps(struct)
            ))

    conn.commit()
    conn.close()
