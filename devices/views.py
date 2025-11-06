from django.shortcuts import render, redirect, get_object_or_404
from .models import Device

# Affiche tous les appareils.
def device_list(request):
    devices = Device.objects.all()
    return render(request, 'devices/devices.html', {'devices': devices})

# Inverse l’état (ON/OFF) du bon appareil selon son id
def toggle_device(request, device_id):
    device = get_object_or_404(Device, id=device_id)
    device.status = not device.status
    device.save()
    return redirect('device_list')
