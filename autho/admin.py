from django.contrib import admin

from autho.models import User, Account, TokenLog


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone', 'is_admin')
    search_fields = ('email', 'phone', 'first_name', 'last_name', 'middle_name')


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('user',)
    autocomplete_fields = ('user', )


@admin.register(TokenLog)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'deleted')
    autocomplete_fields = ('user', )
