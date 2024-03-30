from django.shortcuts import render, get_object_or_404
from django.contrib.auth.hashers import make_password
from rest_framework import status, viewsets
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from api.v1.permissions import IsMeOrAdminPermission
from api.v1.serializers import SignupSerializer, UserSerializer, GetTokenObtainPairSerializer
from api.v1.utils import send_otp
from users.models import User


class SignupView(APIView):
    """Вью для регистрации пользователей."""

    permission_classes = (AllowAny,)

    def post(self, request):
        """Метод POST."""
        serializer = SignupSerializer(data=request.data)
        if User.objects.filter(username=request.data.get('username'),
                               email=request.data.get('email')).exists():
            send_otp(request)
            return Response({'message': 'пароль отравлен на почту'}, status=status.HTTP_200_OK)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        send_otp(request)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetTokenObtainPairView(TokenObtainPairView):
    """Вью для получения токена"""

    serializer_class = GetTokenObtainPairSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    http_method_names = ('get', 'patch', 'delete')
    search_fields = ('username',)
    permission_classes = (IsMeOrAdminPermission,)