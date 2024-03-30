from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken


from users.models import User


class SignupSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователей."""

    def create(self, validated_data):
        return User.objects.create(
            email=validated_data.get('email'),
            username=validated_data.get('username'),
            password = make_password(validated_data.get('password'))
        )
    
    def update(self, instance, validated_data):
        instance.email = validated_data.get('eamil', instance.email)
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        return instance
    
    class Meta:
        model = User
        fields = ('email', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}


class GetTokenObtainPairSerializer(serializers.Serializer):
    """Сериализатор получения токена."""

    email = serializers.EmailField(max_length=254)
    otp = serializers.CharField(max_length=settings.OTP_LENGTH)

    def validate(self, data):
        user = get_object_or_404(User, email=data.get('email'))
        if user.otp != data.get('otp'):
            raise serializers.ValidationError('Не верный otp')
        user.otp = ''
        user.save()
        return {
            'access': str(AccessToken.for_user(user)),
            'refresh': str(RefreshToken.for_user(user)),
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('email', 'username', 'first_name', 'last_name')
        model = User
