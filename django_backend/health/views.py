import uuid
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from documents.models import MedicalDocument
from .models import (
    Patient, Diagnosis, Medication, LabResult, Procedure,
    Symptom, MedicalEvent, HealthTimeline, ChatHistory, FHIRRecord
)
from .serializers import (
    PatientSerializer, MedicationSerializer, LabResultSerializer,
    DiagnosisSerializer, ProcedureSerializer, MedicalEventSerializer,
    HealthTimelineSerializer, ChatRequestSerializer, TranslationRequestSerializer
)
from .services.sample_data_loader import load_sample_dataset_into_django

from ai.chat import generate_chat_reply
from ai.translator import translate_health_content
from fhir.mapper import generate_mock_abha_profile, convert_to_fhir_bundle


def get_aggregated_health_profile():
    """
    Helper function to aggregate user health data for API views and Chat context.
    """
    # Patient demographics
    latest_patient = Patient.objects.order_by('-created_at').first()
    if latest_patient:
        patient_data = {
            "name": latest_patient.name or "Arun Kumar",
            "age": latest_patient.age or 42,
            "gender": latest_patient.gender or "Male",
            "date_of_birth": latest_patient.date_of_birth or "1984-05-14",
            "patient_id": latest_patient.patient_id_ref or "AP-2026-90412",
            "patient_id_ref": latest_patient.patient_id_ref or "AP-2026-90412"
        }
    else:
        patient_data = {
            "name": "Arun Kumar",
            "age": 42,
            "gender": "Male",
            "date_of_birth": "1984-05-14",
            "patient_id": "AP-2026-90412",
            "patient_id_ref": "AP-2026-90412"
        }

    meds_qs = Medication.objects.select_related('document').order_by('-created_at')
    medications = MedicationSerializer(meds_qs, many=True).data

    labs_qs = LabResult.objects.select_related('document').order_by('-created_at')
    lab_results = LabResultSerializer(labs_qs, many=True).data

    diags_qs = Diagnosis.objects.select_related('document').order_by('-created_at')
    diagnoses = DiagnosisSerializer(diags_qs, many=True).data

    procs_qs = Procedure.objects.order_by('-created_at')
    procedures = ProcedureSerializer(procs_qs, many=True).data

    events_qs = MedicalEvent.objects.order_by('-event_date', '-created_at')
    events = MedicalEventSerializer(events_qs, many=True).data

    doc_count = MedicalDocument.objects.count()

    abnormal_count = sum(
        1 for l in lab_results
        if l.get("status") in ["Below reference range", "Above reference range", "High", "Low", "Critical"]
    )

    return {
        "patient": patient_data,
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


class HealthProfileView(APIView):
    def get(self, request, *args, **kwargs):
        profile = get_aggregated_health_profile()
        return Response(profile)


class TimelineView(APIView):
    def get(self, request, *args, **kwargs):
        items = HealthTimeline.objects.select_related('document').order_by('-event_date', '-created_at')
        serializer = HealthTimelineSerializer(items, many=True)
        return Response({
            "timeline": serializer.data,
            "total": len(serializer.data)
        })


class ChatView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ChatRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        message = serializer.validated_data['message']
        session_id = serializer.validated_data.get('session_id', 'default')
        language = serializer.validated_data.get('language', 'English')

        profile = get_aggregated_health_profile()

        # Retrieve recent session history
        history_qs = ChatHistory.objects.filter(session_id=session_id).order_by('created_at')[:6]
        session_history = [{"role": h.role, "content": h.content} for h in history_qs]

        result = generate_chat_reply(
            user_query=message,
            patient_context=profile,
            session_history=session_history,
            language=language
        )

        try:
            ChatHistory.objects.create(
                id=f"msg_{uuid.uuid4().hex[:8]}",
                session_id=session_id,
                role='user',
                content=message
            )
            ChatHistory.objects.create(
                id=f"msg_{uuid.uuid4().hex[:8]}",
                session_id=session_id,
                role='assistant',
                content=result.get("reply", "")
            )
        except Exception as e:
            print("Chat history save note:", e)

        return Response({
            "reply": result.get("reply", ""),
            "sources": result.get("sources", []),
            "grounded_entities": {
                "medications": len(profile["medications"]),
                "lab_results": len(profile["lab_results"])
            },
            "disclaimer": result.get("disclaimer", "")
        })


class TranslationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = TranslationRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        text = serializer.validated_data['text']
        target_language = serializer.validated_data['target_language']

        translated = translate_health_content(text, target_language)
        return Response({
            "translated_text": translated,
            "target_language": target_language
        })


class AbhaProfileView(APIView):
    def get(self, request, *args, **kwargs):
        profile = get_aggregated_health_profile()
        mock_abha = generate_mock_abha_profile(profile["patient"])

        structured_for_fhir = {
            "patient": profile["patient"],
            "document": {
                "type": "Consolidated Personal Health Record",
                "date": "2026-09-12",
                "language": "English + Tamil"
            },
            "diagnoses": profile["diagnoses"],
            "medications": profile["medications"],
            "lab_results": profile["lab_results"],
            "medical_events": profile["medical_events"]
        }
        fhir_data = convert_to_fhir_bundle(structured_for_fhir)

        # Save or update FHIRRecord
        try:
            FHIRRecord.objects.create(
                id=f"fhir_{uuid.uuid4().hex[:8]}",
                resource_type="Bundle",
                bundle_json=json.dumps(fhir_data.get("bundle", {}))
            )
        except Exception:
            pass

        return Response({
            "abha": mock_abha,
            "fhir": fhir_data
        })


class MedicationsListView(APIView):
    def get(self, request, *args, **kwargs):
        meds = Medication.objects.select_related('document').order_by('-created_at')
        serializer = MedicationSerializer(meds, many=True)
        return Response(serializer.data)


class LabsListView(APIView):
    def get(self, request, *args, **kwargs):
        labs = LabResult.objects.select_related('document').order_by('-created_at')
        serializer = LabResultSerializer(labs, many=True)
        return Response(serializer.data)


class DiagnosesListView(APIView):
    def get(self, request, *args, **kwargs):
        diags = Diagnosis.objects.select_related('document').order_by('-created_at')
        serializer = DiagnosisSerializer(diags, many=True)
        return Response(serializer.data)


class AbhaOnlyView(APIView):
    def get(self, request, *args, **kwargs):
        profile = get_aggregated_health_profile()
        mock_abha = generate_mock_abha_profile(profile["patient"])
        return Response(mock_abha)


class FhirOnlyView(APIView):
    def get(self, request, *args, **kwargs):
        profile = get_aggregated_health_profile()
        structured_for_fhir = {
            "patient": profile["patient"],
            "document": {
                "type": "Consolidated Personal Health Record",
                "date": "2026-09-12",
                "language": "English + Tamil"
            },
            "diagnoses": profile["diagnoses"],
            "medications": profile["medications"],
            "lab_results": profile["lab_results"],
            "medical_events": profile["medical_events"]
        }
        fhir_data = convert_to_fhir_bundle(structured_for_fhir)
        return Response(fhir_data)


class LoadDemoSamplesView(APIView):
    def post(self, request, *args, **kwargs):
        load_sample_dataset_into_django()
        return Response({
            "status": "success",
            "message": "Demo sample records loaded successfully into AI Health Copilot."
        })
