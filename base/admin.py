from django.contrib import admin
from base import models

from import_export.admin import ImportExportModelAdmin


admin.site.site_header = "LEO PADEL ACADEMY Admin"
admin.site.site_title = "LEO PADEL ACADEMY"
admin.site.index_title = "Manage academy events, camps and bookings"


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
    list_display = [
        "name",
        "type",
        "cost",
        "max_tickets",
        "sold_tickets",
        "available_tickets",
        "has_image",
        "coach_count",
    ]
    list_filter = ["type"]
    search_fields = ["name", "description"]
    fields = [
        "type",
        "name",
        "description",
        "cost",
        "max_tickets",
        "image",
        "available_coaches",
    ]
    filter_horizontal = ["available_coaches"]

    @admin.display(boolean=True, description="Image")
    def has_image(self, obj):
        return bool(obj.image)

    @admin.display(description="Coaches")
    def coach_count(self, obj):
        return obj.available_coaches.count()

    @admin.display(description="Reserved/Paid")
    def sold_tickets(self, obj):
        return obj.sold_tickets_count

    @admin.display(description="Available")
    def available_tickets(self, obj):
        if obj.available_tickets_count is None:
            return "Unlimited"
        return obj.available_tickets_count


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
    list_display = ["buyer", "guest_email", "total", "status", "date"]

    @admin.display(description="Buyer")
    def buyer(self, obj):
        return obj.buyer_name


admin.site.register(models.Service, ServiceAdmin)
admin.site.register(models.Session, SessionAdmin)
admin.site.register(models.Billing, BillingAdmin)
