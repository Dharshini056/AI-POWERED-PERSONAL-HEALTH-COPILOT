# 🩺 AI Personal Health Copilot

> **Understand your health. Organize your records. Stay informed.**
> A multilingual healthcare copilot with high-accuracy OCR, clinical entity extraction, safe simple-language summaries, unified timeline, and FHIR / ABDM data standardization.

[![Django REST Framework](https://img.shields.io/badge/Backend-Django%20REST%20Framework-092E20.svg?logo=django&logoColor=white)](https://www.django-rest-framework.org/)
[![React](https://img.shields.io/badge/Frontend-React%2019-61DAFB.svg?logo=react&logoColor=black)](https://react.dev)
[![Vite](https://img.shields.io/badge/Bundler-Vite-646CFF.svg?logo=vite&logoColor=white)](https://vitejs.dev)
[![OCR](https://img.shields.io/badge/OCR-RapidOCR%20(PaddleONNX)-FF6F00.svg)](https://github.com/RapidAI/RapidOCR)
[![FHIR](https://img.shields.io/badge/Standards-HL7%20FHIR%20R4%20%7C%20ABDM-E91E63.svg)](https://hl7.org/fhir/)

---

## 📌 1. Architecture Overview

The system backend is built with **Django & Django REST Framework** connected to a modern **React + Vite** frontend.

```
React / Vite Frontend (http://localhost:5174)
        |
        | REST API (Proxied: /api → http://127.0.0.1:8001)
        ↓
Django + Django REST Framework (http://127.0.0.1:8001)
        |
        ├── OCR Engine (RapidOCR / PaddleOCR ONNX + OpenCV CLAHE & Bilateral Filter)
        ├── AI Clinical Extraction (Deterministic Medical NLP + OpenAI GPT-4o-mini)
        ├── AI Summary & Explanations (Bilingual English & Tamil, Non-Diagnostic Safe)
        ├── AI Grounded Chat (Strictly Grounded in Uploaded Patient Records)
        ├── FHIR R4 & Mock ABHA Mapper (Patient, Condition, MedicationRequest, Observation)
        └── SQLite Database with Django ORM & Django Admin
```

---

## 🚀 2. Quick Start (How to Run)

### Terminal 1 — Django REST Framework Backend
```bash
# Navigate to django_backend directory
cd django_backend

# (Optional) Install dependencies if not already installed
pip install -r requirements.txt

# Run database migrations
python manage.py makemigrations
python manage.py migrate

# Seed demo dataset
python -c "import django, os; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings'); django.setup(); from health.services.sample_data_loader import load_sample_dataset_into_django; load_sample_dataset_into_django()"

# Start Django development server on port 8001
python manage.py runserver 8001
```
*Django runs on `http://127.0.0.1:8001/`.*

### Terminal 2 — Frontend (React + Vite)
```bash
# Navigate to frontend directory
cd frontend

# Install frontend dependencies (if first time)
npm install

# Start Vite dev server
npm run dev
```
*Frontend runs on `http://localhost:5174/` (proxies `/api` and `/uploads` to `http://127.0.0.1:8001`).*

---

## ⚙️ 3. Environment Configuration

Create or update `.env` in `django_backend/.env`:
```env
SECRET_KEY=django-insecure-9&c9%a=3xylkr))al&pxo52e8*s1^+z3m**+#x^f%0s%6_wdi6
DEBUG=True
OPENAI_API_KEY=your_openai_api_key_here
PORT=8001
HOST=127.0.0.1
```
*Note: If `OPENAI_API_KEY` is not provided, the system automatically uses the built-in deterministic clinical rule engine for OCR extraction, lab analysis, and chat.*

---

## 🎯 4. Demo Walkthrough for Judges (1-Minute Demo)

1. **Open the Web Application:** Open `http://localhost:5174/` in your browser.
2. **Click "Demo Mode (1-Click)":** Located in the top navigation bar. This immediately seeds 4 realistic synthetic medical records:
   - Scanned Prescription (`Prescription_Metformin_2026.pdf`)
   - Laboratory Blood Panel (`Lab_Report_Biochemistry_CBC.pdf`)
   - Day Care Surgical Discharge Summary (`Discharge_Summary_Daycare_Endoscopy.pdf`)
   - Bilingual Tamil + English Prescription (`Tamil_Prescription_Diabetes_Followup.png`)
3. **Inspect the Dashboard:** Observe Overview Metric Cards, AI Health Insights, and Medication Overview.
4. **Try Document Upload & OCR:** Go to **Upload & OCR**, drag-and-drop a file or click one of the preloaded synthetic sample cards. Watch the 6-stage live processing pipeline!
5. **Compare OCR Output:** Click **"Compare Original & OCR Text"** to see side-by-side view with confidence score and language badge.
6. **Switch Language to Tamil:** Click the language selector dropdown in the top bar and select **"தமிழ் (Tamil)"** to see explanations in Tamil.
7. **Ask AI Health Copilot:** Navigate to **"Ask Copilot"** and click prompt chips:
   - *"What medicines are mentioned in my prescription?"*
   - *"What are my abnormal lab values?"*
   - *"Translate my report into Tamil"*
   - *"What should I ask my doctor about this report?"*
8. **View ABHA / FHIR Profile:** Go to **"ABHA & FHIR"** to inspect the Mock ABHA digital card, FHIR resource mapping table, and copy the standardized FHIR R4 JSON bundle.
9. **Django Admin:** Visit `http://127.0.0.1:8001/admin/` to inspect all database tables through Django's administrative interface.

---

## 🌐 5. Multilingual OCR Pipeline
- **Script Analysis:** Analyzes Unicode code blocks (`\u0B80-\u0BFF` for Tamil, `\u0900-\u097F` for Hindi, `\u0C00-\u0C7F` for Telugu, `[a-zA-Z]` for English).
- **Bilingual Processing:** Detects and parses mixed prescriptions containing Tamil instructions (e.g. `மருந்து: Metformin 500 mg`, `உணவுக்குப் பின்`).
- **Confidence Scoring:** Calculates token-level and line-level confidence. Automatically triggers a visual caution alert if confidence < 70%.

---

## 🛡️ 6. Clinical Safety & Guardrails
Because this is a healthcare application, strict safety guardrails are implemented:
- ❌ **No Unsupervised Diagnoses:** Never says *"You have disease X"*. Uses educational wording: *"This value is outside the reference range shown in the report. There can be several reasons for this result, and a healthcare professional should interpret it in context."*
- ❌ **No Medication Alterations:** Prohibits recommending starting, stopping, or altering doses. Every medication card carries: *"Verify medication name, dose, and instructions against the original prescription before taking or changing any medication."*
- ⚠️ **Emergency Guidance:** Directs emergency symptoms to immediate hospital care.

---

## 📊 7. Django ORM Models & Database

| Model | App | Description |
|---|---|---|
| `MedicalDocument` | `documents` | Uploaded document metadata, filename, file_path, status, summaries |
| `OCRResult` | `documents` | Raw & cleaned OCR text, engine, confidence score, processing time |
| `User` | `health` | User profile and mock ABHA ID reference |
| `Patient` | `health` | Extracted patient demographics (name, age, gender, UHID) |
| `Medication` | `health` | Medication name, dose, frequency, route, duration, food timing |
| `LabResult` | `health` | Test name, measured value, unit, reference range, status, safe explanations |
| `Diagnosis` | `health` | Documented clinical conditions and source document tags |
| `Procedure` | `health` | Surgical and diagnostic procedures with facility and date |
| `Symptom` | `health` | Patient complaints with severity and duration |
| `MedicalEvent` | `health` | Encounters, OPD consultations, lab collections |
| `HealthTimeline` | `health` | Chronological event index with JSON payload |
| `ChatHistory` | `health` | Multi-turn conversational history with copilot |
| `FHIRRecord` | `health` | ABDM compliant FHIR R4 Bundle records |

---

## 🔌 8. REST API Endpoints

All endpoints support requests both with and without trailing slash:

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/documents/upload/` | Ingest and process medical document through complete pipeline |
| `GET` | `/api/documents/` | List all ingested documents with OCR status & language |
| `GET` | `/api/documents/<doc_id>/` | Detailed document view with raw OCR text and structured entities |
| `GET` | `/api/health-profile/` | Aggregated patient profile (active meds, lab tests, diagnoses) |
| `GET` | `/api/timeline/` | Chronological health timeline |
| `POST` | `/api/chat/` | Grounded conversational AI assistant with medical guardrails |
| `POST` | `/api/translate/` | Multilingual translation into Tamil, Hindi, Telugu, etc. |
| `GET` | `/api/abha-profile/` | Mock ABHA card data and HL7 FHIR R4 Bundle representation |
| `GET` | `/api/medications/` | Dedicated list of all prescribed medications |
| `GET` | `/api/labs/` | Dedicated list of all lab results |
| `GET` | `/api/diagnoses/` | Dedicated list of all clinical diagnoses |
| `GET` | `/api/abha/` | Mock ABHA digital card demographics |
| `GET` | `/api/fhir/` | Exportable HL7 FHIR R4 Bundle |
| `POST` | `/api/demo/load-samples/` | 1-Click seed of synthetic clinical records |
| `DELETE` | `/api/documents/reset/` | Clear all records for fresh test run |

---

## 🧪 9. Running Tests

Run the Django automated test suite:
```bash
cd django_backend
python manage.py test health
```
All 11 automated test suites validate:
- Root API connectivity
- Health profile schema & aggregation
- Document upload with PDF & image OCR
- Document list & detail queries
- Timeline chronologic sorting
- Chat grounding and guardrails
- Multilingual translation (Tamil)
- ABHA & FHIR bundle generation
- Dedicated REST resource endpoints
- Data reset and reload workflows
