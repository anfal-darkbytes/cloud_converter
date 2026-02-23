from django.contrib import admin
from .models import ConvertModel
from unfold.admin import ModelAdmin
# admin.site.register(ConvertModel)

@admin.register(ConvertModel)
class CustomAdminClass(ModelAdmin):
    pass