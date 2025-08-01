from django.urls import path
from . import views

urlpatterns = [
    path('api/report_data', views.report_data),
    path('api/get_command', views.get_command),
    path('api/register_device', views.register_device),
    path('api/list_devices', views.list_devices),
    path('api/control_device', views.control_device),
     path('api/test_email/', views.test_email),
]
