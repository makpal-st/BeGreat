from rest_framework import serializers

from support.models import Conversation, ConversationAnswer


class ConversationCreateSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, max_length=100)
    text = serializers.CharField(required=True, max_length=1000)


class ConversationAnswerResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = ConversationAnswer
        fields = ('text',)


class ConversationResponseSerializer(serializers.ModelSerializer):
    answers = ConversationAnswerResponseSerializer(many=True)

    class Meta:
        model = Conversation
        fields = ('id', 'title', 'text', 'answers')
