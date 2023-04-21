from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.shortcuts import render

# Create your views here.
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework import serializers, permissions

from semester_registration.errors import AppError
from users.http_helpers import ok, bad_request, no_content
from users.models import User
from users.services import email_exists, username_exists, register_user, resend_verification_email, verify_user_email, \
    change_password, send_forget_password_email, check_secret, reset_password
from users.validators import password_validator


class RegisterAPIView(APIView):

    permission_classes = [permissions.AllowAny]

    class RegisterSerializer(serializers.Serializer):
        username = serializers.CharField(max_length=40, validators=[RegexValidator(r'\d+', message="شماره دانشجویی غیر مجاز")])
        password = serializers.CharField(validators=[password_validator])
        email = serializers.EmailField()
        gender = serializers.CharField()

        def validate_email(self, value):
            exist = email_exists(email=value)
            if exist:
                raise ValidationError("آدرس ایمیل توسط کاربر دیگری استفاده شده")
            return value

        def validate_username(self, value):
            exist = username_exists(username=value)
            if exist:
                raise ValidationError("این شماره دانشجویی توسط کاربر دیگری استفاده شده")
            return value

        def update(self, instance, validated_data):
            pass

        def create(self, validated_data):
            pass

    def post(self, request: Request):
        sr = self.RegisterSerializer(data=request.data)
        if not sr.is_valid():
            return bad_request(sr.errors)
        tokens = register_user(**sr.validated_data)
        return ok(tokens)