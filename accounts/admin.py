from django.contrib import admin
from .models import UserProfile, ForumPost, ForumComment

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile_image')
    search_fields = ('user__username',)
    list_filter = ('user__is_active',)
    ordering = ('user__username',)
    actions = ['deactivate_users']

    def deactivate_users(self, request, queryset):
        for profile in queryset:
            profile.user.is_active = False
            profile.user.save()
        self.message_user(request, "Маркираните потребители са деактивирани.")
    deactivate_users.short_description = "Деактивирай потребители"

@admin.register(ForumPost)
class ForumPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    search_fields = ('title', 'author__username')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

@admin.register(ForumComment)
class ForumCommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at')
    search_fields = ('post__title', 'author__username', 'content')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
