from django import forms
from .models import Device


class DeviceForm(forms.ModelForm):
    """
    Formularz do tworzenia / edycji urzadzenia.
    Zasady:
    - typ 'sensor':
        * nie uzywa pola 'status'
        * może miec wartosc 'value'
    - typ 'light' lub 'plug':
        * używaja 'status'
        * nie uzywaja 'value' (wartosc liczbowa ignorujemy)
    """

    class Meta:
        model = Device
        fields = ['name', 'room', 'type', 'status', 'value']
        labels = {
            'name': 'Nazwa urządzenia',
            'room': 'Pokój',
            'type': 'Typ urządzenia',
            'status': 'Stan (Włączone/Wyłączone)',
            'value': 'Temperatura',
        }

    def clean(self):
        """
        Dodatkowa walidacja po stronie serwera.
        Nawet jesli ktos wysle "dziwny" formularz np. przez manipulacje w przegladarce,
        to tutaj narzucamy sensowne wartosci zaleznie od typu urzadzenia.
        """
        cleaned_data = super().clean()
        typ = cleaned_data.get('type')
        status = cleaned_data.get('status')
        value = cleaned_data.get('value')

        # Dla czujnika:
        if typ == 'sensor':
            # Czujnik nie ma stanu ON/OFF -> wymuszamy False
            cleaned_data['status'] = False

        # Dla lampy / gniazdka:
        elif typ in ['light', 'plug']:
            # Urzadzenia sterowalne nie maja wartosci liczbowej -> czyscimy
            cleaned_data['value'] = None

        # Mozna dodac inne typy w przyszlosci
        return cleaned_data
    

class SensorValueForm(forms.ModelForm):
    """
    Formularz do edycji wartosci czujnika (np. temperatury)
    w panelu urzadzen. Uzywamy go tylko dla urzadzen typu 'sensor'.
    """

    class Meta:
        model = Device
        fields = ['value']
        labels = {
            'value': 'Temperatura',
        }
