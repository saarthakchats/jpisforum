from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from accounts.models import Register
# Register your models here.

class RegisterInline(admin.StackedInline):
    model = Register
    can_delete = False
    verbose_name_plural = 'Registers'

class UserAdmin(BaseUserAdmin):
    inlines = (RegisterInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
