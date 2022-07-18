
from django.contrib import admin

from account.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):

    list_display = [
        'user',
        "email",
        "password",
    ]


admin.site.register(UserProfile, UserProfileAdmin)
