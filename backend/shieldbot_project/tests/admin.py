from django.contrib import admin
from .models import Test, RequestLog, AppLog

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    """Admin configuration for Test model"""
    list_display = ('id', 'user', 'test_type', 'test_name', 'status', 'start_time', 'end_time')
    list_filter = ('status', 'test_type', 'start_time')
    search_fields = ('test_name', 'base_url', 'user__username')
    date_hierarchy = 'start_time'
    readonly_fields = ('start_time', 'last_updated')

@admin.register(RequestLog)
class RequestLogAdmin(admin.ModelAdmin):
    """Admin configuration for RequestLog model"""
    list_display = ('id', 'user', 'test_type', 'status', 'execution_time', 'timestamp')
    list_filter = ('status', 'test_type', 'timestamp')
    search_fields = ('base_url', 'user__username')
    date_hierarchy = 'timestamp'
    readonly_fields = ('timestamp', 'last_updated')

@admin.register(AppLog)
class AppLogAdmin(admin.ModelAdmin):
    """Admin configuration for AppLog model"""
    list_display = ('id', 'log_message', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('log_message',)
    date_hierarchy = 'timestamp'
    readonly_fields = ('timestamp',) 