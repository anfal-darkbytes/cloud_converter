from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('blogs/', views.blog, name='blog'),
    path('blog/<slug:slug>', views.blog_by_id, name='blog_by_slug'),
    path('blog/search/', views.search_by_query, name='search_by_query')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)