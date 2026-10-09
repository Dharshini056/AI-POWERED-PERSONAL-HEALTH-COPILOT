from django.contrib import admin
from .models import (
    User, Patient, Diagnosis, Medication, LabResult,
    Procedure, Symptom, MedicalEvent, HealthTimeline, ChatHistory, FHIRRecord
)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'abha_id', 'created_at')
    search_fields = ('name', 'email', 'abha_id')

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'age', 'gender', 'patient_id_ref', 'created_at')
    search_fields = ('name', 'patient_id_ref')

@admin.register(Diagnosis)
class DiagnosisAdmin(admin.ModelAdmin):
    list_display = ('id', 'diagnosis_name', 'date', 'source_document', 'created_at')
    search_fields = ('diagnosis_name', 'source_document')

@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'dose', 'frequency', 'duration', 'before_after_food', 'created_at')
    search_fields = ('name', 'instructions')

@admin.register(LabResult)
class LabResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'test_name', 'value', 'unit', 'reference_range', 'status', 'date')
    search_fields = ('test_name', 'status')
    list_filter = ('status',)

@admin.register(MedicalEvent)
class MedicalEventAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'event_type', 'doctor_name', 'facility_name', 'event_date')
    search_fields = ('title', 'doctor_name', 'facility_name')

@admin.register(HealthTimeline)
class HealthTimelineAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'event_date')
    search_fields = ('title', 'category')

@admin.register(ChatHistory)
class ChatHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'session_id', 'role', 'created_at')
    list_filter = ('role', 'session_id')

@admin.register(FHIRRecord)
class FHIRRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'resource_type', 'created_at')
