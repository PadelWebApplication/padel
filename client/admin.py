from django.contrib import admin

from client import models


class ClientAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'email', 'mobile', 'gender']


admin.site.register(models.Client, ClientAdmin)
