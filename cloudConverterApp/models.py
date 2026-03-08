from django.db import models
from decimal import Decimal

class ConvertModel(models.Model):
    user = models.ForeignKey("accounts.CustomUser", on_delete=models.SET_NULL, null=True, blank=True)
    ipaddr = models.GenericIPAddressField()
    from_format = models.CharField(max_length=100)
    to_format = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    total_files = models.PositiveIntegerField(default=1)
    total_size = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created_at']

class UploadMultiFileModel(models.Model):
    file = models.FileField(upload_to='uploaded/')
    convert = models.ForeignKey(ConvertModel, on_delete=models.CASCADE, related_name='uploaded_files')

class ConvertedMultiFileModel(models.Model):
    file = models.FileField(upload_to='converted/')
    convert = models.ForeignKey(ConvertModel, on_delete=models.CASCADE, related_name='converted_files')

class RateModel(models.Model):
    convert = models.OneToOneField(ConvertModel, on_delete=models.CASCADE, related_name='file_size')
    rate_per_kb = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    @property
    def total_price(self):
        return self.rate_per_kb * (self.convert.total_size/1024)

    def __str__(self):
        return f'rate per kb: {self.rate_per_kb}'

class ContactUsModel(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(null=False)
    subject = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return f'{self.name}'

