from support.models import Conversation


def create_conversation(user, kwargs):
    instance = Conversation.objects.create(user=user, **kwargs)
    return instance
