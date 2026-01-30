from django.db import models
from tinymce.models import HTMLField

class BlogModel(models.Model):
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='blog/')
    heading = models.CharField(max_length=100,unique=True)
    description = HTMLField()

    def __str__(self):
        return self.heading
