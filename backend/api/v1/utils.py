import string

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string

from users.models import User
from api.v1.tasks import send_email


def get_otp():
    return get_random_string(settings.OTP_LENGTH, string.digits)


def send_otp(request):
    user = get_object_or_404(
        User,
        email=request.data.get('email'),
    )
    user.otp = get_otp()
    user.save()
    send_email.delay(
        theme='OTP',
        body=f'Код подтверждения {user.otp}',
        sender='token@example.com',
        recipient=[request.data.get('email')],
    )
