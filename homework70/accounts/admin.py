from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from accounts.models import Profile

User = get_user_model()


class ProfileInline(admin.StackedInline):
    model = Profile
    fields = ['birth_date', 'avatar']


class ProfileAdmin(UserAdmin):
    inlines = [ProfileInline]


admin.site.unregister(User)
admin.site.register(User, ProfileAdmin)