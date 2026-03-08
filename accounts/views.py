from rest_framework import status
from .models import CustomUser
from .serializers import RegistrationSerializer, KeySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import LoginSerializer
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

def login(request):
    # if request.user.is_authenticated:
    #     return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password')

    return render(request, 'accounts/login.html')

def signup(request):
    if request.method == 'POST':

        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Password and confirm password mismatch')
            return render(request, 'accounts/signup.html')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'User with this email already exists')
            return render(request, 'accounts/signup.html')

        try:
            user = CustomUser.objects.create_user(
                email=email,
                full_name=full_name,
                password=password
            )

            messages.success(request, 'Account created successfully')
            return redirect('login')

        except Exception as e:
            print(f'error: {e}')

    return render(request, 'accounts/signup.html')

class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "User registered successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        tokens = serializer.validated_data["tokens"]

        return Response({
            "success": True,
            "message": "Login successful.",
            "data": {
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "full_name": user.full_name,
                },
                "tokens": tokens
            }
        }, status=status.HTTP_200_OK)

class CreateApiKey(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({
                'success':False,
                'error': 'Email field is missing'
            })
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({
            "success": True,
            "data": serializer.data
        })
