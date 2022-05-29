from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.postgres.fields import ArrayField
from django.db import models, transaction
from django.utils import timezone

from autho.services import avatar_upload
from autho.validators import validate_image
from mixins.models import TimestampMixin


class UserManager(BaseUserManager):

    def create_user(self, email, phone=None, password=None, **kwargs):
        """
        Creates and saves a user with the given phone and password
        """
        user = self.model(phone=phone, email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given phone and password
        """
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.is_superuser = True
        user.is_moderator = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        unique_together = ('phone', 'email')

    first_name = models.CharField(
        max_length=100,
        verbose_name='Имя',
    )
    last_name = models.CharField(
        max_length=100,
        verbose_name='Фамилия',
        blank=True,
        null=True
    )
    middle_name = models.CharField(
        max_length=100,
        verbose_name='Отчества',
        blank=True,
        null=True
    )
    phone = models.CharField(
        unique=True,
        max_length=50,
        verbose_name='Номер телефона',
        null=True,
    )
    email = models.EmailField(
        unique=True,
        max_length=50,
        verbose_name='Рабочая почта',
        null=True
    )

    is_admin = models.BooleanField(
        default=False
    )

    region = models.CharField(
        max_length=50,
        verbose_name='Регион',
        blank=True,
        null=True
    )

    USERNAME_FIELD = 'email'

    objects = UserManager()

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def __str__(self):
        return f'{self.email} - {self.phone}'


class Account(TimestampMixin):

    class Meta:
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунты'

    user = models.OneToOneField(
        User,
        on_delete=models.PROTECT,
        verbose_name='Пользователь',
        related_name='account'
    )

    interested_courses = ArrayField(
        models.IntegerField(),
        default=list,
        blank=True
    )

    avatar = models.ImageField(
        verbose_name='Аватар',
        blank=True,
        null=True,
        upload_to=avatar_upload,
        validators=[validate_image],
    )

    passed_lectures = ArrayField(
        models.IntegerField(),
        default=list,
        blank=True,
        verbose_name='Id пройденных курсов'
    )

    @classmethod
    def create(cls, user):
        with transaction.atomic():
            account = cls.objects.create(
                user=user,
                interested_courses=[],
                avatar=None
            )
        return account

    def __str__(self):
        return f'Account - {self.user}'


class TokenLog(TimestampMixin):
    """
    Token log model
    """
    user = models.ForeignKey(
        User,
        related_name='tokens',
        on_delete=models.CASCADE
    )
    token = models.CharField(max_length=500)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return "token={0}".format(self.token)

    class Meta:
        index_together = [
            ["token", "user"]
        ]
        verbose_name = 'Токен'
        verbose_name_plural = 'Токены'
