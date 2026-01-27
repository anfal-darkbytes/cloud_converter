from django.db import models

class ConvertModel(models.Model):
    uploaded = models.FileField(upload_to='uploaded/')
    converted = models.FileField(upload_to='converted/')
    from_format = models.CharField(max_length=100, default='')
    to_format = models.CharField(max_length=100, default='')
    created_at = models.DateField()

    class Meta:
        ordering = ['created_at']

    def  __str__(self):
        return f'{self.converted}'