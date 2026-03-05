from django.conf import settings
from django.conf.urls.static import static
from .views import RegisterView, LoginView, login, signup
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register-api'),
    path('api/login/', LoginView.as_view(), name='login-api'),
    path('login/', login, name='login'),
    path('signup/', signup, name='signup'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
