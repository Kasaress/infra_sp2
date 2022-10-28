import datetime as dt
import re

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


def validate_year(value):
    if value > dt.datetime.now().year:
        raise ValidationError(
            'Значение года не может быть больше текущего')
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
        raise ValidationError(
            'Запрещено использовать "me" в качестве никнейма'
        )
    bad_symbols = [symbol for symbol in r'^[\w.@+-]+$' if symbol in value]
    if bad_symbols:
        raise ValidationError(
            f'Юзернейм содержит запрещенные символы: '
            f'{" ".join(str(symbol) for symbol in bad_symbols)}'
        )
    return value


def validate_slug(value):
    print(re.fullmatch(r'^[-a-zA-Z0-9_]+$', value))
    if not re.fullmatch(r'^[-a-zA-Z0-9_]+$', value):
        raise ValidationError(
            'Адрес категории не соответствует шаблону: ^[-a-zA-Z0-9_]+$'
        )
    return value
