from rest_framework.decorators import api_view, permission_classes , authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from .alerts import send_email_alert
from django.core.mail import send_mail
from datetime import time

LOW_POWER_THRESHOLD = 10  # this is in watts

@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def report_data(request):
    serializer = DeviceDataSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

        # Alert if load is too low
        if serializer.validated_data['power'] < LOW_POWER_THRESHOLD:
            send_email_alert(f"Low power detected for device {serializer.validated_data['device']}")

        return Response({'message': 'Data received'}, status=200)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def get_command(request):
    device_id = request.GET.get('device_id')
    try:
        device = Device.objects.get(device_id=device_id)
        command_obj = DeviceCommand.objects.get(device=device)
        serializer = DeviceCommandSerializer(command_obj)
        return Response(serializer.data)
    except Device.DoesNotExist:
        return Response({'error': 'Device not found'}, status=404)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_device(request):
    serializer = DeviceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_devices(request):
    devices = Device.objects.all()
    serializer = DeviceSerializer(devices, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def control_device(request):
    device_id = request.data.get('device_id')
    command = request.data.get('command')
    # duration = request.data.get('duration', 0)

    try:
        device = Device.objects.get(device_id=device_id)
        device.status = command
        device.save()

        DeviceCommand.objects.update_or_create(device=device, defaults={
            'command': command,
            # 'duration': duration
        })
        return Response({'message': 'Command updated'})
    except Device.DoesNotExist:
        return Response({'error': 'Device not found'}, status=404)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_schedules(request):
    schedules = Schedule.objects.all()
    serializer = ScheduleSerializer(schedules, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_schedule(request):
    serializer = ScheduleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_schedule(request, schedule_id):
    try:
        schedule = Schedule.objects.get(id=schedule_id)
        schedule.delete()
        return Response({'message': 'Schedule deleted'})
    except Schedule.DoesNotExist:
        return Response({'error': 'Schedule not found'}, status=404)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_device_data(request, device_id):
    try:
        device = Device.objects.get(device_id=device_id)
        # Get the latest device data
        latest_data = DeviceData.objects.filter(device=device).order_by('-timestamp').first()
        
        # Get historical data for charts (last 24 hours)
        from datetime import datetime, timedelta
        yesterday = datetime.now() - timedelta(days=1)
        historical_data = DeviceData.objects.filter(
            device=device,
            timestamp__gte=yesterday
        ).order_by('timestamp')
        
        # Get recent activity (last 10 commands)
        recent_commands = DeviceCommand.objects.filter(device=device).order_by('-id')[:10]
        
        response_data = {
            'device': {
                'id': device.id,
                'device_id': device.device_id,
                'location': device.location,
                'total_lights': device.total_lights,
                'estimated_load': device.estimated_load,
                'status': device.status,
            },
            'latest_data': {
                'voltage': latest_data.voltage if latest_data else 0,
                'current': latest_data.current if latest_data else 0,
                'power': latest_data.power if latest_data else 0,
                'energy': latest_data.energy if latest_data else 0,
                'status': latest_data.status if latest_data else 'OFF',
                'timestamp': latest_data.timestamp if latest_data else None,
            },
            'historical_data': [
                {
                    'time': data.timestamp.strftime('%H:%M'),
                    'power': data.power,
                    'voltage': data.voltage,
                    'current': data.current,
                    'energy': data.energy,
                }
                for data in historical_data
            ],
            'recent_activity': [
                {
                    'action': f"Device turned {cmd.command}",
                    'timestamp': cmd.id,  # Using ID as timestamp for now
                }
                for cmd in recent_commands
            ]
        }
        
        return Response(response_data)
    except Device.DoesNotExist:
        return Response({'error': 'Device not found'}, status=404)

