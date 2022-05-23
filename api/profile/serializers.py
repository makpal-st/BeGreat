from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from autho.models import Account, User
from autho.serializers import UserResponseSerializer
from course.models import Course
from course.serializers import CourseSerializer


class ProfileResponseSerializer(serializers.ModelSerializer):
    user = UserResponseSerializer()
    interested_courses = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = ('user', 'interested_courses', 'avatar')

    def get_interested_courses(self, obj):
        courses = Course.objects.filter(id__in=obj.interested_courses)
        return CourseSerializer(courses, many=True).data


class ProfileRequestSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    middle_name = serializers.CharField(required=False)
    phone = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    region = serializers.ImageField(required=False)
    avatar = serializers.ImageField(required=False)
    password = serializers.CharField(min_length=8, required=False)

    def validate(self, attrs):
        user = self.context['request'].user
        if not attrs:
            raise ValidationError('Один из полей должен быть не пустым')
        if attrs.get('email', None) and user.email != attrs['email'] and User.objects.filter(email=attrs['email']).exists():
            raise ValidationError('Электронная почта уже занята!')
        if attrs.get('phone', None) and user.phone != attrs['phone'] and User.objects.filter(email=attrs['phone']).exists():
            raise ValidationError('Номер телефона уже занят!')
        return attrs
