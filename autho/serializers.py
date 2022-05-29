from rest_framework import serializers
from autho.models import User


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'middle_name', 'email', 'phone', 'password')

    def validate(self, attrs):
        if User.objects.filter(phone=attrs['phone']).exists():
            raise serializers.ValidationError('Пользователь с таким телефоном уже существует')
        if User.objects.filter(phone=attrs['email']).exists():
            raise serializers.ValidationError('Пользователь с такой почтой уже существует')
        return attrs


class SignInSerializer(serializers.Serializer):
    email = serializers.CharField(
        required=True,
        max_length=50
    )
    password = serializers.CharField(
        required=True,
        min_length=8,
        max_length=128
    )
    anonymous_token = serializers.CharField(
        required=False,
        max_length=500
    )

    def validate(self, attrs):
        user = User.objects.filter(email=attrs['email']).first()
        anonymous_token = attrs.get('anonymous_token', None)
        if not user:
            raise serializers.ValidationError('User not found')
        attrs['anonymous_token'] = anonymous_token
        return attrs


class UserResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'middle_name', 'phone', 'email', 'region')


class UserSerializer(serializers.Serializer):
    user = UserResponseSerializer()
    token = serializers.CharField()
