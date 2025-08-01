from django.urls import path
from . import views

urlpatterns = [
    path('api/report_data', views.report_data),
    path('api/get_command', views.get_command),
    path('api/register_device', views.register_device),
    path('api/list_devices', views.list_devices),
    path('api/control_device', views.control_device),
    path('api/device_data/<str:device_id>', views.get_device_data),
    path('api/list_schedules', views.list_schedules),
    path('api/create_schedule', views.create_schedule),
    path('api/delete_schedule/<int:schedule_id>', views.delete_schedule),
    #  path('api/test_email/', views.test_email),
]
