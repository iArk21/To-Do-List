from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin

from .models import Apy

# Register your models here.
class ApyAdmin(admin.ModelAdmin):
    readonly_fields = ("creacion", )

admin.site.register(Apy, ApyAdmin)
admin.site.register(CustomUser, UserAdmin)