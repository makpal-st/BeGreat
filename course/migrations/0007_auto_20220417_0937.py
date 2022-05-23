# Generated by Django 3.2.12 on 2022-04-17 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0006_usercourse_anonymous_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Время последнего изменения')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активный?')),
                ('title', models.CharField(max_length=50, verbose_name='Заголовок лекции')),
                ('context', models.TextField(verbose_name='Текст лекции')),
            ],
            options={
                'verbose_name': 'Лекция',
                'verbose_name_plural': 'Лекции',
            },
        ),
        migrations.RemoveField(
            model_name='questionoption',
            name='result_text',
        ),
        migrations.AlterField(
            model_name='questionoption',
            name='value',
            field=models.IntegerField(blank=True, max_length=1, verbose_name='Баллы за ответ'),
        ),
    ]