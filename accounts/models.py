from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.exceptions import ValidationError
from decimal import Decimal

class CustomUserManager(BaseUserManager):
    def create_user(self, email, full_name, password=None, **extra_fields):
        if not email:
            raise ValueError('The email must be set')
        email=self.normalize_email(email)
        user=self.model(email=email, full_name=full_name, password=None, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, full_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, full_name, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.email

class SubscriptionPlan(models.Model):
    PLAN_CHOICES = (
        ("FREE", "Free"),
        ("PRO", "Pro")
    )
    name = models.CharField(max_length=100, choices=PLAN_CHOICES, unique=True)
    file_limit = models.PositiveIntegerField(default=3)
    conversion_limit = models.PositiveIntegerField(default=3)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))

    def __str__(self):
        return self.name

class UserSubscription(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='subscription')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT)
    conversion_used = models.PositiveIntegerField(default=0)
    file_used = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def can_convert(self):
        return self.conversion_used < self.plan.conversion_limit

    def can_upload_file(self):
        return self.file_used < self.plan.file_limit

    def __str__(self):
        return f'{self.user.full_name} - {self.plan.name}'

class UserIPAddress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="ip_addresses")
    ip_address = models.GenericIPAddressField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["ip_address", "user"]

    def __str__(self):
        return f"{self.user.full_name} - {self.ip_address}"

class ApiKey(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user')
    key = models.CharField(unique=True, null=False)
    max_limit = models.PositiveIntegerField(default=3)
    created_at = models.DateTimeField(auto_now_add=True)
    # life_span = models.DateTimeField(default= Date)

    def clean(self, *args, **kwargs):
        key_count = ApiKey.objects.filter(user=self.user).count()
        if key_count > self.max_limit:
            raise ValidationError({"error": "You have reached the limit"})
        super().clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'key:{self.key} for user:{self.user}'

