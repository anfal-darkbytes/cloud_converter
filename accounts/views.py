from rest_framework import generics, status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from .serializers import RegisterSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import LoginSerializer

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response({
            "success": True,
            "message": "User registered successfully.",
            "data": {
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "full_name": user.full_name,
                },
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            }
        }, status=status.HTTP_201_CREATED)




class LoginView(APIView):

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