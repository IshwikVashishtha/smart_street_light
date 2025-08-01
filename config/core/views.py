from rest_framework.decorators import api_view, permission_classes , authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from .alerts import send_email_alert
from django.core.mail import send_mail

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
    



