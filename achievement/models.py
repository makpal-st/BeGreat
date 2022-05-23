from django.db import models
from django.contrib.auth import get_user_model

from mixins.models import TimestampMixin, IsActiveMixin
from utils.services import prize_upload
from utils.validators import validate_pdf

User = get_user_model()


class Achievement(IsActiveMixin):

    MULTI_TEST = 'MULTI_TEST'

    TYPES = (
        (MULTI_TEST, MULTI_TEST),
    )

    class Meta:
        verbose_name = 'Достижение'
        verbose_name_plural = 'Достижении'

    title = models.CharField(
        max_length=50,
        verbose_name='Заголовок'
    )

    description = models.TextField(
        verbose_name='Описание достижении'
    )

    type = models.CharField(
        max_length=50,
        choices=TYPES,
        verbose_name='Тип достижения'
    )

    show_text = models.CharField(
        max_length=200,
        verbose_name='Текст при достижении'
    )

    min_points = models.IntegerField(
        default=50,
        verbose_name='Минимальные баллы для достижения'
    )

    prize = models.FileField(
        upload_to=prize_upload,
        validators=[validate_pdf],
        verbose_name='Приз',
    )

    def __str__(self):
        return f'{self.title}'


class UserAchievement(TimestampMixin):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='achievements'
    )

    achievement = models.ForeignKey(
        Achievement,
        on_delete=models.CASCADE,
        verbose_name='Достижение'
    )

    class Meta:
        verbose_name = 'Достижение пользователя'
        verbose_name_plural = 'Достижении пользователей'
