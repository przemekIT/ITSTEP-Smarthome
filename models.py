from django.db import models
from django.utils import timezone

class Device(models.Model):
    """
    Model reprezentujacy urzadzenie w systemie SmartKey.
    """
    DEVICE_TYPES = [
        ('light', 'Swiatło'),
        ('sensor', 'Czujnik'),
        ('plug', 'Gniazdko'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="Nazwa urządzenia")
    room = models.CharField(max_length=100, verbose_name="Pokój") 
    type = models.CharField(max_length=20, choices=DEVICE_TYPES, verbose_name="Typ urządzenia")
    status = models.BooleanField(default=False, verbose_name="Status") # True = Wlaczone, False = Wylaczone
    value = models.FloatField(null=True, blank=True, verbose_name="Wartość")
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
            verbose_name = "Urządzenie"
            verbose_name_plural = "Urządzenia"

    def __str__(self):
        """Zwraca czytelny opis urzadzenia - przydatne w panelu admina."""
        return f"{self.name} ({self.room})"


class SensorData(models.Model):
    """
    Model przechowujacy dane historyczne z czujnikow.
    """
    # Do ktorego urzadzenia (czujnika) nalezy ten odczyt
    device = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
        related_name='readings',
        verbose_name='Czujnik'
    )
    # Zmierzona wartosc (np. 18.5 °C)
    value = models.FloatField(
        verbose_name='Wartość'
    )
    # Data i godzina pomiaru
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Czas pomiaru'
    )

    class Meta:
        verbose_name = "Dane czujnika"
        verbose_name_plural = "Dane czujników"
        ordering = ['timestamp'] # sortujemy rosnaco po czasie

    def __str__(self):
        """
        Czytelna reprezentacja jednego pomiaru.
        """
        return f"{self.device.name} -> {self.value} {self.timestamp}"
    


class EventLog(models.Model):
    """
    Logi zdarzen zwiazanych z urzadzeniami.
    """
    # typ akcji - kilka podstawowych wartosci
    ACTION_CHOICES = [
        ('manual', 'Reczna'),
        ('auto', 'Automatyczna'),
    ]

    # Urzadzenie, ktore zostalo zmienione
    device = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
        related_name='event_logs',
        verbose_name='Urzadzenie'
    )

    # Typ akcji: manual / auto
    action = models.CharField(
        max_length=20,
        choices=ACTION_CHOICES,
        verbose_name='Akcja'
    )

    # Krotki opis zdarzenia
    description = models.CharField(
        max_length=255,
        verbose_name='Opis zdarzenia'
    )

    # Data i godzina zdarzenia
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='Czas zdarzenia'
    )

    class Meta:
        ordering = ['-created_at']  # najnowsze logi na gorze
        verbose_name = 'Log zdarzenia'
        verbose_name_plural = 'Logi zdarzen'

    def __str__(self):
        return f"{self.device.name} - {self.get_action_display()} - {self.created_at}"
   
