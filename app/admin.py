from django.contrib import admin
from .models import Profile,Project

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'google_name', 'github_name', 'facebook_name', 'facebook_email', )

    def email(self, obj):
        return obj.user.email  # Show email for manual users in admin panel

    email.admin_order_field = 'user__email'
    email.short_description = 'Email'

    # Custom method to display Facebook profile picture

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'team_members_list', 'created_at', 'updated_at')

    def team_members_list(self, obj):
        return ", ".join([user.username for user in obj.team_members.all()])
    team_members_list.short_description = 'Team Members'

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('team_members')