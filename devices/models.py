from django.db import models

class Device(models.Model):
    DEVICE_TYPES = [
        ('light', 'Lumière'),
        ('sensor', 'Capteur'),
        ('plug', 'Prise connectée'),
    ]

    name = models.CharField(max_length=100)
    room = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=DEVICE_TYPES)
    status = models.BooleanField(default=False)
    value = models.FloatField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.room})"
