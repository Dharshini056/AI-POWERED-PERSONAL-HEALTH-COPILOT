import json
from rest_framework import serializers
from .models import (
    User, Patient, Diagnosis, Medication, LabResult,
    Procedure, Symptom, MedicalEvent, HealthTimeline, ChatHistory, FHIRRecord
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class PatientSerializer(serializers.ModelSerializer):
    patient_id = serializers.CharField(source='patient_id_ref', read_only=True)

    class Meta:
        model = Patient
        fields = ['id', 'name', 'age', 'gender', 'date_of_birth', 'patient_id_ref', 'patient_id', 'created_at']

class MedicationSerializer(serializers.ModelSerializer):
    filename = serializers.SerializerMethodField()
    doc_type = serializers.SerializerMethodField()
    doc_date = serializers.SerializerMethodField()

    class Meta:
        model = Medication
        fields = [
            'id', 'document_id', 'name', 'dose', 'dosage_unit', 'frequency',
            'route', 'duration', 'instructions', 'before_after_food',
            'created_at', 'filename', 'doc_type', 'doc_date'
        ]

    def get_filename(self, obj):
        return obj.document.filename if obj.document else None

    def get_doc_type(self, obj):
        return obj.document.doc_type if obj.document else "Prescription"

    def get_doc_date(self, obj):
        return str(obj.document.created_at) if obj.document else None

class LabResultSerializer(serializers.ModelSerializer):
    filename = serializers.SerializerMethodField()
    doc_type = serializers.SerializerMethodField()
    explanation = serializers.CharField(source='explanation_en', read_only=True)

    class Meta:
        model = LabResult
        fields = [
            'id', 'document_id', 'test_name', 'value', 'unit', 'reference_range',
            'status', 'date', 'explanation_en', 'explanation_ta', 'explanation',
            'created_at', 'filename', 'doc_type'
        ]

    def get_filename(self, obj):
        return obj.document.filename if obj.document else None

    def get_doc_type(self, obj):
        return obj.document.doc_type if obj.document else "Laboratory Report"

class DiagnosisSerializer(serializers.ModelSerializer):
    filename = serializers.SerializerMethodField()

    class Meta:
        model = Diagnosis
        fields = [
            'id', 'document_id', 'diagnosis_name', 'date', 'source_document',
            'notes', 'created_at', 'filename'
        ]

    def get_filename(self, obj):
        return obj.document.filename if obj.document else None

class ProcedureSerializer(serializers.ModelSerializer):
    procedure = serializers.CharField(source='procedure_name', read_only=True)

    class Meta:
        model = Procedure
        fields = ['id', 'document_id', 'procedure_name', 'procedure', 'date', 'hospital', 'notes', 'created_at']

class SymptomSerializer(serializers.ModelSerializer):
    symptom = serializers.CharField(source='symptom_name', read_only=True)

    class Meta:
        model = Symptom
        fields = ['id', 'document_id', 'symptom_name', 'symptom', 'severity', 'duration', 'created_at']

class MedicalEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalEvent
        fields = '__all__'

class HealthTimelineSerializer(serializers.ModelSerializer):
    details = serializers.SerializerMethodField()
    filename = serializers.SerializerMethodField()
    file_type = serializers.SerializerMethodField()
    ocr_confidence = serializers.SerializerMethodField()

    class Meta:
        model = HealthTimeline
        fields = [
            'id', 'document_id', 'event_date', 'title', 'category', 'summary',
            'details_json', 'details', 'created_at',
            'filename', 'file_type', 'ocr_confidence'
        ]

    def get_details(self, obj):
        if obj.details_json:
            try:
                return json.loads(obj.details_json)
            except Exception:
                return {}
        return {}

    def get_filename(self, obj):
        return obj.document.filename if obj.document else None

    def get_file_type(self, obj):
        return obj.document.file_type if obj.document else "application/pdf"

    def get_ocr_confidence(self, obj):
        return obj.document.ocr_confidence if obj.document else 0.95

class ChatRequestSerializer(serializers.Serializer):
    message = serializers.CharField(required=True)
    session_id = serializers.CharField(default='default', required=False)
    language = serializers.CharField(default='English', required=False)

class TranslationRequestSerializer(serializers.Serializer):
    text = serializers.CharField(required=True)
    target_language = serializers.CharField(required=True)
    context_type = serializers.CharField(default='summary', required=False)

class FHIRRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = FHIRRecord
        fields = '__all__'
