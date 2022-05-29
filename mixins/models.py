from django.db import models


class TimestampMixin(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Время последнего изменения')


class IsActiveMixin(models.Model):
    class Meta:
        abstract = True

    is_active = models.BooleanField(default=True, verbose_name='Активный?')


