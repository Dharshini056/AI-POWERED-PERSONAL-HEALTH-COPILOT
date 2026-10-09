from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def root_view(request):
    return Response({
        "status": "online",
        "service": "AI Personal Health Copilot (Django REST Framework)",
        "version": "1.0.0",
        "docs_url": "/admin/"
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', root_view, name='root'),
    
    # API endpoints
    path('api/documents/', include('documents.urls')),
    path('api/documents', include('documents.urls')),
    path('api/', include('health.urls')),
]

# Explicit static/media serving for uploaded files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        re_path(r'^uploads/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]
