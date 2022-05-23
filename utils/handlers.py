import logging
from copy import deepcopy
from functools import wraps

from django.http import Http404
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.status import is_success
from rest_framework.views import exception_handler, set_rollback
from rest_framework.exceptions import PermissionDenied, NotAuthenticated, ValidationError, AuthenticationFailed

from utils import codes


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    error_message = 'SOMETHING_WENT_WRONG'
    print(response, exc, context, type(exc))
    data = dict()
    code = 999
    if isinstance(exc, Http404):
        error_message = 'NOT_FOUND'
        code = 1
    elif isinstance(exc, PermissionDenied):
        error_message = 'PERMISSION_DENIED'
        code = 2
    elif isinstance(exc, NotAuthenticated):
        error_message = 'NOT_AUTHENTICATED'
        code = 3
    elif isinstance(exc, AuthenticationFailed):
        error_message = 'TOKEN_INVALID'
        code = 4
    elif isinstance(exc, ValidationError):
        code = 5
        error_message = 'BAD_REQUEST'
    print(error_message, code)
    if isinstance(exc, exceptions.APIException):
        if isinstance(exc.detail, list):
            error_messages = [error for error in exc.detail]
            error_message = ','.join(error_messages)
        elif isinstance(exc.detail, dict):
            error_messages = []
            for key in exc.detail:
                if isinstance(exc.detail[key], list):
                    if key != 'non_field_errors':
                        error_messages.extend([key + ' : ' + str(err) for err in exc.detail[key]])
                    else:
                        error_messages.extend([str(err) for err in exc.detail[key]])
                elif isinstance(exc.detail[key], str):
                    error_messages.append(key)
                else:
                    error_messages.append(str(exc.detail[key]))
            error_message = '\n'.join(error_messages)
        else:
            if hasattr(exc, 'detail'):
                error_message = exc.detail
        data['message'] = error_message
        data['code'] = code
        set_rollback()
        return Response(data, status=exc.status_code)
    return response


def response_code_wrapper(response_result_key='result'):
    """
    Decorator to make a view only accept request with required http method.
    :param required http method.
    """

    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            response = func(request, *args, **kwargs)
            try:
                if is_success(response.status_code):
                    if hasattr(response, 'data'):
                        # PopUp response
                        if isinstance(response.data, dict) and response.data.get('code', 0) in (
                                codes.POPUP_ERROR, codes.BAD_REQUEST, codes.DIALOG_ERROR):
                            return response

                        # Response result and code status in one level
                        data = deepcopy(response.data)

                        response.data = {
                            response_result_key: data,
                            'code': codes.OK
                        }

            except Exception as exc:
                logging.exception(str(exc))
            return response

        return inner

    return decorator
