import string

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string

from users.models import User


def get_otp():
    """Генерирует opt."""
    return get_random_string(settings.OTP_LENGTH, string.digits)


def send_otp(request):
    """Отправляет сгенерированный opt пользователю."""
    user = get_object_or_404(
        User,
        email=request.data.get('email'),
    )
    user.otp = get_otp()
    user.save()
    send_mail(
        'OTP',
        f'Код подтверждения {user.otp}',
        'token@example.com',
        [request.data.get('email')],
    )
