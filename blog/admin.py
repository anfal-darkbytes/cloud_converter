from django.contrib import admin
from .models import BlogModel, CategoryModel

@admin.register(CategoryModel)
class CategoryAdmin(admin.ModelAdmin):
    list_display= ('name','id')


@admin.register(BlogModel)
class BlogAdmin(admin.ModelAdmin):
    list_display = [field.name for field in BlogModel._meta.fields]