from django.contrib import admin

from client import models


class ClientAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'email', 'mobile', 'gender']


class NotificationAdmin(admin.ModelAdmin):
    list_display = ['client', 'session', 'type', 'seen', 'date']


admin.site.register(models.Client, ClientAdmin)
admin.site.register(models.Notification, NotificationAdmin)
