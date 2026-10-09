from django.contrib import admin
from .models import MedicalDocument, OCRResult

@admin.register(MedicalDocument)
class MedicalDocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'filename', 'doc_type', 'detected_language', 'ocr_confidence', 'status', 'created_at')
    search_fields = ('filename', 'doc_type', 'detected_language')
    list_filter = ('doc_type', 'detected_language', 'status')

@admin.register(OCRResult)
class OCRResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'document', 'detected_language', 'confidence_score', 'processing_time_ms', 'engine_name', 'created_at')
    search_fields = ('document__filename', 'raw_text')
    list_filter = ('detected_language', 'engine_name')
