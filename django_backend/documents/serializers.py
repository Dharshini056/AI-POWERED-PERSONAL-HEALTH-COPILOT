from rest_framework import serializers
from .models import MedicalDocument, OCRResult

class OCRResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = OCRResult
        fields = '__all__'

class MedicalDocumentSerializer(serializers.ModelSerializer):
    raw_text = serializers.SerializerMethodField()
    processing_time_ms = serializers.SerializerMethodField()
    engine_name = serializers.SerializerMethodField()

    class Meta:
        model = MedicalDocument
        fields = [
            'id', 'user_id', 'filename', 'file_path', 'file_type', 'file_size',
            'doc_type', 'status', 'detected_language', 'ocr_confidence',
            'summary_en', 'summary_ta', 'created_at',
            'raw_text', 'processing_time_ms', 'engine_name'
        ]

    def get_raw_text(self, obj):
        ocr = getattr(obj, 'ocr_result', None)
        return ocr.raw_text if ocr else None

    def get_processing_time_ms(self, obj):
        ocr = getattr(obj, 'ocr_result', None)
        return ocr.processing_time_ms if ocr else 420

    def get_engine_name(self, obj):
        ocr = getattr(obj, 'ocr_result', None)
        return ocr.engine_name if ocr else 'RapidOCR-PaddleONNX'
