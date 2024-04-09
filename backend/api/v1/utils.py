import string

from django.conf import settings
from django.core.cache import cache
from django.utils.crypto import get_random_string

from users.models import User
from api.v1.tasks import send_email


def get_otp():
    return get_random_string(settings.OTP_LENGTH, string.digits)


def send_otp(request):
    email = request.data.get('email')
    cache.set(email, get_otp())
    send_email.delay(
        theme='OTP',
        body=f'Код подтверждения {cache.get(email)}',
        sender='token@example.com',
        recipient=[email],
    )
