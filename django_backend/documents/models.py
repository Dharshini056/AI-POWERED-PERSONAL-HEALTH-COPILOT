from django.db import models

class MedicalDocument(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    user_id = models.CharField(max_length=64, default='usr_demo_01')
    filename = models.CharField(max_length=255)
    file_path = models.CharField(max_length=512)
    file_type = models.CharField(max_length=100, blank=True, null=True)
    file_size = models.IntegerField(default=0)
    doc_type = models.CharField(max_length=100, default='Medical Document')
    status = models.CharField(max_length=50, default='processed')
    detected_language = models.CharField(max_length=50, default='English')
    ocr_confidence = models.FloatField(default=0.0)
    summary_en = models.TextField(blank=True, null=True)
    summary_ta = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.filename} ({self.doc_type})"


class OCRResult(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    document = models.OneToOneField(MedicalDocument, on_delete=models.CASCADE, related_name='ocr_result')
    raw_text = models.TextField(blank=True, null=True)
    cleaned_text = models.TextField(blank=True, null=True)
    detected_language = models.CharField(max_length=50, default='English')
    confidence_score = models.FloatField(default=0.0)
    processing_time_ms = models.IntegerField(default=0)
    engine_name = models.CharField(max_length=100, default='RapidOCR-PaddleONNX')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"OCR for {self.document.filename} ({self.confidence_score})"
