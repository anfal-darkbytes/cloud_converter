from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import web_views
from .views.api_views import Convert

urlpatterns = [
    path('', web_views.home, name='home'),
    path('converter/<str:from_format>-to-<str:to_format>/<int:pk>/', web_views.convert, name='convert'),
    path('privacy-policy/', web_views.privacy_policy, name='privacy_policy'),
    path('terms_condition/', web_views.terms_condition, name='terms_condition'),
    path('api/', web_views.apis, name='apis'),
    path('contact-us/',web_views.contact_us, name='contact_us'),

    # API's
    path('api/convert/', Convert.as_view(), name='convert_api')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)