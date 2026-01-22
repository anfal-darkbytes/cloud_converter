from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('converter/<str:from>-to-<str:to>/', views.convert, name='convert'),

    path('data/', views.data, name='name'),
]