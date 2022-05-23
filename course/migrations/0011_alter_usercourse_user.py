# Generated by Django 3.2.12 on 2022-04-17 13:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('course', '0010_lecture_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercourse',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='courses', to=settings.AUTH_USER_MODEL, verbose_name='Студент курса'),
        ),
    ]
