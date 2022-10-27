
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models

ROLE_CHOICES = (
    (settings.USER, 'Пользователь'),
    (settings.MODERATOR, 'Модератор'),
    (settings.ADMIN, 'Администратор'),
)


class UserValidatorMixin:
    username = models.CharField(
        max_length=settings.USER_NAMES_LENGTH,
        verbose_name='Никнейм',
        unique=True,
        null=True,
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+$',
            message='Юзернейм содержит запрещенный символ'
        )]
    )

    def validate_username(self, value):
        if value == 'me':
            raise ValidationError(
                "Запрещено использовать 'me' в качестве никнейма"
            )
        return value


class CustomUser(AbstractUser, UserValidatorMixin):  # type: ignore
    """Кастомная модель User.
       Позволяет при создании запрашивать емейл и юзернейм.
    """
    username: str = models.CharField(
        'Username',
        unique=True,
        blank=False,
        max_length=settings.USER_NAMES_LENGTH,
    )
    email: str = models.EmailField(
        'E-mail address',
        unique=True,
        blank=False,
        max_length=settings.EMAIL_LENGTH,
    )
    first_name: str = models.CharField(
        'first name',
        max_length=settings.USER_NAMES_LENGTH,
        blank=True
    )
    last_name: str = models.CharField(
        'last name',
        max_length=settings.USER_NAMES_LENGTH,
        blank=True
    )
    bio: str = models.TextField(
        'Биография пользователя',
        blank=True
    )
    role: str = models.CharField(
        max_length=len(max(ROLE_CHOICES)),
        choices=ROLE_CHOICES,
        default='user'
    )
    confirmation_code: str = models.CharField(
        max_length=settings.CONFIRMATION_CODE_LEN, null=True,
        verbose_name='Код подтверждения',
        default=' '
    )

    class Meta:
        ordering = ('id',)
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_name'
            ),
        ]

    def __str__(self) -> str:
        """Строковое представление модели (отображается в консоли)."""
        return self.username

    @property
    def is_admin(self):
        return ((self.role == settings.ADMIN)
                or self.is_superuser or self.is_staff)

    @property
    def is_moderator(self):
        return self.role == settings.MODERATOR
