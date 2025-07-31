from rest_framework import serializers
from .models import Device, DeviceData, DeviceCommand, Schedule

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'

class DeviceDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceData
        fields = '__all__'

class DeviceCommandSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceCommand
        fields = '__all__'

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'
