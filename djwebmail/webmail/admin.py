from django.contrib import admin

from .models import IMAPHost


class IMAPHostAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'address',
        'port',
        'ssl',
        'public'
    )


admin.site.register(IMAPHost, IMAPHostAdmin)
