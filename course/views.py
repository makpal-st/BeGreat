from django.shortcuts import render
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import mixins, viewsets
from rest_framework.decorators import permission_classes, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from course.models import Course, Category, Question, Lecture, MultiTest
from course.serializers import CourseSerializer, JoinCourseSerializer, CategorySerializer, UserCourseSerializer, \
    QuestionSerializer, LectureSerializer, NoteSerializer, AnswerSubmitSerializer, AnswerResultSerializer, \
    MultitestAnswerSubmitSerializer, UserAchievementSerializer
from utils.handlers import response_code_wrapper
from utils.pagination import CategoryPagination


@method_decorator(response_code_wrapper(), name='dispatch')
class CourseViewSet(
    viewsets.GenericViewSet,
):
    filter_backends = (DjangoFilterBackend,)

    def get_object(self):
        course_id = self.kwargs['course_id']
        return self.get_queryset().filter(id=course_id).first()

    def get_queryset(self):
        return Category.objects.all()

    def get_serializer_class(self):
        if self.action == 'list_categories':
            return CategorySerializer
        elif self.action == 'join_course':
            return JoinCourseSerializer
        elif self.action == 'list_courses':
            return CourseSerializer
        return None

    @extend_schema(
        responses={
            200: CategorySerializer
        }
    )
    def list_categories(self, request, *args, **kwargs):
        course_id = self.kwargs['course_id']
        course: Course = Course.objects.filter(id=course_id).first()
        if not course:
            raise ValidationError('Курс не существует!')
        serializer = self.get_serializer(course.categories, many=True)
        return Response(serializer.data)

    def list_courses(self, request, *args, **kwargs):
        courses = Course.objects.filter(is_active=True).order_by('-priority')
        serializer = self.get_serializer(courses, many=True)
        return Response(serializer.data)

    @action(methods=("POST",), detail=True, permission_classes=(IsAuthenticated, ))
    def join_course(self, request, *args, **kwargs):
        from course.services import join_course
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_course = join_course(**serializer.validated_data)
        response = UserCourseSerializer(user_course)
        return Response(response.data)


class CourseLecturesViewSet(
    viewsets.GenericViewSet,
):
    filter_backends = (DjangoFilterBackend,)
    pagination_class = CategoryPagination

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        return Lecture.objects.filter(category_id=category_id).select_related('category').order_by('-priority')

    def get_serializer_class(self):
        if self.action == 'lecture_materials':
            return LectureSerializer
        return None

    @extend_schema(
        responses={
            200: LectureSerializer(many=True)
        }
    )
    def lecture_materials(self, request, *args, **kwargs):
        from course.services import add_passed_lectures
        page = self.paginate_queryset(self.get_queryset())
        serializer = self.get_serializer(page, many=True)
        if request.user.is_authenticated:
            add_passed_lectures(request.user, page)
        return self.get_paginated_response(serializer.data)


@method_decorator(response_code_wrapper(), name='dispatch')
class LectureNoteViewSet(
    viewsets.GenericViewSet
):

    def get_serializer_class(self):
        if self.action == 'post_note':
            return NoteSerializer
        return None

    def post_note(self, request, *args, **kwargs):
        from course.services import save_note
        serializer = self.get_serializer(data=request.data, context={'request': self.request, 'kwargs': self.kwargs})
        serializer.is_valid(raise_exception=True)
        category_id = self.kwargs.get('category_id')
        save_note(request.user, category_id, **serializer.validated_data)
        return Response()


@method_decorator(response_code_wrapper(), name='dispatch')
class CourseSurveyViewSet(
    viewsets.GenericViewSet,
):
    filter_backends = (DjangoFilterBackend, )
    pagination_class = CategoryPagination
    permission_classes = (IsAuthenticated,)
    lookup_field = 'category_id'

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        return Question.objects.filter(category_id=category_id).select_related('category').order_by('-priority')

    def get_serializer_class(self):
        if self.action == 'questions':
            return QuestionSerializer
        elif self.action == 'submit_answer':
            return AnswerSubmitSerializer
        return None

    @extend_schema(
        responses={
            200: QuestionSerializer(many=True)
        }
    )
    def questions(self, request, *args, **kwargs):
        page = self.paginate_queryset(self.get_queryset())
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @extend_schema(
        responses={
            200: AnswerResultSerializer
        }
    )
    def submit_answer(self, request, category_id, *args, **kwargs):
        from course.services import check_answer
        serializer = self.get_serializer(data=request.data, context={'request': request, 'category_id': category_id})
        serializer.is_valid(raise_exception=True)
        response = check_answer(self.request.user, **serializer.validated_data)
        return Response(AnswerResultSerializer(response).data)


@method_decorator(response_code_wrapper(), name='dispatch')
class MultitestViewSet(viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, )
    pagination_class = CategoryPagination

    def get_queryset(self):
        multi_test = MultiTest.objects.filter(user=self.request.user, result=0).first()
        if multi_test:
            return multi_test.question.all()
        return MultiTest.objects.none()

    def get_serializer_class(self):
        if self.action == 'generate':
            return None
        elif self.action == 'submit_answer':
            return MultitestAnswerSubmitSerializer
        elif self.action == 'get_result':
            return UserAchievementSerializer
        return QuestionSerializer

    def generate(self, request, *args, **kwargs):
        from course.services import generate_multitest
        if len(request.user.account.passed_lectures) < 1:
            raise ValidationError('Вы еще не прошли необходимое количество курсов')
        generate_multitest(request.user)
        return Response()

    @extend_schema(
        responses={
            200: QuestionSerializer(many=True)
        }
    )
    def get_questions(self, request, *args, **kwargs):
        page = self.paginate_queryset(self.get_queryset())
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @extend_schema(
        responses={
            200: AnswerResultSerializer
        }
    )
    def submit_answer(self, request, category_id, *args, **kwargs):
        from course.services import check_answer
        serializer = self.get_serializer(data=request.data, context={'request': request, 'category_id': category_id})
        serializer.is_valid(raise_exception=True)
        response = check_answer(self.request.user, **serializer.validated_data)
        return Response(AnswerResultSerializer(response).data)

    def get_result(self, request, *args, **kwargs):
        from course.services import get_result_of_multitest
        achievement = get_result_of_multitest(self.request.user)
        return Response(self.get_serializer(achievement, many=True).data)
