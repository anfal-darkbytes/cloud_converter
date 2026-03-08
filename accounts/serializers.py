from .models import CustomUser, ApiKey
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .utils import generate_unique_uuid_string


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['full_name', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        if CustomUser.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"error": "User with this email already exists"})
        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            full_name=validated_data['full_name'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            username=data['email'],
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


class KeySerializer(serializers.Serializer):
    class Meta:
        model = CustomUser
        fields = ['email']

    def validate(self, attrs):
        if not CustomUser.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({'error':'User not found'})
        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.filter(email=validated_data['email'])
        key = generate_unique_uuid_string()
        created_key = ApiKey.objects.create(
            user=user,
            key = key,
        )
        return created_key
