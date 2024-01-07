from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile, Meep

admin.site.unregister(Group)

class ProfileInline(admin.StackedInline):
    model = Profile
    fields = ['user', 'profile_image', 'profile_bio', 'homepage_link', 'facebook_link', 'instagram_link', 'linkedin_link']
    can_delete = False

class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ['username', 'email', 'first_name', 'last_name']
    inlines = [ProfileInline]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Meep)
class MeepAdmin(admin.ModelAdmin):
    list_display = ('user', 'body', 'number_of_likes', 'created_at')
    search_fields = ('user__username',)

    def number_of_likes(self, obj):
        return obj.likes.count()

    number_of_likes.short_description = 'Likes'

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile_bio', 'display_follows', 'display_followed_by',  'date_modified',)
    search_fields = ('user__username',)

    def display_follows(self, obj):
        return ", ".join([user.user.username for user in obj.follows.all()])

    def display_followed_by(self, obj):
        return ", ".join([user.user.username for user in obj.followed_by.all()])

    display_follows.short_description = 'Follows'
    display_followed_by.short_description = 'Followed By'