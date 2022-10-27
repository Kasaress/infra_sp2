import datetime as dt

from django.core.exceptions import ValidationError


def validate_year(value):
    if value > dt.datetime.now().year:
        raise ValidationError(
            'Значение года не может быть больше текущего')
    return value
