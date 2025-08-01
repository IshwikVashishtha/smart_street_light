from django.db import models

class Device(models.Model):
    device_id = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=200)
    total_lights = models.IntegerField()
    estimated_load = models.FloatField()
    status = models.CharField(max_length=10, default="OFF")

    def __str__(self):
        return self.device_id

class DeviceData(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    voltage = models.FloatField()
    current = models.FloatField()
    power = models.FloatField()
    energy = models.FloatField()
    status = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.device.device_id
    

class DeviceCommand(models.Model):
    device = models.OneToOneField(Device, on_delete=models.CASCADE)
    command = models.CharField(max_length=10)  # ON or OFF
    # duration = models.IntegerField(default=0)  # in minutes


    def __str__(self):
        return self.device.device_id

class Schedule(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    on_time = models.TimeField()
    off_time = models.TimeField()
    repeat_daily = models.BooleanField(default=True)

    def __str__(self):
        return self.device.device_id
