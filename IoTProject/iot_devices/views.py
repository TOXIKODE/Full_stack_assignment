from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Device, TemperatureReading, HumidityReading
from .serializers import DeviceSerializer, TemperatureReadingSerializer, HumidityReadingSerializer
from django.http import JsonResponse
from datetime import datetime
from django.utils import timezone
import matplotlib.pyplot as plt
import io
import urllib, base64


# from .serializers import ReadingsFilterSerializer



@api_view(['POST'])
def create_device(request):
    serializer = DeviceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_device(request, device_uid):
    try:
        device = Device.objects.get(uid=device_uid)
        device.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Device.DoesNotExist:
        return Response({"error": "Device not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def retrieve_device(request, device_uid):
    try:
        device = Device.objects.get(uid=device_uid)
        serializer = DeviceSerializer(device)
        return Response(serializer.data)
    except Device.DoesNotExist:
        return Response({"error": "Device not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def list_devices(request):
    devices = Device.objects.all()
    serializer = DeviceSerializer(devices, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def home_devices(request):
    
    return render(request, 'home.html') 


@api_view(['GET'])
def temp_devices(request):
    devices = TemperatureReading.objects.all()
    serializer = TemperatureReadingSerializer(devices, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_device_readings(request, device_uid, parameter):
    # Get the query parameters from the request
    start_on = request.query_params.get('start_on')
    end_on = request.query_params.get('end_on')

    # Parse the start_on and end_on strings into datetime objects
    try:
        start_on = datetime.strptime(start_on, "%Y-%m-%dT%H:%M:%S")  
        end_on = datetime.strptime(end_on, "%Y-%m-%dT%H:%M:%S") 
    except ValueError:
        return JsonResponse({"error": "Invalid date format. Use yyyy-mm-ddTHH:MM:SS."}, status=400)

    # Query the readings based on the parameters
    if parameter == 'temperature':
        readings = TemperatureReading.objects.filter(
            device__uid=device_uid,
            start_on__gte=start_on,
            end_on__lte=end_on
        ).order_by('start_on')
    elif parameter == 'humidity':
        readings = HumidityReading.objects.filter(
            device__uid=device_uid,
            start_on__gte=start_on,
            end_on__lte=end_on
        ).order_by('start_on')
    else:
        return JsonResponse({"error": "Invalid parameter. Use 'temperature' or 'humidity'."}, status=400)

    readings_data = [{'start_on': start_on, 'end_on': end_on, parameter: getattr(reading, parameter)} for reading in readings]
    return JsonResponse(readings_data, safe=False)


def device_graph(request):
    device_uid = request.GET.get('device_uid', None)

    if device_uid:
        # Fetch temperature and humidity data for the device
        temperature_data = TemperatureReading.objects.filter(device__uid=device_uid)
        humidity_data = HumidityReading.objects.filter(device__uid=device_uid)

        # Extract timestamps and corresponding values
        temperature_timestamps = [reading.start_on for reading in temperature_data]
        temperature_values = [reading.temperature for reading in temperature_data]
        humidity_timestamps = [reading.start_on for reading in humidity_data]
        humidity_values = [reading.humidity for reading in humidity_data]

        # Create a plot
        plt.style.use('Solarize_Light2')
        plt.figure(figsize=(10, 6))
         
        plt.plot(temperature_timestamps, temperature_values, label='Temperature (°C)', color='red')
        plt.plot(humidity_timestamps, humidity_values, label='Humidity (%)', color='blue')
        plt.xlabel('Time')
        plt.ylabel('degree')
        plt.title('Temperature and Humidity vs. Time')
        plt.legend()

        # Save the plot to a byte buffer
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plt.close()

        # Convert the byte buffer to a base64-encoded string
        plot_data = base64.b64encode(buffer.read()).decode('utf-8')

        # Pass the base64-encoded plot to the template
        context = {
            'device_uid': device_uid,
            'plot_data': plot_data,
        }

        return render(request, 'device_graph.html', context)

    return render(request, 'error.html', {'error_message': 'Device UID not provided'})

    
