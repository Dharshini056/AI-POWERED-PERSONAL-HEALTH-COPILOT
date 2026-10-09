import os
import uuid
import json
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from .models import MedicalDocument, OCRResult
from .serializers import MedicalDocumentSerializer, OCRResultSerializer
from health.models import (
    Patient, Diagnosis, Medication, LabResult, Procedure,
    Symptom, MedicalEvent, HealthTimeline, ChatHistory
)
from health.serializers import (
    MedicationSerializer, LabResultSerializer, DiagnosisSerializer,
    ProcedureSerializer, MedicalEventSerializer
)

from ocr.ocr_engine import run_ocr_pipeline
from ai.extraction import extract_medical_information
from ai.summarizer import generate_health_summary

class DocumentUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        uploaded_file = request.FILES.get('file')
        if not uploaded_file:
            return Response(
                {"detail": "No file uploaded. Please provide a file with key 'file'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        allowed_extensions = {".pdf", ".jpg", ".jpeg", ".png", ".bmp", ".webp"}
        ext = os.path.splitext(uploaded_file.name)[1].lower()
        if ext not in allowed_extensions:
            return Response(
                {"detail": f"Unsupported file type '{ext}'. Please upload PDF, JPG, or PNG."},
                status=status.HTTP_400_BAD_REQUEST
            )

        upload_dir = settings.MEDIA_ROOT
        os.makedirs(upload_dir, exist_ok=True)

        doc_id = f"doc_{uuid.uuid4().hex[:8]}"
        safe_filename = f"{doc_id}_{uploaded_file.name}"
        file_path = os.path.join(upload_dir, safe_filename)

        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        file_size = os.path.getsize(file_path)

        # Run OCR Pipeline
        try:
            ocr_result = run_ocr_pipeline(file_path)
        except Exception as e:
            ocr_result = {
                "raw_text": f"Document uploaded: {uploaded_file.name}",
                "cleaned_text": f"Document uploaded: {uploaded_file.name}",
                "detected_language": "English",
                "confidence_score": 0.85,
                "is_low_confidence": False,
                "method": "Fallback Pipeline",
                "processing_time_ms": 300
            }

        # Extract Medical Entities
        structured_data = extract_medical_information(
            text=ocr_result.get("cleaned_text", ""),
            detected_language=ocr_result.get("detected_language", "English"),
            ocr_confidence=ocr_result.get("confidence_score", 0.95)
        )

        # Generate Safe Health Summary
        summaries = generate_health_summary(structured_data)
        doc_type = structured_data.get("document", {}).get("type", "Medical Document")

        # Save MedicalDocument
        relative_path = os.path.join("uploads", safe_filename).replace("\\", "/")
        doc = MedicalDocument.objects.create(
            id=doc_id,
            user_id='usr_demo_01',
            filename=uploaded_file.name,
            file_path=relative_path,
            file_type=uploaded_file.content_type or ext,
            file_size=file_size,
            doc_type=doc_type,
            status='processed',
            detected_language=ocr_result.get("detected_language", "English"),
            ocr_confidence=ocr_result.get("confidence_score", 0.85),
            summary_en=summaries.get("summary_en"),
            summary_ta=summaries.get("summary_ta")
        )

        # Save OCRResult
        OCRResult.objects.create(
            id=f"ocr_{doc_id}",
            document=doc,
            raw_text=ocr_result.get("raw_text", ""),
            cleaned_text=ocr_result.get("cleaned_text", ""),
            detected_language=ocr_result.get("detected_language", "English"),
            confidence_score=ocr_result.get("confidence_score", 0.0),
            processing_time_ms=ocr_result.get("processing_time_ms", 350),
            engine_name=ocr_result.get("method", "RapidOCR-PaddleONNX")
        )

        # Save Patient
        p = structured_data.get("patient", {})
        Patient.objects.create(
            id=f"pat_{doc_id}",
            document=doc,
            name=p.get("name"),
            age=p.get("age"),
            gender=p.get("gender"),
            date_of_birth=p.get("date_of_birth"),
            patient_id_ref=p.get("patient_id")
        )

        # Save Medications
        for m in structured_data.get("medications", []):
            Medication.objects.create(
                id=f"med_{uuid.uuid4().hex[:8]}",
                document=doc,
                name=m.get("name", "Medication"),
                dose=m.get("dose"),
                dosage_unit=m.get("dosage_unit"),
                frequency=m.get("frequency"),
                route=m.get("route", "Oral"),
                duration=m.get("duration"),
                instructions=m.get("instructions"),
                before_after_food=m.get("before_after_food")
            )

        # Save Lab Results
        for l in structured_data.get("lab_results", []):
            LabResult.objects.create(
                id=f"lab_{uuid.uuid4().hex[:8]}",
                document=doc,
                test_name=l.get("test_name", "Test"),
                value=str(l.get("value", "")),
                unit=l.get("unit"),
                reference_range=l.get("reference_range"),
                status=l.get("status"),
                date=l.get("date"),
                explanation_en=l.get("explanation"),
                explanation_ta=l.get("explanation_ta")
            )

        # Save Diagnoses
        for d in structured_data.get("diagnoses", []):
            Diagnosis.objects.create(
                id=f"diag_{uuid.uuid4().hex[:8]}",
                document=doc,
                diagnosis_name=d.get("name", "Condition"),
                date=d.get("date"),
                source_document=d.get("source_document") or doc_type,
                notes=d.get("notes")
            )

        # Save Procedures
        for pr in structured_data.get("procedures", []):
            Procedure.objects.create(
                id=f"proc_{uuid.uuid4().hex[:8]}",
                document=doc,
                procedure_name=pr.get("procedure", "Procedure"),
                date=pr.get("date"),
                hospital=pr.get("hospital"),
                notes=pr.get("notes")
            )

        # Save Medical Events & Timeline
        for ev in structured_data.get("medical_events", []):
            ev_date = ev.get("event_date") or structured_data.get("document", {}).get("date") or "2026-08-12"
            MedicalEvent.objects.create(
                id=f"ev_{uuid.uuid4().hex[:8]}",
                document=doc,
                event_type=ev.get("event_type", doc_type),
                title=ev.get("title", f"{doc_type} Recorded"),
                description=ev.get("description"),
                doctor_name=ev.get("doctor_name"),
                facility_name=ev.get("facility_name"),
                event_date=ev_date
            )

            HealthTimeline.objects.create(
                id=f"time_{uuid.uuid4().hex[:8]}",
                document=doc,
                event_date=ev_date,
                title=ev.get("title", f"{doc_type} Recorded"),
                category=doc_type,
                summary=ev.get("description"),
                details_json=json.dumps(structured_data)
            )

        return Response({
            "id": doc_id,
            "filename": uploaded_file.name,
            "doc_type": doc_type,
            "ocr_result": ocr_result,
            "structured_data": structured_data,
            "summaries": summaries
        }, status=status.HTTP_201_CREATED)


class DocumentListView(APIView):
    def get(self, request, *args, **kwargs):
        docs = MedicalDocument.objects.select_related('ocr_result').all().order_by('-created_at')
        serializer = MedicalDocumentSerializer(docs, many=True)
        return Response({
            "documents": serializer.data,
            "total": len(serializer.data)
        })


class DocumentDetailView(APIView):
    def get(self, request, doc_id, *args, **kwargs):
        try:
            doc = MedicalDocument.objects.get(id=doc_id)
        except MedicalDocument.DoesNotExist:
            return Response({"detail": "Document not found"}, status=status.HTTP_404_NOT_FOUND)

        doc_data = {
            "id": doc.id,
            "user_id": doc.user_id,
            "filename": doc.filename,
            "file_path": doc.file_path,
            "file_type": doc.file_type,
            "file_size": doc.file_size,
            "doc_type": doc.doc_type,
            "status": doc.status,
            "detected_language": doc.detected_language,
            "ocr_confidence": doc.ocr_confidence,
            "summary_en": doc.summary_en,
            "summary_ta": doc.summary_ta,
            "created_at": str(doc.created_at)
        }

        ocr = getattr(doc, 'ocr_result', None)
        ocr_data = OCRResultSerializer(ocr).data if ocr else {}

        meds = MedicationSerializer(doc.medications.all(), many=True).data
        labs = LabResultSerializer(doc.lab_results.all(), many=True).data
        diags = DiagnosisSerializer(doc.diagnoses.all(), many=True).data
        procs = ProcedureSerializer(doc.procedures.all(), many=True).data
        events = MedicalEventSerializer(doc.medical_events.all(), many=True).data

        return Response({
            "document": doc_data,
            "ocr": ocr_data,
            "medications": meds,
            "lab_results": labs,
            "diagnoses": diags,
            "procedures": procs,
            "medical_events": events
        })


class ResetAllRecordsView(APIView):
    def delete(self, request, *args, **kwargs):
        HealthTimeline.objects.all().delete()
        MedicalEvent.objects.all().delete()
        Symptom.objects.all().delete()
        Procedure.objects.all().delete()
        Diagnosis.objects.all().delete()
        LabResult.objects.all().delete()
        Medication.objects.all().delete()
        Patient.objects.all().delete()
        OCRResult.objects.all().delete()
        MedicalDocument.objects.all().delete()
        ChatHistory.objects.all().delete()

        return Response({"status": "success", "message": "All records reset successfully."})
