from django.contrib import admin
from .models import CustomUser, SubscriptionPlan, UserSubscription, UserIPAddress, ApiKey
from unfold.admin import ModelAdmin

@admin.register(CustomUser)
class CustomUserAdmin(ModelAdmin):
    pass

@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(ModelAdmin):
    pass

@admin.register(UserSubscription)
class UserSubscriptionAdmin(ModelAdmin):
    pass

@admin.register(UserIPAddress)
class UserIPAddressAdmin(ModelAdmin):
    pass

@admin.register(ApiKey)
class ApiKeyAdmin(ModelAdmin):
    pass