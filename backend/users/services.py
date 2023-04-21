import secrets
from smtplib import SMTPException

from django.conf import settings
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.mail import send_mail
from django.db import transaction
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken

from semester_registration.errors import AppError
from users.models import User, UserVerificationCode


def email_exists(*args, email: str) -> bool:
    return User.objects.filter(email=email).exists()


def username_exists(*args, username: str) -> bool:
    return User.objects.filter(username=username).exists()


def register_user(*args, username: str, password: str, email: str, gender: str) -> dict:
    with transaction.atomic():
        user = User.objects.create(username=username, email=email, gender=gender)
        user.email_verified = True
        user.set_password(password)
        user.save()
        return get_tokens_for_user(user=user)


def get_tokens_for_user(*args, user: User):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def change_password(*args, user: User, old_password: str, new_password: str):
    auth_user = authenticate(username=user.username, password=old_password)
    if auth_user is None:
        raise AppError("کلمه عبور اشتباه است")
    user.set_password(new_password)
    user.save()
    return user


def check_secret(*args, email, secret):
    try:
        code = UserVerificationCode.objects.get(
            user__email=email,
            code=secret,
            expire_date__gt=timezone.now()
        )
    except ObjectDoesNotExist:
        raise AppError("لینک منقضی شده یا اشتباه است")


def reset_password(*args, email, secret, new_password):
    try:
        code = UserVerificationCode.objects.get(
            user__email=email,
            code=secret,
            expire_date__gt=timezone.now()
        )
        code.user.set_password(new_password)
        code.user.save()
        code.delete()
    except ObjectDoesNotExist:
        raise AppError("لینک منقضی شده یا اشتباه است")
