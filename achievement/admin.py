from django.contrib import admin

from achievement.models import Achievement, UserAchievement


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'min_points')
    search_fields = ('title', )


@admin.register(UserAchievement)
class UserAchievement(admin.ModelAdmin):
    list_display = ('id', 'user', 'achievement')
    search_fields = ('user', )
    autocomplete_fields = ('user', 'achievement')
