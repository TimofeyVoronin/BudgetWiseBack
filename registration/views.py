from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import CustomUserSerializer

class RegistrationAPIView(APIView):
    """
    POST /reg/register/
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            refresh.payload.update({
                'user_id': user.id,
                'username': user.username,
            })
            return Response({
                'refresh': str(refresh),
                'access':  str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    """
    POST /reg/login/
    """
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        email = data.get('email')
        password = data.get('password')

        if email is None or password is None:
            return Response(
                {'error': 'Нужны и email, и password'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(username=email, password=password)
        if user is None:
            return Response(
                {'error': 'Неверные учётные данные'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)
        refresh.payload.update({
            'user_id': user.id,
            'username': user.username,
        })
        return Response({
            'refresh': str(refresh),
            'access':  str(refresh.access_token),
        }, status=status.HTTP_200_OK)


class LogoutAPIView(APIView):
    """
    POST /reg/logout/
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            return Response(
                {'error': 'Необходим refresh_token'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            return Response(
                {'error': 'Неверный refresh_token'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response({'success': 'Выход выполнен'}, status=status.HTTP_200_OK)
