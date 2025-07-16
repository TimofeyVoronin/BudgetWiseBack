from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, OpenApiResponse
from drf_spectacular.utils import extend_schema

from .serializers import (
    CustomUserSerializer,
    LoginSerializer,
    TokenPairSerializer,
    LogoutSerializer,
    ProfileSerializer,
    ChangePasswordSerializer
)


@extend_schema(
    request=CustomUserSerializer,
    responses={201: CustomUserSerializer}
)
@extend_schema(tags=['Auth'])
class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(
    request=LoginSerializer,
    responses={200: TokenPairSerializer}
)
@extend_schema(tags=['Auth'])
class LoginAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = authenticate(username=email, password=password)
        if user is None:
            return Response(
                {'error': 'Неверные учётные данные'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)
        tokens = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
        return Response(tokens, status=status.HTTP_200_OK)


@extend_schema(
    request=LogoutSerializer,
    responses={200: OpenApiResponse(description="{'success': 'Выход выполнен'}")}
)
@extend_schema(tags=['Auth'])
class LogoutAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh_token = serializer.validated_data['refresh_token']
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            return Response(
                {'error': 'Неверный refresh_token'},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({'success': 'Выход выполнен'}, status=status.HTTP_200_OK)


@extend_schema(
    responses=ProfileSerializer
)
@extend_schema(tags=['Auth'])
class ProfileAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user


@extend_schema(
    request=ChangePasswordSerializer,
    responses={200: OpenApiResponse(description="{'detail': 'Пароль успешно изменён'}")}
)
@extend_schema(tags=['Auth'])
class ChangePasswordAPIView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return Response(
            {"detail": "Пароль успешно изменён"},
            status=status.HTTP_200_OK
        )
