from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field

class PatientInfo(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    date_of_birth: Optional[str] = None
    patient_id: Optional[str] = None

class DocumentMeta(BaseModel):
    type: Optional[str] = "Medical Document"
    language: Optional[str] = "English"
    date: Optional[str] = None
    ocr_confidence: Optional[float] = 0.0

class MedicationItem(BaseModel):
    name: str
    dose: Optional[str] = None
    dosage_unit: Optional[str] = None
    frequency: Optional[str] = None
    route: Optional[str] = "Oral"
    duration: Optional[str] = None
    instructions: Optional[str] = None
    before_after_food: Optional[str] = None
    source_document: Optional[str] = None

class LabResultItem(BaseModel):
    test_name: str
    value: str
    unit: Optional[str] = None
    reference_range: Optional[str] = None
    status: Optional[str] = "Normal"  # "Normal", "High", "Low", "Critical", "Below reference range", "Above reference range"
    date: Optional[str] = None
    explanation: Optional[str] = None
    explanation_ta: Optional[str] = None

class DiagnosisItem(BaseModel):
    name: str
    date: Optional[str] = None
    source_document: Optional[str] = None
    notes: Optional[str] = None

class ProcedureItem(BaseModel):
    procedure: str
    date: Optional[str] = None
    hospital: Optional[str] = None
    notes: Optional[str] = None

class SymptomItem(BaseModel):
    symptom: str
    severity: Optional[str] = None
    duration: Optional[str] = None

class MedicalEventItem(BaseModel):
    event_type: str  # "Visit", "Admission", "Prescription", "Lab Test", "Discharge"
    title: str
    description: Optional[str] = None
    doctor_name: Optional[str] = None
    facility_name: Optional[str] = None
    event_date: Optional[str] = None

class StructuredHealthRecord(BaseModel):
    patient: PatientInfo = Field(default_factory=PatientInfo)
    document: DocumentMeta = Field(default_factory=DocumentMeta)
    diagnoses: List[DiagnosisItem] = Field(default_factory=list)
    medications: List[MedicationItem] = Field(default_factory=list)
    lab_results: List[LabResultItem] = Field(default_factory=list)
    procedures: List[ProcedureItem] = Field(default_factory=list)
    symptoms: List[SymptomItem] = Field(default_factory=list)
    medical_events: List[MedicalEventItem] = Field(default_factory=list)
    summary_en: Optional[str] = None
    summary_ta: Optional[str] = None
    important_findings: List[str] = Field(default_factory=list)

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default"
    language: Optional[str] = "English"

class ChatResponse(BaseModel):
    reply: str
    sources: List[str] = Field(default_factory=list)
    grounded_entities: Dict[str, Any] = Field(default_factory=dict)
    disclaimer: str

class TranslationRequest(BaseModel):
    text: str
    target_language: str
    context_type: Optional[str] = "summary"  # summary, medication, lab

class TranslationResponse(BaseModel):
    translated_text: str
    target_language: str
