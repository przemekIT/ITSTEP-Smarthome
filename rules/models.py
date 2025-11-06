from django.db import models
from django.utils import timezone
from devices.models import Device

class Rule(models.Model):
    COMPARATORS = [
        ('lt', '<'),
        ('le', '<='),
        ('gt', '>'),
        ('ge', '>='),
        ('eq', '=='),
        ('ne', '!='),
    ]
    ACTIONS = [
        ('on', 'Włącz'),
        ('off', 'Wyłącz'),
        ('toggle', 'Przełącz'),
    ]

    name = models.CharField(max_length=100, verbose_name="Nazwa reguły")
    enabled = models.BooleanField(default=True, verbose_name="Aktywna")

    sensor = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
        related_name='rules_as_sensor',
        verbose_name="Czujnik",
        help_text="Urządzenie typu 'sensor'"
    )

    comparator = models.CharField(max_length=2, choices=COMPARATORS, default='lt', verbose_name="Porównanie")
    threshold = models.FloatField(verbose_name="Próg")

    target = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
        related_name='rules_as_target',
        verbose_name="Urządzenie docelowe"
    )
    action = models.CharField(max_length=6, choices=ACTIONS, default='on', verbose_name="Akcja")

    last_triggered = models.DateTimeField(null=True, blank=True, verbose_name="Ostatnie uruchomienie")

    def __str__(self):
        return f"{self.name} ({self.get_comparator_display()} {self.threshold} -> {self.target.name} {self.get_action_display()})"
