# Generated by Django 3.2.12 on 2022-04-20 17:41

from django.db import migrations, models
import utils.services


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=utils.services.images_upload, verbose_name='Изображение'),
        ),
    ]
