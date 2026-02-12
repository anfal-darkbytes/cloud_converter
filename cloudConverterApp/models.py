from django.db import models


class ConvertModel(models.Model):
    ipaddr = models.GenericIPAddressField(null=True, blank=True)
    from_format = models.CharField(max_length=100, default='')
    to_format = models.CharField(max_length=100, default='')
    created_at = models.DateField()

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.from_format} to {self.to_format}'


class UploadMultiFileModel(models.Model):
    file = models.FileField(upload_to='uploaded/')
    convert = models.ManyToManyField(ConvertModel, blank=True)

class ConvertedMultiFileModel(models.Model):
    file = models.FileField(upload_to='converted/')
    convert = models.ManyToManyField(ConvertModel, blank=True)
