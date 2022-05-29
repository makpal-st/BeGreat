from django.contrib import admin
from django.urls import path, include

from autho.views import AuthViewSet

urlpatterns = [
    path(
        "sign_up/", AuthViewSet.as_view(
            {'post': 'sign_up'}
        ),
        name='authorization'
    ),
    path(
        "sign_in/", AuthViewSet.as_view(
            {'post': 'sign_in'}
        ),
        name='authorization'
    ),
    path(
        "sign_out/", AuthViewSet.as_view(
            {'post': 'sign_out'}
        ),
        name='authorization'
    )
]
