from django.db import models

class ConvertedFile(models.Model):
    original_file = models.FileField(upload_to='uploads/')
    converted_file = models.FileField(upload_to='converted/', null=True, blank=True)
    original_extension = models.CharField(max_length=10)
    target_extension = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.original_extension} → {self.target_extension}"
