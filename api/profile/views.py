from django.utils.decorators import method_decorator
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.profile.serializers import ProfileResponseSerializer, ProfileRequestSerializer
from course.serializers import FinishedCategorySerializer
from utils.handlers import response_code_wrapper


@method_decorator(response_code_wrapper(), name='dispatch')
class ProfileViewSet(viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == "get_profile":
            return ProfileResponseSerializer
        elif self.action == "update_profile":
            return ProfileRequestSerializer
        return

    @extend_schema(
        responses={
            200: ProfileResponseSerializer
        }
    )
    def get_profile(self, request, *args, **kwargs):
        return Response(ProfileResponseSerializer(self.request.user.account).data)

    @extend_schema(
        responses={
            200: ProfileResponseSerializer
        }
    )
    def update_profile(self, request, *args, **kwargs):
        from api.profile.services import update_profile
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        account = update_profile(request.user, serializer.validated_data)
        return Response(ProfileResponseSerializer(account).data)


@method_decorator(response_code_wrapper(), name='dispatch')
class FinishedCoursesViewSet(viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == 'get_finished_courses':
            return FinishedCategorySerializer
        return None

    @extend_schema(
        responses={
            200: FinishedCategorySerializer(many=True)
        }
    )
    def get_finished_courses(self, request, *args, **kwargs):
        from course.services import get_finished_courses
        user_courses = get_finished_courses(request.user)
        return Response(FinishedCategorySerializer(user_courses, many=True).data)
