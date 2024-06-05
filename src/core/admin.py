from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

BaseUserAdmin.fieldsets += ('Followed Partners', {'fields': ('followed_partners',)}),
admin.site.unregister(User)
admin.site.register(User, BaseUserAdmin)
