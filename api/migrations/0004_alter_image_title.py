# Generated by Django 3.2.12 on 2022-04-20 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20220420_1748'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='title',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Описание фотографии'),
        ),
    ]