from .models import CustomUser
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'full_name', 'password']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            full_name=validated_data['full_name'],
            password=validated_data['password']
        )
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)

        return {
            "id": instance.id,
            "email": instance.email,
            "full_name": instance.full_name,
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        }

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            email=data['email'],
            password=data['password']
        )

        if not user:
            raise serializers.ValidationError("Invalid email or password.")

        if not user.is_active:
            raise serializers.ValidationError("Account is disabled.")

        refresh = RefreshToken.for_user(user)

        return {
            "user": user,
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        }