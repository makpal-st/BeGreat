# Generated by Django 3.2.12 on 2022-05-22 14:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0021_alter_question_description'),
        ('achievement', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userachievement',
            name='multitest',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='course.multitest', verbose_name='Тест за которого юзер получил достижение'),
        ),
    ]