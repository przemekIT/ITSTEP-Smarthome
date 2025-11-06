from django.shortcuts import render
from devices.models import Device

def dashboard(request):
    total_devices = Device.objects.count()
    active_devices = Device.objects.filter(status=True).count()
    inactive_devices = total_devices - active_devices
    sensors = Device.objects.filter(type='sensor')

    context = {
        'total_devices': total_devices,
        'active_devices': active_devices,
        'inactive_devices': inactive_devices,
        'sensors': sensors,
    }
    return render(request, 'dashboard/dashboard.html', context)
