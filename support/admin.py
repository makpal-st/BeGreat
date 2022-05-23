from django.contrib import admin

from support.models import Conversation, ConversationAnswer


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_display = ('id', 'title', 'created_at')
    autocomplete_fields = ('user', )


@admin.register(ConversationAnswer)
class ConversationAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'conversation', 'created_at')
    autocomplete_fields = ('conversation', )
