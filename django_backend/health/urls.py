from django.urls import path, re_path
from .views import (
    HealthProfileView, TimelineView, ChatView, TranslationView,
    AbhaProfileView, MedicationsListView, LabsListView, DiagnosesListView,
    AbhaOnlyView, FhirOnlyView, LoadDemoSamplesView
)

urlpatterns = [
    re_path(r'^health-profile/?$', HealthProfileView.as_view(), name='health-profile'),
    re_path(r'^timeline/?$', TimelineView.as_view(), name='timeline'),
    re_path(r'^chat/?$', ChatView.as_view(), name='chat'),
    re_path(r'^translate/?$', TranslationView.as_view(), name='translate'),
    re_path(r'^abha-profile/?$', AbhaProfileView.as_view(), name='abha-profile'),
    re_path(r'^abha/?$', AbhaOnlyView.as_view(), name='abha-only'),
    re_path(r'^fhir/?$', FhirOnlyView.as_view(), name='fhir-only'),
    re_path(r'^medications/?$', MedicationsListView.as_view(), name='medications-list'),
    re_path(r'^labs/?$', LabsListView.as_view(), name='labs-list'),
    re_path(r'^diagnoses/?$', DiagnosesListView.as_view(), name='diagnoses-list'),
    re_path(r'^demo/load-samples/?$', LoadDemoSamplesView.as_view(), name='load-demo-samples'),
]
