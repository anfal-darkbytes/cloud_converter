from django.db import models

class UploadMultiFileModel(models.Model):
    file = models.FileField(upload_to='uploaded/')

class ConvertedMultiFileModel(models.Model):
    file = models.FileField(upload_to='converted/')

class ConvertModel(models.Model):
    ipaddr = models.GenericIPAddressField(null=True, blank=True)
    uploaded = models.ManyToManyField(UploadMultiFileModel, blank=True)
    converted = models.ManyToManyField(
        ConvertedMultiFileModel,
        null=True,
        blank=True
    )
    from_format = models.CharField(max_length=100, default='')
    to_format = models.CharField(max_length=100, default='')
    created_at = models.DateField()

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.converted}' if self.converted else "Not Converted Yet"
