import re

from django.core.exceptions import ValidationError


def password_validator(value):

    result = re.match("^(?=.*\\d)(?=.*[a-z])(?=.*[A-Z]).{8,30}$", value)

    if result is None:
        raise ValidationError('کلمه عبور باید شامل یک حرف بزرگ، یک حرف کوچک و عدد و طول آن بین 8 تا 16 کاراکتر باشد')

    return value
