from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # dynamic converter URL
    path('<str:from_ext>-to-<str:to_ext>/', views.convert, name='convert'),
]
