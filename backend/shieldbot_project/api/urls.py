from django.urls import path
from api.views import TestListCreateAPIView
from django.conf.urls.static import static
from django.conf import settings
from .views import csrf_token_view
urlpatterns = [
    path('get-csrf/', csrf_token_view, name='get-csrf'),
    path('tests/', TestListCreateAPIView.as_view(), name='test-list-create'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)