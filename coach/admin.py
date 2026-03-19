from django.contrib import admin

from coach import models

class CoachAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'specialization', 'qualification', 'years_of_experience']

class NotificationAdmin(admin.ModelAdmin):
    list_display = ['coach', 'session', 'type', 'seen', 'date']

admin.site.register(models.Coach, CoachAdmin)
admin.site.register(models.Notification, NotificationAdmin)
