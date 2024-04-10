from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken


from users.models import User


class SignupSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return User.objects.create(
            email=validated_data.get('email'),
            username=validated_data.get('username'),
            password = make_password(validated_data.get('password'))
        )

    
    class Meta:
        model = User
        fields = ('email', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}


class GetTokenObtainPairSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254)
    otp = serializers.CharField(max_length=settings.OTP_LENGTH)

    def validate(self, data):
        email = data.get('email')
        user = get_object_or_404(User, email=email)
        if cache.get(email) != data.get('otp'):
            raise serializers.ValidationError('Не верный otp')
        cache.delete(email)
        return {
            'access': str(AccessToken.for_user(user)),
            'refresh': str(RefreshToken.for_user(user)),
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('email', 'username', 'first_name', 'last_name')
        model = User
