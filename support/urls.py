from django.urls import path, include

from support.views import SupportViewSet

urlpatterns = [
    path(
        "ask/",
        SupportViewSet.as_view({
            'post': 'create_conversation',
        }),
        name="create conversation"
    ),
    path(
        "conversations/",
        SupportViewSet.as_view({
            'get': 'get_conversation'
        }),
        name="get conversation"
    )
]
