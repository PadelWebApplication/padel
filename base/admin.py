from django.contrib import admin
from base import models

from import_export.admin import ImportExportModelAdmin

class SessionInline(admin.TabularInline):
    model = models.Session
    extra = 1

class SessionNoteInline(admin.TabularInline):
    model = models.SessionNote
    extra = 1

class ActionItemInline(admin.TabularInline):
    model = models.ActionItem
    extra = 1


class ResourceInline(admin.TabularInline):
    model = models.Resource
    extra = 1

class BillingInline(admin.TabularInline):
    model = models.Billing
    extra = 1

class ServiceAdmin(ImportExportModelAdmin):
    list_display = ["name", "cost"]
    search_fields = ["name", "description"]
    filter_horizontal = ["available_coaches"]

class SessionAdmin(admin.ModelAdmin):
    list_display = ["client", "coach", "session_date", "status"]
    search_fields = ["client__username", "coach__user__username"]
    inlines = [BillingInline]

class SessionNoteAdmin(ImportExportModelAdmin):
    list_display = ["session", "summary"]

class ActionItemAdmin(ImportExportModelAdmin):
    list_display = ["session", "task"]

class ResourceAdmin(ImportExportModelAdmin):
    list_display = ["session", "title"]

class BillingAdmin(admin.ModelAdmin):
    list_display = ["client", "total", "status", "date"]


admin.site.register(models.Service, ServiceAdmin)
admin.site.register(models.Session, SessionAdmin)
admin.site.register(models.Billing, BillingAdmin)

