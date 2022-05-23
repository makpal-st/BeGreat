from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from api.models import Image
from autho.models import User
from mixins.models import TimestampMixin, IsActiveMixin


class Course(TimestampMixin):

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    name = models.CharField(
        max_length=100,
        verbose_name='Наименование курса',
        blank=False,
        null=False
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name='Активный курс?'
    )

    priority = models.IntegerField(
        default=0,
        verbose_name='Приоритетность курсов',
        blank=True
    )

    def __str__(self):
        return f'{self.name}'


class Category(models.Model):

    HARD = 'Сложный'
    MEDIUM = 'Средний'
    EASY = 'Легкий'

    LEVEL_CHOICES = (
        (EASY, EASY),
        (MEDIUM, MEDIUM),
        (HARD, HARD)
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    name = models.CharField(
        max_length=100,
        verbose_name='Имя категории',
        blank=False,
        null=False
    )

    level = models.CharField(
        max_length=100,
        choices=LEVEL_CHOICES,
        verbose_name='Уровень сложности'
    )

    grade = models.IntegerField(
        verbose_name='Класс для которого предназначена категория',
        default=0,
        blank=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(12)
        ]
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name='Курс',
        related_name='categories'
    )

    def __str__(self):
        return f'{self.name}'


class Question(models.Model):

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ['-priority']

    title = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Заголовок вопроса'
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Категория к которому относится вопрос',
        related_name='questions'
    )

    description = models.CharField(
        max_length=100,
        verbose_name='Описание вопроса'
    )

    priority = models.IntegerField(
        default=0,
        verbose_name='Приоритет'
    )

    images = models.ManyToManyField(
        Image,
        verbose_name='Изображении',
        blank=True
    )

    def __str__(self):
        return f'{self.title}'


class QuestionOption(models.Model):

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
        ordering = ['-priority']
        unique_together = ('priority', 'question')

    question = models.ForeignKey(
        Question,
        related_name='options',
        max_length=256,
        verbose_name='Текст вопроса',
        on_delete=models.CASCADE,
    )
    priority = models.PositiveSmallIntegerField(
        verbose_name='Приоритет',
        default=0,
        blank=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(4)
        ]
    )
    option_text = models.CharField(
        max_length=256,
        verbose_name='Вариант ответа',
        blank=True
    )
    value = models.IntegerField(
        verbose_name='Баллы за ответ',
        validators=[
            MinValueValidator(0),
            MaxValueValidator(1)
        ],
        blank=True
    )

    def __str__(self):
        return f'{self.option_text} - {self.value}'


class MultiTest(TimestampMixin):

    class Meta:
        verbose_name = 'Мультитест'
        verbose_name_plural = 'Мультитесты'
        ordering = ('-created_at', )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='multitests',
        verbose_name='Пользователь для которого тест',
    )

    question = models.ManyToManyField(
        Question,
        verbose_name='Вопросы',
        blank=True
    )

    result = models.IntegerField(
        default=0,
        verbose_name='Результат'
    )

    def __str__(self):
        return f'Мультитест для - {self.user}'


class QuestionAnswer(TimestampMixin):

    MULTITEST = "MULTITEST"
    TEST = "TEST"

    TYPES = (
        (MULTITEST, MULTITEST),
        (TEST, TEST)
    )

    class Meta:
        verbose_name = 'Ответ на вопрос'
        verbose_name_plural = 'Ответы на вопросы'

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        verbose_name='Вопрос'
    )
    option = models.ForeignKey(
        QuestionOption,
        on_delete=models.CASCADE,
        verbose_name='Вариант ответа'
    )

    type = models.CharField(
        max_length=50,
        default=TEST,
        verbose_name='Тип ответа'
    )

    attempt_counter = models.IntegerField(
        default=0,
        verbose_name='Попытка ответить на этот вопрос',
        help_text='Увеличивается при каждой попытке ответить на вопрос'
    )

    multitest = models.ForeignKey(
        MultiTest,
        on_delete=models.CASCADE,
        verbose_name='Мультитест',
        blank=True, null=True
    )

    def __str__(self):
        return f'{self.user} - {self.option}'


class UserCourse(TimestampMixin):

    class Meta:
        verbose_name = 'Прохождение курса'
        verbose_name_plural = 'Прохождение курсов'

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='courses',
        verbose_name='Студент курса',
        null=True,
        blank=True
    )

    anonymous_user = models.CharField(
        max_length=500,
        verbose_name='Тег для анонимного юзера',
        blank=True,
        null=True
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='Текущая категория курса',
        null=True
    )

    is_finished = models.BooleanField(
        verbose_name='Курс закончен?',
        default=False
    )

    score = models.IntegerField(
        verbose_name='Оценка по окончанию',
        blank=True,
        null=True,
    )

    note = models.TextField(
        verbose_name='Заметки юзера',
        blank=True,
        null=True
    )

    def __str__(self):
        return f'{self.user} - {self.category}'


class Lecture(TimestampMixin, IsActiveMixin):

    class Meta:
        verbose_name = 'Лекция'
        verbose_name_plural = 'Лекции'
        ordering = ('-priority', )

    title = models.CharField(
        max_length=50,
        verbose_name='Заголовок лекции'
    )

    context = models.TextField(
        verbose_name='Текст лекции'
    )

    priority = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(1000)
        ],
        verbose_name='Приоритет материалов'
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Курс к которому относится материал',
        related_name='lectures'
    )

    images = models.ManyToManyField(
        Image,
        verbose_name='Изображении',
        blank=True,
    )

    def __str__(self):
        return f'{self.title}'
