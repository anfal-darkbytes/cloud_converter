from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from ..views import api_views

urlpatterns = [
    path('blogs/', api_views.Blog.as_view(), name='blog-api'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)