from django.urls import path
from . import views

urlpatterns = [
    
    # url for home
    path('', views.home_devices, name='/api/devices/'),
    
    path('create/api/devices/', views.create_device, name='create/api/devices/'),
    path('delete/devices/<str:device_uid>/', views.delete_device, name='delete-device'),
    path('retrieve/api/devices/<str:device_uid>/', views.retrieve_device, name='retrieve/api/devices/<str:device_uid>/'),
    path('list/api/devices/', views.list_devices, name='list/api/devices/'),
        
    path('api/devices/<str:device_uid>/readings/<str:parameter>/', views.get_device_readings, name='get_device_readings'),
                                         
    path('devices-graph/', views.device_graph, name='device-graph'),
    
   
]