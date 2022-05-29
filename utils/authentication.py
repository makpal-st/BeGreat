import time
from django.contrib.auth.hashers import check_password
import pytz
from django.conf import settings
from django.utils import timezone
from drf_spectacular.extensions import OpenApiAuthenticationExtension
from rest_framework import authentication, exceptions
import jwt
from rest_framework.exceptions import ValidationError

from autho.models import TokenLog, User
from course.models import UserCourse
from utils.main import empty_to_none


def create_token(user, request=None):
    """
    Creates token string.
    :param user: User for which token should be created.
    :return: authentication token.
    """
    info = {
        'id': user.id,
        'phone': user.phone,
        'timestamp': int(time.time()),
    }
    token = jwt.encode(info, settings.JWT_KEY, settings.JWT_ALGORITHM)

    if request:
        TokenLog.objects.filter(user=user, deleted=False).update(deleted=True)
    TokenLog.objects.create(user=user, token=token)
    return token


def verify_token(token_string, request):
    """
    Verifies token string.
    :param token_string: Token string to verify.
    :return: Profile/user object if token is valid; None is token is invalid.
    """
    try:
        result = jwt.decode(
            token_string, settings.JWT_KEY, settings.JWT_ALGORITHM)
        user_id = result['id']
        user = User.objects.get(id=user_id)
        # Check if token exists in TokenLog and not deleted
        token_obj = user.tokens.get(token=token_string, deleted=False)
        return user, token_obj
    except:
        return None, None


def extract_token_from_request(request):
    header_names_list = settings.AUTH_TOKEN_HEADER_NAME
    token_string = None
    for name in header_names_list:
        if name in request.META:
            token_string = empty_to_none(request.META[name])
    return empty_to_none(token_string)


class CustomAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        token_string = extract_token_from_request(request)
        if token_string is None:
            return None

        user, token_obj = verify_token(token_string, request)
        if user is None:
            raise exceptions.AuthenticationFailed('Invalid token.')

        return user, token_string


class JWTScheme(OpenApiAuthenticationExtension):
    target_class = "utils.authentication.CustomAuthentication"  # full import path OR class ref
    name = "JWTAuthentication"  # custom name for your auth scheme

    def get_security_definition(self, auto_schema):
        return {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Auth-Token',
            'description': 'Token value'
        }


def authorize(request, email, password, anonymous_token):
    user = User.objects.get(email=email)
    if not check_password(password, user.password):
        raise ValidationError('Пароль неверный!')
    token = create_token(user, request)
    UserCourse.objects.filter(anonymous_user=anonymous_token).update(user=user)
    return user, token


def logout(request):
    token_string = extract_token_from_request(request)
    token_obj = request.user.tokens.get(token=token_string, deleted=False)
    token_obj.deleted = True
    token_obj.save(update_fields=('deleted',))
