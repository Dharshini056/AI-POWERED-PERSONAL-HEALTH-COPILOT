from django.urls import path, re_path
from .views import DocumentUploadView, DocumentListView, DocumentDetailView, ResetAllRecordsView

urlpatterns = [
    re_path(r'^upload/?$', DocumentUploadView.as_view(), name='document-upload'),
    re_path(r'^reset/?$', ResetAllRecordsView.as_view(), name='document-reset'),
    re_path(r'^(?P<doc_id>[a-zA-Z0-9_\-]+)/?$', DocumentDetailView.as_view(), name='document-detail'),
    re_path(r'^$', DocumentListView.as_view(), name='document-list'),
]
