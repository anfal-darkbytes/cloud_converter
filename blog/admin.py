from django.contrib import admin
from .models import BlogModel, CategoryModel
from unfold.admin import ModelAdmin

@admin.register(CategoryModel)
class CategoryAdmin(ModelAdmin):
    list_display= ('name','id')


@admin.register(BlogModel)
class BlogAdmin(ModelAdmin):
    list_display = ('title', 'description', 'category', 'author', 'uploaded_date')