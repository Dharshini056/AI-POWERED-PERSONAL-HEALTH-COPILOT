import uuid
import datetime
from typing import Dict, Any, List

def generate_mock_abha_profile(patient_info: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Generates ABDM compliant mock ABHA ID and demographic profile.
    Clearly designated as Demo / Mock ABHA.
    """
    p_name = (patient_info and patient_info.get("name")) or "Arun Kumar"
    gender = (patient_info and patient_info.get("gender")) or "Male"
    age = (patient_info and patient_info.get("age")) or 42

    birth_year = 2026 - int(age)

    return {
        "abha_number": "91-4521-8934-1022",
        "abha_address": "arunkumar@sbx",
        "is_mock": True,
        "badge_label": "Demo / Mock ABHA ID (Sandbox Architecture)",
        "full_name": p_name,
        "gender": gender,
        "date_of_birth": f"{birth_year}-05-14",
        "mobile": "+91 98765 43210",
        "state": "Tamil Nadu",
        "district": "Chennai",
        "kyc_verified": True,
        "linked_hip": [
            {"hip_id": "IN-TN-HOSP-0012", "hip_name": "Apollo Multispeciality Hospital, Chennai"},
            {"hip_id": "IN-TN-LAB-045", "hip_name": "Metropolis Healthcare Diagnostics"}
        ]
    }

def convert_to_fhir_bundle(structured_data: Dict[str, Any], document_id: str = "doc_01") -> Dict[str, Any]:
    """
    Translates extracted healthcare data into a standard FHIR R4 Bundle
    conforming to Ayushman Bharat Digital Mission (ABDM) standards.
    """
    bundle_id = f"bundle-{uuid.uuid4().hex[:8]}"
    patient_id = f"Patient-{uuid.uuid4().hex[:6]}"
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()

    patient_meta = structured_data.get("patient", {})
    doc_meta = structured_data.get("document", {})
    medications = structured_data.get("medications", [])
    lab_results = structured_data.get("lab_results", [])
    diagnoses = structured_data.get("diagnoses", [])
    events = structured_data.get("medical_events", [])

    entries = []

    # 1. FHIR Patient Resource
    patient_resource = {
        "fullUrl": f"urn:uuid:{patient_id}",
        "resource": {
            "resourceType": "Patient",
            "id": patient_id,
            "identifier": [
                {
                    "system": "https://healthid.ndhm.gov.in",
                    "value": "91-4521-8934-1022"
                }
            ],
            "name": [
                {
                    "text": patient_meta.get("name") or "Arun Kumar"
                }
            ],
            "gender": (patient_meta.get("gender") or "male").lower(),
            "birthDate": patient_meta.get("date_of_birth") or "1984-05-14"
        }
    }
    entries.append(patient_resource)

    # 2. FHIR DocumentReference Resource (Uploaded medical file)
    doc_ref_id = f"DocumentReference-{document_id}"
    doc_ref_resource = {
        "fullUrl": f"urn:uuid:{doc_ref_id}",
        "resource": {
            "resourceType": "DocumentReference",
            "id": doc_ref_id,
            "status": "current",
            "subject": {"reference": f"Patient/{patient_id}"},
            "type": {
                "text": doc_meta.get("type", "Clinical Document")
            },
            "date": doc_meta.get("date") or "2026-08-12",
            "description": f"Extracted via Multilingual AI OCR ({doc_meta.get('language', 'English')})"
        }
    }
    entries.append(doc_ref_resource)

    # 3. FHIR Condition Resources (Diagnoses)
    for idx, d in enumerate(diagnoses):
        cond_id = f"Condition-{idx + 1}"
        entries.append({
            "fullUrl": f"urn:uuid:{cond_id}",
            "resource": {
                "resourceType": "Condition",
                "id": cond_id,
                "clinicalStatus": {
                    "coding": [{"system": "http://terminology.hl7.org/CodeSystem/condition-clinical", "code": "active"}]
                },
                "code": {
                    "text": d.get("name")
                },
                "subject": {"reference": f"Patient/{patient_id}"},
                "recordedDate": d.get("date") or doc_meta.get("date")
            }
        })

    # 4. FHIR MedicationRequest Resources (Prescriptions)
    for idx, m in enumerate(medications):
        med_req_id = f"MedicationRequest-{idx + 1}"
        entries.append({
            "fullUrl": f"urn:uuid:{med_req_id}",
            "resource": {
                "resourceType": "MedicationRequest",
                "id": med_req_id,
                "status": "active",
                "intent": "order",
                "medicationCodeableConcept": {
                    "text": m.get("name")
                },
                "subject": {"reference": f"Patient/{patient_id}"},
                "dosageInstruction": [
                    {
                        "text": f"{m.get('dose', '')} {m.get('frequency', '')} ({m.get('instructions', '')})",
                        "route": {"text": m.get("route", "Oral")},
                        "timing": {"code": {"text": m.get("frequency", "Once daily")}}
                    }
                ]
            }
        })

    # 5. FHIR Observation Resources (Laboratory Results)
    obs_references = []
    for idx, l in enumerate(lab_results):
        obs_id = f"Observation-{idx + 1}"
        obs_ref = {"reference": f"Observation/{obs_id}", "display": l.get("test_name")}
        obs_references.append(obs_ref)

        entries.append({
            "fullUrl": f"urn:uuid:{obs_id}",
            "resource": {
                "resourceType": "Observation",
                "id": obs_id,
                "status": "final",
                "code": {
                    "text": l.get("test_name")
                },
                "subject": {"reference": f"Patient/{patient_id}"},
                "valueQuantity": {
                    "value": l.get("value"),
                    "unit": l.get("unit")
                },
                "interpretation": [
                    {
                        "text": l.get("status", "Normal")
                    }
                ],
                "referenceRange": [
                    {
                        "text": l.get("reference_range", "")
                    }
                ]
            }
        })

    # 6. FHIR DiagnosticReport Resource (Lab Report grouping observations)
    if lab_results:
        diag_rep_id = f"DiagnosticReport-{uuid.uuid4().hex[:6]}"
        entries.append({
            "fullUrl": f"urn:uuid:{diag_rep_id}",
            "resource": {
                "resourceType": "DiagnosticReport",
                "id": diag_rep_id,
                "status": "final",
                "code": {"text": "Laboratory Biochemical Profile"},
                "subject": {"reference": f"Patient/{patient_id}"},
                "result": obs_references
            }
        })

    # 7. FHIR Encounter Resources (Clinical Visits)
    for idx, ev in enumerate(events):
        enc_id = f"Encounter-{idx + 1}"
        entries.append({
            "fullUrl": f"urn:uuid:{enc_id}",
            "resource": {
                "resourceType": "Encounter",
                "id": enc_id,
                "status": "finished",
                "class": {"code": "AMB", "display": "Ambulatory OPD"},
                "subject": {"reference": f"Patient/{patient_id}"},
                "serviceProvider": {"display": ev.get("facility_name", "Clinical Facility")},
                "participant": [{"individual": {"display": ev.get("doctor_name", "Physician")}}]
            }
        })

    fhir_bundle = {
        "resourceType": "Bundle",
        "id": bundle_id,
        "type": "document",
        "timestamp": timestamp,
        "entry": entries
    }

    # Resource type breakdown for quick dashboard metrics
    resource_counts = {
        "Patient": 1,
        "DocumentReference": 1,
        "Condition": len(diagnoses),
        "MedicationRequest": len(medications),
        "Observation": len(lab_results),
        "DiagnosticReport": 1 if lab_results else 0,
        "Encounter": len(events)
    }

    return {
        "bundle": fhir_bundle,
        "resource_counts": resource_counts,
        "mappings": [
            {"document_element": "Uploaded PDF / Image", "fhir_resource": "DocumentReference", "purpose": "Document tracking & integrity hash"},
            {"document_element": "Patient Demographics", "fhir_resource": "Patient", "purpose": "Patient identity & ABHA binding"},
            {"document_element": "Prescribed Medications", "fhir_resource": "MedicationRequest", "purpose": "Prescription orders and dosage schedule"},
            {"document_element": "Lab Test Values & Ranges", "fhir_resource": "Observation", "purpose": "Biochemical test measurements & ranges"},
            {"document_element": "Laboratory Summary Report", "fhir_resource": "DiagnosticReport", "purpose": "Diagnostic interpretation container"},
            {"document_element": "Clinical Diagnoses", "fhir_resource": "Condition", "purpose": "Active disease / diagnosis documentation"},
            {"document_element": "Doctor & Hospital Visits", "fhir_resource": "Encounter", "purpose": "Healthcare encounter & provider tracking"}
        ]
    }
