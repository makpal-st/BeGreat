from django.db import models

from utils.services import images_upload


class Image(models.Model):

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображении'

    title = models.CharField(
        max_length=50,
        verbose_name='Описание фотографии',
        blank=True,
        null=True
    )

    image = models.ImageField(
        upload_to=images_upload,
        verbose_name='Изображение',
        blank=True,
        null=True,
    )

    priority = models.IntegerField(
        default=0,
        verbose_name='Приоритет',
        blank=True,
    )

    def __str__(self):
        return f'{self.title}'
