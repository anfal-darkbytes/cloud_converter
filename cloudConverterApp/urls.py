from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('converter/<str:from_format>-to-<str:to_format>/<int:pk>/', views.convert, name='convert'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms_condition/', views.terms_condition, name='terms_condition'),
    path('get_ip/', views.get_user_ip, name='get_user_ip'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)