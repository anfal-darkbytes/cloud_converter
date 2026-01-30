from django.contrib import admin
from .models import BlogModel

class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug': 'heading'}

admin.site.register(BlogModel)
