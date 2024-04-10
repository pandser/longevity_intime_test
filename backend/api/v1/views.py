from rest_framework import status, viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from api.v1.permissions import IsMeOrAdminPermission
from api.v1.serializers import (SignupSerializer, UserSerializer,
                                GetTokenObtainPairSerializer)
from api.v1.utils import send_otp
from users.models import User



class SignupView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        send_otp(request)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LoginView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            send_otp(request)
            return Response(
                {'message': 'пароль отравлен на почту'},
                status=status.HTTP_200_OK
            )
        except AuthenticationFailed as error:
            return error


class GetTokenObtainPairView(TokenObtainPairView):
    serializer_class = GetTokenObtainPairSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    http_method_names = ('get', 'patch', 'delete')
    search_fields = ('username',)
    permission_classes = (IsMeOrAdminPermission,)
