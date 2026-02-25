from django.db import models

class ConvertModel(models.Model):
    ipaddr = models.GenericIPAddressField(null=True, blank=True)
    from_format = models.CharField(max_length=100, default='')
    to_format = models.CharField(max_length=100, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.ipaddr} | {self.from_format} to {self.to_format}"

class UploadMultiFileModel(models.Model):
    file = models.FileField(upload_to='uploaded/')
    convert = models.ForeignKey(
        ConvertModel,
        on_delete=models.CASCADE,
        related_name='uploaded_files'
    )

class ConvertedMultiFileModel(models.Model):
    file = models.FileField(upload_to='converted/')
    convert = models.ForeignKey(
        ConvertModel,
        on_delete=models.CASCADE,
        related_name='converted_files'
    )


