from django.conf.urls import url
from django.urls import path, include

urlpatterns = [
    path('profile/', include("api.profile.urls")),
]

