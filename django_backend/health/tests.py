import os
import json
from io import BytesIO
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework import status

from documents.models import MedicalDocument
from health.models import Patient, Medication, LabResult, Diagnosis
from health.services.sample_data_loader import load_sample_dataset_into_django

class HealthCopilotAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        load_sample_dataset_into_django()

    def test_root_endpoint(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('status'), 'online')

    def test_health_profile_endpoints(self):
        for url in ['/api/health-profile', '/api/health-profile/']:
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn('patient', response.data)
            self.assertIn('stats', response.data)
            self.assertIn('medications', response.data)
            self.assertIn('lab_results', response.data)
            self.assertIn('diagnoses', response.data)
            self.assertGreaterEqual(response.data['stats']['total_documents'], 4)

    def test_documents_list_endpoints(self):
        for url in ['/api/documents', '/api/documents/']:
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn('documents', response.data)
            self.assertIn('total', response.data)
            self.assertGreaterEqual(response.data['total'], 4)

    def test_document_detail_endpoint(self):
        doc = MedicalDocument.objects.first()
        self.assertIsNotNone(doc)
        response = self.client.get(f'/api/documents/{doc.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('document', response.data)
        self.assertIn('ocr', response.data)
        self.assertIn('medications', response.data)

    def test_timeline_endpoints(self):
        for url in ['/api/timeline', '/api/timeline/']:
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn('timeline', response.data)
            self.assertIn('total', response.data)

    def test_chat_endpoint(self):
        payload = {
            "message": "What medicines are listed in my records?",
            "language": "English",
            "session_id": "test_session"
        }
        for url in ['/api/chat', '/api/chat/']:
            response = self.client.post(url, data=payload, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn('reply', response.data)
            self.assertIn('sources', response.data)
            self.assertIn('disclaimer', response.data)

    def test_translate_endpoint(self):
        payload = {
            "text": "Your hemoglobin is slightly below normal range.",
            "target_language": "Tamil",
            "context_type": "summary"
        }
        for url in ['/api/translate', '/api/translate/']:
            response = self.client.post(url, data=payload, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn('translated_text', response.data)

    def test_abha_and_fhir_endpoints(self):
        res_abha_prof = self.client.get('/api/abha-profile/')
        self.assertEqual(res_abha_prof.status_code, status.HTTP_200_OK)
        self.assertIn('abha', res_abha_prof.data)
        self.assertIn('fhir', res_abha_prof.data)

        res_abha = self.client.get('/api/abha/')
        self.assertEqual(res_abha.status_code, status.HTTP_200_OK)
        self.assertTrue(res_abha.data.get('is_mock'))

        res_fhir = self.client.get('/api/fhir/')
        self.assertEqual(res_fhir.status_code, status.HTTP_200_OK)
        self.assertIn('bundle', res_fhir.data)

    def test_medications_labs_diagnoses_list(self):
        res_m = self.client.get('/api/medications/')
        self.assertEqual(res_m.status_code, status.HTTP_200_OK)
        self.assertIsInstance(res_m.data, list)

        res_l = self.client.get('/api/labs/')
        self.assertEqual(res_l.status_code, status.HTTP_200_OK)
        self.assertIsInstance(res_l.data, list)

        res_d = self.client.get('/api/diagnoses/')
        self.assertEqual(res_d.status_code, status.HTTP_200_OK)
        self.assertIsInstance(res_d.data, list)

    def test_document_upload(self):
        sample_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads', '1_Sample_Prescription_Metformin.pdf')
        if os.path.exists(sample_path):
            with open(sample_path, 'rb') as f:
                pdf_file = SimpleUploadedFile("Test_Prescription.pdf", f.read(), content_type="application/pdf")
            response = self.client.post('/api/documents/upload/', {'file': pdf_file}, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertIn('id', response.data)
            self.assertIn('structured_data', response.data)
            self.assertIn('summaries', response.data)

    def test_reset_and_reload(self):
        res_reset = self.client.delete('/api/documents/reset/')
        self.assertEqual(res_reset.status_code, status.HTTP_200_OK)
        self.assertEqual(MedicalDocument.objects.count(), 0)

        res_reload = self.client.post('/api/demo/load-samples/')
        self.assertEqual(res_reload.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(MedicalDocument.objects.count(), 4)
