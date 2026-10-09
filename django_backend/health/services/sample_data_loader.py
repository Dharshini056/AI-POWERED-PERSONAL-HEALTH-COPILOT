import uuid
import json
from documents.models import MedicalDocument, OCRResult
from health.models import (
    User, Patient, Diagnosis, Medication, LabResult, Procedure,
    Symptom, MedicalEvent, HealthTimeline
)
from ai.summarizer import generate_health_summary

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
Total Cholesterol             224.0      mg/dL      125.0 - 200.0     Above reference range
Serum Potassium               4.2        mEq/L      3.5 - 5.0         Normal
Serum Sodium                  138.0      mEq/L      135.0 - 145.0     Normal

CLINICAL INTERPRETATION / REMARKS:
- Elevated Fasting Blood Sugar and HbA1c reflect suboptimal glycemic control.
- Hemoglobin of 10.2 g/dL indicates mild microcytic anemia; clinical correlation recommended.
- Borderline hypercholesterolemia noted. Renal parameters within healthy bounds.

Dr. Ananya Sen, MD (Biochemistry)
Chief Clinical Pathologist""",
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
            "diagnoses": [
                {"name": "Mild Anemia", "date": "2026-08-18", "source_document": "Laboratory Report", "notes": "Hb 10.2 g/dL"},
                {"name": "Dyslipidemia", "date": "2026-08-18", "source_document": "Laboratory Report", "notes": "Cholesterol 224 mg/dL"}
            ],
            "medications": [],
            "lab_results": [
                {
                    "test_name": "Hemoglobin",
                    "value": "10.2",
                    "unit": "g/dL",
                    "reference_range": "12.0 - 16.0 g/dL",
                    "status": "Below reference range",
                    "date": "2026-08-18",
                    "explanation": "Hemoglobin measures oxygen carrying red blood cells. 10.2 g/dL is below the typical 12-16 reference range, indicating mild anemia.",
                    "explanation_ta": "ஹீமோகுளோபின் இரத்த சிவப்பணுக்களின் ஆக்ஸிஜன் தாங்கும் அளவைக் குறிக்கிறது. 10.2 g/dL என்பது இயல்பான வரம்பை விட குறைவு."
                },
                {
                    "test_name": "Fasting Blood Sugar",
                    "value": "142.0",
                    "unit": "mg/dL",
                    "reference_range": "70.0 - 100.0 mg/dL",
                    "status": "Above reference range",
                    "date": "2026-08-18",
                    "explanation": "Fasting blood sugar is higher than the standard upper limit of 100 mg/dL.",
                    "explanation_ta": "வெறும் வயிற்றில் இரத்த சர்க்கரை அளவு 142 mg/dL ஆக உயர்ந்துள்ளது."
                },
                {
                    "test_name": "HbA1c",
                    "value": "7.4",
                    "unit": "%",
                    "reference_range": "4.0 - 5.7 %",
                    "status": "Above reference range",
                    "date": "2026-08-18",
                    "explanation": "Reflects average blood sugar over the last 3 months. At 7.4%, it is above normal range.",
                    "explanation_ta": "HbA1c கடந்த 3 மாத சராசரி சர்க்கரை அளவைக் காட்டுகிறது (7.4%)."
                },
                {
                    "test_name": "Serum Creatinine",
                    "value": "0.95",
                    "unit": "mg/dL",
                    "reference_range": "0.6 - 1.2 mg/dL",
                    "status": "Normal",
                    "date": "2026-08-18",
                    "explanation": "Kidney filtration indicator is within healthy limits.",
                    "explanation_ta": "சிறுநீரக செயல்பாட்டு அளவு சீராக உள்ளது."
                },
                {
                    "test_name": "Total Cholesterol",
                    "value": "224.0",
                    "unit": "mg/dL",
                    "reference_range": "125.0 - 200.0 mg/dL",
                    "status": "Above reference range",
                    "date": "2026-08-18",
                    "explanation": "Serum cholesterol is modestly above 200 mg/dL reference limit.",
                    "explanation_ta": "கொலஸ்ட்ரால் அளவு அனுமதிக்கப்பட்ட அளவை விட சற்றே அதிகமாக உள்ளது."
                }
            ],
            "procedures": [],
            "symptoms": [],
            "medical_events": [
                {
                    "event_type": "Laboratory Report",
                    "title": "Biochemistry & CBC Panel Done",
                    "description": "Routine diagnostic workup for diabetes and lipid profile.",
                    "doctor_name": "Dr. Ananya Sen, MD",
                    "facility_name": "Metropolis Healthcare Clinical Laboratory",
                    "event_date": "2026-08-18"
                }
            ],
            "important_findings": [
                "Hemoglobin: 10.2 g/dL (Below reference range)",
                "Fasting Blood Sugar: 142.0 mg/dL (Above reference range)",
                "HbA1c: 7.4% (Above reference range)",
                "Total Cholesterol: 224.0 mg/dL (Above reference range)"
            ]
        }
    },
    {
        "id": "sample-doc-03",
        "filename": "Discharge_Summary_Daycare_Endoscopy.pdf",
        "file_type": "application/pdf",
        "doc_type": "Discharge Summary",
        "detected_language": "English",
        "ocr_confidence": 0.97,
        "date": "2026-09-02",
        "raw_text": """SIMS MULTISPECIALTY HOSPITALS
DEPARTMENT OF GASTROENTEROLOGY
DISCHARGE SUMMARY (DAYCARE ADMISSION)

PATIENT DEMOGRAPHICS:
Patient: Arun Kumar      Age: 42      Sex: Male
Admission Date: 02-Sep-2026    Discharge Date: 02-Sep-2026
IP Number: IP-94180            UHID: AP-2026-90412

FINAL DIAGNOSIS:
Gastroesophageal Reflux Disease (GERD) with Mild Antral Gastritis

PROCEDURE PERFORMED:
Upper Gastrointestinal Endoscopy under conscious sedation.
Findings: Normal esophagus, mild mucosal erythema in gastric antrum. No ulceration or bleeding. Rapid urease test negative for H. pylori.

DISCHARGE MEDICATIONS:
1. Tab. Pantoprazole 40 mg
   Dosage: 40 mg
   Frequency: Once daily
   Duration: 14 days
   Timing: Morning 30 mins Before Food

2. Syr. Sucralfate 10 ml
   Dosage: 10 ml
   Frequency: Thrice daily
   Duration: 7 days
   Timing: 1 hour after meals

FOLLOW-UP ADVICE:
- Avoid spicy, deeply fried meals and late-night snacking.
- Review with Gastroenterology OPD if dyspepsia persists after 2 weeks.

Dr. K. Venkatesh, MD, DM
Consultant Gastroenterologist""",
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
                "date": "2026-09-02",
                "ocr_confidence": 0.97
            },
            "diagnoses": [
                {"name": "Gastroesophageal Reflux Disease (GERD)", "date": "2026-09-02", "source_document": "Discharge Summary", "notes": "Mild antral gastritis"}
            ],
            "medications": [
                {
                    "name": "Pantoprazole",
                    "dose": "40 mg",
                    "dosage_unit": "mg",
                    "frequency": "Once daily",
                    "route": "Oral",
                    "duration": "14 days",
                    "instructions": "Morning 30 mins before food",
                    "before_after_food": "Before food",
                    "source_document": "Discharge Summary — 02 Sep 2026"
                },
                {
                    "name": "Sucralfate",
                    "dose": "10 ml",
                    "dosage_unit": "ml",
                    "frequency": "Thrice daily",
                    "route": "Oral",
                    "duration": "7 days",
                    "instructions": "1 hour after meals",
                    "before_after_food": "After food",
                    "source_document": "Discharge Summary — 02 Sep 2026"
                }
            ],
            "lab_results": [],
            "procedures": [
                {
                    "procedure": "Upper Gastrointestinal Endoscopy",
                    "date": "2026-09-02",
                    "hospital": "SIMS Multispecialty Hospitals",
                    "notes": "Mild mucosal erythema in gastric antrum. No active bleeding."
                }
            ],
            "symptoms": [
                {"symptom": "Heartburn", "severity": "Moderate", "duration": "1 month"}
            ],
            "medical_events": [
                {
                    "event_type": "Discharge Summary",
                    "title": "Daycare Endoscopy & Discharge",
                    "description": "Upper GI endoscopy performed with discharge on same day with acid suppression therapy.",
                    "doctor_name": "Dr. K. Venkatesh, MD, DM",
                    "facility_name": "SIMS Multispecialty Hospitals",
                    "event_date": "2026-09-02"
                }
            ],
            "important_findings": [
                "Underwent Upper GI Endoscopy showing mild antral gastritis",
                "Started on Pantoprazole 40mg before breakfast for 14 days"
            ]
        }
    },
    {
        "id": "sample-doc-04",
        "filename": "Tamil_Prescription_Diabetes_Followup.png",
        "file_type": "image/png",
        "doc_type": "Prescription",
        "detected_language": "Bilingual (English + Tamil)",
        "ocr_confidence": 0.94,
        "date": "2026-09-12",
        "raw_text": """மீனாட்சி மருத்துவமனை (Meenakshi Hospital)
பொது மருத்துவம் மற்றும் நீரிழிவு பிரிவு
மருத்துவர்: Dr. R. செல்வம், MD
தேதி: 12-09-2026

நோயாளி விவரங்கள் (Patient Details):
நோயாளி பெயர்: Arun Kumar
வயது: 42 ஆண்டுகள்    பாலினம்: ஆண்
பதிவு எண்: MH-2026-4410

மருத்துவ முடிவு (Diagnosis):
நீரிழிவு நோய் பின்தொடர்தல் (Type 2 Diabetes Mellitus Follow-up)

பரிந்துரைக்கப்பட்ட மருந்துகள் (Prescribed Medications):
1. மருந்து: Metformin
   அளவு: 500 mg
   உட்கொள்ளும் முறை: 1-0-1 (இரண்டு முறை)
   கால அளவு: 30 நாட்கள்
   குறிப்பு: உணவுக்குப் பின் (After food)

2. மருந்து: Glimepiride
   அளவு: 1 mg
   உட்கொள்ளும் முறை: 1-0-0 (காலை ஒரு முறை)
   கால அளவு: 30 நாட்கள்
   குறிப்பு: உணவுக்கு முன் (Before breakfast)

3. மருந்து: Atorvastatin
   அளவு: 10 mg
   உட்கொள்ளும் முறை: 0-0-1 (இரவு ஒரு முறை)
   கால அளவு: 30 நாட்கள்
   குறிப்பு: இரவு உணவுக்குப் பின்

மருத்துவர் ஆலோசனை:
- உணவு கட்டுப்பாடு மற்றும் உடற்பயிற்சி தொடரவும்.
- 1 மாதம் கழித்து மீண்டும் இரத்த சர்க்கரை பரிசோதனை செய்து வரவும்.

Dr. R. Selvam, MD
சீஃப் டயாபடாலஜிஸ்ட்""",
        "structured_data": {
            "patient": {
                "name": "Arun Kumar",
                "age": 42,
                "gender": "Male",
                "date_of_birth": "1984-05-14",
                "patient_id": "MH-2026-4410"
            },
            "document": {
                "type": "Prescription",
                "language": "Bilingual (English + Tamil)",
                "date": "2026-09-12",
                "ocr_confidence": 0.94
            },
            "diagnoses": [
                {"name": "Type 2 Diabetes Mellitus (Follow-up)", "date": "2026-09-12", "source_document": "Tamil Prescription", "notes": "Glimepiride added"}
            ],
            "medications": [
                {
                    "name": "Metformin",
                    "dose": "500 mg",
                    "dosage_unit": "mg",
                    "frequency": "Twice daily",
                    "route": "Oral",
                    "duration": "30 days",
                    "instructions": "உணவுக்குப் பின் (After food)",
                    "before_after_food": "After food",
                    "source_document": "Meenakshi Hospital — 12 Sep 2026"
                },
                {
                    "name": "Glimepiride",
                    "dose": "1 mg",
                    "dosage_unit": "mg",
                    "frequency": "Once daily",
                    "route": "Oral",
                    "duration": "30 days",
                    "instructions": "உணவுக்கு முன் (Before breakfast)",
                    "before_after_food": "Before food",
                    "source_document": "Meenakshi Hospital — 12 Sep 2026"
                },
                {
                    "name": "Atorvastatin",
                    "dose": "10 mg",
                    "dosage_unit": "mg",
                    "frequency": "Once daily",
                    "route": "Oral",
                    "duration": "30 days",
                    "instructions": "இரவு உணவுக்குப் பின் (After dinner)",
                    "before_after_food": "After food",
                    "source_document": "Meenakshi Hospital — 12 Sep 2026"
                }
            ],
            "lab_results": [],
            "procedures": [],
            "symptoms": [],
            "medical_events": [
                {
                    "event_type": "Prescription",
                    "title": "Bilingual Tamil Follow-up Prescription",
                    "description": "Diabetes review by Dr. R. Selvam with addition of Glimepiride and Atorvastatin.",
                    "doctor_name": "Dr. R. Selvam, MD",
                    "facility_name": "Meenakshi Hospital",
                    "event_date": "2026-09-12"
                }
            ],
            "important_findings": [
                "Tamil prescription successfully extracted via multilingual OCR",
                "Dual oral hypoglycemic regimen with Metformin & Glimepiride",
                "Atorvastatin added for lipid optimization"
            ]
        }
    }
]

def load_sample_dataset_into_django():
    """
    Seeds the standard synthetic clinical records into Django database.
    """
    # Ensure default user exists
    User.objects.get_or_create(
        id='usr_demo_01',
        defaults={
            'name': 'Arun Kumar',
            'email': 'arun.kumar@demo-health.org',
            'abha_id': '91-4521-8934-1022'
        }
    )

    for sample in SAMPLE_DOCUMENTS:
        doc_id = sample["id"]
        # Skip if already exists
        if MedicalDocument.objects.filter(id=doc_id).exists():
            continue

        raw_text = sample["raw_text"]
        struct = sample["structured_data"]
        summaries = generate_health_summary(struct)

        doc = MedicalDocument.objects.create(
            id=doc_id,
            user_id='usr_demo_01',
            filename=sample["filename"],
            file_path=f"uploads/{sample['filename']}",
            file_type=sample["file_type"],
            file_size=2048,
            doc_type=sample["doc_type"],
            status="processed",
            detected_language=sample["detected_language"],
            ocr_confidence=sample["ocr_confidence"],
            summary_en=summaries.get("summary_en"),
            summary_ta=summaries.get("summary_ta")
        )

        OCRResult.objects.create(
            id=f"ocr-{doc_id}",
            document=doc,
            raw_text=raw_text,
            cleaned_text=raw_text,
            detected_language=sample["detected_language"],
            confidence_score=sample["ocr_confidence"],
            processing_time_ms=420,
            engine_name="RapidOCR-PaddleONNX + OpenCV CLAHE"
        )

        p = struct["patient"]
        Patient.objects.create(
            id=f"pat-{doc_id}",
            document=doc,
            name=p.get("name"),
            age=p.get("age"),
            gender=p.get("gender"),
            date_of_birth=p.get("date_of_birth"),
            patient_id_ref=p.get("patient_id")
        )

        for d in struct.get("diagnoses", []):
            Diagnosis.objects.create(
                id=f"diag-{uuid.uuid4().hex[:8]}",
                document=doc,
                diagnosis_name=d.get("name"),
                date=d.get("date"),
                source_document=d.get("source_document"),
                notes=d.get("notes")
            )

        for m in struct.get("medications", []):
            Medication.objects.create(
                id=f"med-{uuid.uuid4().hex[:8]}",
                document=doc,
                name=m.get("name"),
                dose=m.get("dose"),
                dosage_unit=m.get("dosage_unit"),
                frequency=m.get("frequency"),
                route=m.get("route", "Oral"),
                duration=m.get("duration"),
                instructions=m.get("instructions"),
                before_after_food=m.get("before_after_food")
            )

        for l in struct.get("lab_results", []):
            LabResult.objects.create(
                id=f"lab-{uuid.uuid4().hex[:8]}",
                document=doc,
                test_name=l.get("test_name"),
                value=str(l.get("value")),
                unit=l.get("unit"),
                reference_range=l.get("reference_range"),
                status=l.get("status"),
                date=l.get("date"),
                explanation_en=l.get("explanation"),
                explanation_ta=l.get("explanation_ta")
            )

        for pr in struct.get("procedures", []):
            Procedure.objects.create(
                id=f"proc-{uuid.uuid4().hex[:8]}",
                document=doc,
                procedure_name=pr.get("procedure"),
                date=pr.get("date"),
                hospital=pr.get("hospital"),
                notes=pr.get("notes")
            )

        for ev in struct.get("medical_events", []):
            MedicalEvent.objects.create(
                id=f"ev-{uuid.uuid4().hex[:8]}",
                document=doc,
                event_type=ev.get("event_type"),
                title=ev.get("title"),
                description=ev.get("description"),
                doctor_name=ev.get("doctor_name"),
                facility_name=ev.get("facility_name"),
                event_date=ev.get("event_date")
            )

            HealthTimeline.objects.create(
                id=f"time-{uuid.uuid4().hex[:8]}",
                document=doc,
                event_date=ev.get("event_date") or sample["date"],
                title=ev.get("title"),
                category=sample["doc_type"],
                summary=ev.get("description"),
                details_json=json.dumps(struct)
            )

    print("Demo dataset verified and loaded successfully in Django!")
