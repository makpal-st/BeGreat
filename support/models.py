from django.db import models

from autho.models import User
from mixins.models import TimestampMixin


class Conversation(TimestampMixin):

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='conversations',
        verbose_name='Источник вопроса',
    )

    title = models.CharField(
        max_length=100,
        verbose_name='Заголовок чата'
    )
    text = models.CharField(
        max_length=1000,
        verbose_name='Текст чата'
    )

    def __str__(self):
        return f'{self.title}'


class ConversationAnswer(TimestampMixin):

    class Meta:
        verbose_name = 'Ответ на беседу'
        verbose_name_plural = 'Ответы на беседы'

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        verbose_name='Чат, на которую отвечает',
        related_name='answers'
    )

    text = models.CharField(
        max_length=1000,
        verbose_name='Текст ответа'
    )

    def __str__(self):
        return f'Ответ на {self.conversation}'
