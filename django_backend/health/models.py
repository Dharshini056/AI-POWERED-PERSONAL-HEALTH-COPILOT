from django.db import models
from documents.models import MedicalDocument

class User(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, blank=True, null=True)
    abha_id = models.CharField(max_length=64, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.id})"


class Patient(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    document = models.ForeignKey(MedicalDocument, on_delete=models.CASCADE, null=True, blank=True, related_name='patients')
    name = models.CharField(max_length=255, blank=True, null=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=50, blank=True, null=True)
    date_of_birth = models.CharField(max_length=50, blank=True, null=True)
    patient_id_ref = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name or self.id


class Diagnosis(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    document = models.ForeignKey(MedicalDocument, on_delete=models.CASCADE, related_name='diagnoses')
    diagnosis_name = models.CharField(max_length=255)
    date = models.CharField(max_length=50, blank=True, null=True)
    source_document = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Diagnoses"

    def __str__(self):
        return self.diagnosis_name


class Medication(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    document = models.ForeignKey(MedicalDocument, on_delete=models.CASCADE, related_name='medications')
    name = models.CharField(max_length=255)
    dose = models.CharField(max_length=100, blank=True, null=True)
    dosage_unit = models.CharField(max_length=50, blank=True, null=True)
    frequency = models.CharField(max_length=100, blank=True, null=True)
    route = models.CharField(max_length=50, default='Oral')
    duration = models.CharField(max_length=100, blank=True, null=True)
    instructions = models.TextField(blank=True, null=True)
    before_after_food = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} {self.dose or ''}"


class LabResult(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    document = models.ForeignKey(MedicalDocument, on_delete=models.CASCADE, related_name='lab_results')
    test_name = models.CharField(max_length=255)
    value = models.CharField(max_length=50)
    unit = models.CharField(max_length=50, blank=True, null=True)
    reference_range = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    date = models.CharField(max_length=50, blank=True, null=True)
    explanation_en = models.TextField(blank=True, null=True)
    explanation_ta = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.test_name}: {self.value} {self.unit or ''}"


class Procedure(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    document = models.ForeignKey(MedicalDocument, on_delete=models.CASCADE, related_name='procedures')
    procedure_name = models.CharField(max_length=255)
    date = models.CharField(max_length=50, blank=True, null=True)
    hospital = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.procedure_name


class Symptom(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    document = models.ForeignKey(MedicalDocument, on_delete=models.CASCADE, related_name='symptoms')
    symptom_name = models.CharField(max_length=255)
    severity = models.CharField(max_length=50, blank=True, null=True)
    duration = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.symptom_name


class MedicalEvent(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    document = models.ForeignKey(MedicalDocument, on_delete=models.CASCADE, related_name='medical_events')
    event_type = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    doctor_name = models.CharField(max_length=255, blank=True, null=True)
    facility_name = models.CharField(max_length=255, blank=True, null=True)
    event_date = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-event_date', '-created_at']

    def __str__(self):
        return f"{self.title} ({self.event_date})"

# Alias for HealthEvent
HealthEvent = MedicalEvent


class HealthTimeline(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    document = models.ForeignKey(MedicalDocument, on_delete=models.CASCADE, related_name='timeline_items')
    event_date = models.CharField(max_length=50)
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    summary = models.TextField(blank=True, null=True)
    details_json = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-event_date', '-created_at']

    def __str__(self):
        return f"{self.title} ({self.event_date})"


class ChatHistory(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    session_id = models.CharField(max_length=100, default='default')
    role = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.role}: {self.content[:40]}"


class FHIRRecord(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True, related_name='fhir_records')
    resource_type = models.CharField(max_length=100, default='Bundle')
    bundle_json = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"FHIR {self.resource_type} ({self.id})"
