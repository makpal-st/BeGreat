from django.conf.urls import url
from django.urls import path, include

from api.profile.views import ProfileViewSet, FinishedCoursesViewSet

urlpatterns = [
    path(
        "",
        ProfileViewSet.as_view({'get': 'get_profile', 'put': 'update_profile'}),
        name="profile read-update"
    ),
    path(
        "finished_courses/",
        FinishedCoursesViewSet.as_view({'get': 'get_finished_courses'}),
        name="get finished courses"
    )
]

