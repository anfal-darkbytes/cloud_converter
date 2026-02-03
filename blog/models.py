from django.utils import timezone
from django.db import models
from tinymce.models import HTMLField


class CategoryModel(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class BlogModel(models.Model):
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE, related_name='Category')
    image = models.ImageField(upload_to='blog/')
    title = models.CharField(max_length=100,unique=True)
    description = models.CharField(max_length=50, default='')
    body = models.TextField()
    hash_tag = models.CharField(max_length=50)
    author = models.CharField(max_length=100, default='DarkBytes')
    uploaded_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


