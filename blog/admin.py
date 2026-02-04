from django.contrib import admin
from django.db import models
from .models import BlogModel, CategoryModel
from unfold.admin import ModelAdmin
from tinymce.widgets import TinyMCE

@admin.register(CategoryModel)
class CategoryAdmin(ModelAdmin):
    list_display= ('name','id')


@admin.register(BlogModel)
class BlogAdmin(ModelAdmin):
    list_display = ('title', 'description', 'category', 'author', 'uploaded_date')
    formfield_overrides = {
        models.TextField: {
            "widget": TinyMCE(),
        }
    }