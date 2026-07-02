from django.contrib import admin

from coach import models


class CoachAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'full_name',
        'specialization',
        'qualification',
        'years_of_experience',
    ]


admin.site.register(models.Coach, CoachAdmin)
