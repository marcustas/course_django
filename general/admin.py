from django.contrib import admin

from general.models import RequestStatistics


@admin.register(RequestStatistics)
class RequestStatistics(admin.ModelAdmin):
    list_display = ('user',)
