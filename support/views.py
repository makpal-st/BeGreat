from django.shortcuts import render
from drf_spectacular.utils import extend_schema

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from support.models import Conversation
from support.serializer import ConversationCreateSerializer, ConversationResponseSerializer


class SupportViewSet(viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        user = self.request.user
        return Conversation.objects.filter(user_id=user.id)

    def get_serializer_class(self):
        if self.action == 'create_conversation':
            return ConversationCreateSerializer
        return None

    @extend_schema(
        responses={
            200: ConversationResponseSerializer
        }
    )
    def create_conversation(self, request, *args, **kwargs):
        from support.services import create_conversation
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        create_conversation(request.user, serializer.validated_data)
        conversations = self.get_queryset()
        return Response(ConversationResponseSerializer(conversations, many=True).data)

    @extend_schema(
        responses={
            200: ConversationResponseSerializer
        }
    )
    def get_conversation(self, request, *args, **kwargs):
        conversations = self.get_queryset()
        return Response(ConversationResponseSerializer(conversations, many=True).data)
