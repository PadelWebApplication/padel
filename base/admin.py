from django.contrib import admin
from base import models

from import_export.admin import ImportExportModelAdmin

class SessionInline(admin.TabularInline):
    model = models.Session
    extra = 1

class BillingInline(admin.TabularInline):
    model = models.Billing
    extra = 1

class ServiceAdmin(ImportExportModelAdmin):
    list_display = ['name', 'cost']
    search_fields = ['name', 'description']
    filter_horizontal = ['available_coaches']

class SessionAdmin(admin.ModelAdmin):
    list_display = ['client', 'coach', 'session_date', 'status']
    search_fields = ['client__username', 'coach__user__username']
    inlines = [BillingInline]

class BillingAdmin(admin.ModelAdmin):
    list_display = ['client', 'total', 'status', 'date']


admin.site.register(models.Service, ServiceAdmin)
admin.site.register(models.Session, SessionAdmin)
admin.site.register(models.Billing, BillingAdmin)

