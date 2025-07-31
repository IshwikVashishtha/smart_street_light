from django.contrib import admin
from .models import Device, DeviceData, DeviceCommand, Schedule

# Register your models here.

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('device_id', 'location', 'total_lights', 'estimated_load', 'status')
    search_fields = ('device_id', 'location')
    list_filter = ('status',)

@admin.register(DeviceData)
class DeviceDataAdmin(admin.ModelAdmin):
    list_display = ('device', 'voltage', 'current', 'power', 'energy', 'status', 'timestamp')
    list_filter = ('status', 'timestamp')
    date_hierarchy = 'timestamp'

@admin.register(DeviceCommand)
class DeviceCommandAdmin(admin.ModelAdmin):
    list_display = ('device', 'command', 'duration')

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('device', 'on_time', 'off_time', 'repeat_daily')
