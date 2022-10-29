import datetime as dt
import re

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


def validate_year(value):
    if value > dt.datetime.now().year:
        raise ValidationError(settings.YEAR_ERROR_MESSAGE)
    return value


class UserValidatorMixin:
    username = models.CharField(
        max_length=settings.USER_NAMES_LENGTH,
        verbose_name='Никнейм',
        unique=True,
        null=True,
    )

    def validate_username(self, value):
        return validate_name(value)


def validate_name(value):
    if value == 'me':
        raise ValidationError(settings.NAME_ME_ERROR_MESSAGE)
    bad_symbols = [
        symbol for symbol in settings.FORBIDDEN_SYMBOLS if symbol in value
    ]
    if bad_symbols:
        # forbidden_symbols = r"^[\w.@+-]+$"
        raise ValidationError(
            f'Юзернейм содержит запрещенные символы:'
            f'{" ".join(str(symbol) for symbol in bad_symbols)}'
            # f'{"".join(set(re.sub(settings.FORBIDDEN_SYMBOLS, "", value)))}'
            # некорректно работает с нашим паттерном, а если даже будет,
            # выведет разрешенные символы, а не запрещенные
            # f'{re.sub(forbidden_symbols, "", value)}'  # не меняет строчку
        )
    return value


def validate_slug(value):
    if not re.fullmatch(settings.SLUG_PATTERN, value):
        raise ValidationError(settings.SLUG_ERROR_MESSAGE)
    return value
