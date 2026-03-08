from accounts.models import UserSubscription, UserIPAddress
from django.core.exceptions import PermissionDenied


class ConversionService:

    @staticmethod
    def validate_conversion(user, ip_address, files):

        if not user.is_authenticated:
            raise PermissionDenied("Login required")

        subscription = user.subscription

        if len(files) > 1:
            raise PermissionDenied("Free plan allows only 1 file per conversion")

        if not subscription.can_convert():
            raise PermissionDenied("Conversion limit reached")

        if not subscription.can_upload_file():
            raise PermissionDenied("File limit reached")

        existing_ips = UserIPAddress.objects.filter(ip_address=ip_address)

        if existing_ips.exists():
            for record in existing_ips:
                other_sub = record.user.subscription
                if other_sub.files_used >= other_sub.plan.file_limit * other_sub.plan.conversion_limit:
                    raise PermissionDenied(
                        "Free usage already consumed from this IP address"
                    )

    @staticmethod
    def update_usage(user, file_count):

        subscription = user.subscription

        subscription.conversions_used += 1
        subscription.files_used += file_count

        subscription.save()