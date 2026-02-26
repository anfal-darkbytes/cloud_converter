from django.contrib import admin
from .models import ConvertModel, ContactUsModel
from unfold.admin import ModelAdmin

@admin.register(ConvertModel)
class CustomAdminClass(ModelAdmin):
    pass

@admin.register(ContactUsModel)
class CustomContactUsModel(ModelAdmin):
    list_display= ('name',)