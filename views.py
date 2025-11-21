from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse  # potrzebne do generowania pliku CSV
import csv  # wbudowany modul Pythona do obslugi CSV
from .models import Device, EventLog
from .forms import DeviceForm, SensorValueForm
from rules.engine import evaluate_for_sensor  # piekna funkcja automatyzacji po zmianie czujnika
from devices.models import SensorData  # jesli nie masz, dodaj import



def device_list(request):
    """Widok wyswietlajacy liste wszystkich urzadzen."""
    urzadzenia = Device.objects.all()
    kontekst = {
        'devices': urzadzenia
    }
    return render(request, 'devices/devices.html', kontekst)


def toggle_device(request, device_id):
    """
    Widok przelaczajacy stan urzadzenia (ON/OFF).
    - Nie pozwalamy przelaczac CZUJNIKOW (type='sensor'),
      poniewaz czujnik jest urzadzeniem pasywnym, tylko mierzy wartosc.
    - Dla lamp / gniazdek zmieniamy pole `status` i zapisujemy log.
    """
    urzadzenie = get_object_or_404(Device, id=device_id)

    # Blokada: jesli to czujnik -> nic nie robimy, wracamy na liste
    if urzadzenie.type == 'sensor':
        return redirect('device_list')

    # Zmiana stanu dla urzadzen sterowalnych (light, plug, itp.)
    urzadzenie.status = not urzadzenie.status
    urzadzenie.save()

    # Zapisujemy w logach, że zmiana była ręczna
    EventLog.objects.create(
        device=urzadzenie,
        action='manual',  # dostosuj do swoich CHOICES
        description="Stan urządzenia został zmieniony ręcznie z listy urządzeń.",
    )

    return redirect('device_list')


def event_log_list(request):
    """
    Prosty widok wyswietlajacy liste logow zdarzen.
    """
    logi = EventLog.objects.select_related('device').all()[:100]  # ograniczamy do ostatnich 100
    kontekst = {
        'logs': logi,
    }
    return render(request, 'devices/logs.html', kontekst)

def export_event_logs_csv(request):
    """
    Widok eksportujacy logi zdarzen do pliku CSV.
    """

    # tworzymy obiekt HttpResponse z odpowiednim typem MIME dla CSV
    odpowiedz = HttpResponse(content_type='text/csv; charset=utf-8')

    # ustawiamy naglowek Content-Disposition, zeby przegladarka pobrala plik
    odpowiedz['Content-Disposition'] = 'attachment; filename="smartkey_event_logs.csv"'
    
    # zeby Excel poprawnie rozpoznal kodowanie
    odpowiedz.write('\ufeff')

    # tworzymy writer CSV, ktory bedzie pisal do naszej odpowiedzi HTTP
    writer = csv.writer(odpowiedz, delimiter=';')

    # pierwsza linia - naglowki kolumn (u gory pliku)
    writer.writerow(['czas', 'urzadzenie', 'pokoj', 'akcja', 'opis'])

    # pobieramy wszystkie logi (mozesz ograniczyc, np. [:1000])
    logi = EventLog.objects.select_related('device').all()

    # dla kazdego logu zapisujemy wiersz w CSV
    for log in logi:
        writer.writerow([
            log.created_at.strftime('%Y-%m-%d %H:%M:%S'),  # czas w formacie tekstowym
            log.device.name,
            log.device.room,
            log.get_action_display(),  # czytelna nazwa akcji
            log.description,
        ])

# zwracamy odpowiedz - przegladarka pobierze plik CSV
    return odpowiedz


def device_create(request):
    """
    Widok do tworzenia nowego urzadzenia bez uzycia panelu admina.
    Pozwala dodac lampe, czujnik lub gniazdko w programie.

    URL: /devices/add/
    Szablon: devices/device_form.html
    """
    if request.method == 'POST':
        form = DeviceForm(request.POST)
        if form.is_valid():
            urzadzenie = form.save()
            # Jesli od razu ustawiamy wartosc dla czujnika,
            # mozna od razu utworzyc wpis SensorData.
            if urzadzenie.type == 'sensor' and urzadzenie.value is not None:
                SensorData.objects.create(
                    device=urzadzenie,
                    value=urzadzenie.value,
                )
                # I od razu sprawdzamy reguly dla tego czujnika
                evaluate_for_sensor(urzadzenie)

            return redirect('device_list')
    else:
        form = DeviceForm()

    return render(request, 'devices/device_form.html', {'form': form, 'title': 'Dodaj urządzenie'})


def device_update(request, device_id):
    """
    Widok do edycji urządzenia.

    Uzywamy go glownie do:
      - zmiany temperatury czujnika,
      - pokazania, ze automatyzacja dziala bez przycisku.
    """
    urzadzenie = get_object_or_404(Device, id=device_id)

    # Jesli to czujnik -> uzywamy formularza SensorValueForm (tylko pole value)
    if urzadzenie.type == 'sensor':
        FormClass = SensorValueForm
    else:
        # Dla innych urzadzen – pelny formularz
        FormClass = DeviceForm

    if request.method == 'POST':
        form = FormClass(request.POST, instance=urzadzenie)
        if form.is_valid():
            urzadzenie = form.save()

            # Jesli edytowalismy czujnik, to:
            if urzadzenie.type == 'sensor' and urzadzenie.value is not None:
                # 1) zapisujemy nowy punkt danych dla wykresu Plotly
                SensorData.objects.create(
                    device=urzadzenie,
                    value=urzadzenie.value,
                )
                # 2) uruchamiamy automatycznie reguly, ktore uzywaja tego czujnika
                evaluate_for_sensor(urzadzenie)

            return redirect('device_list')
    else:
        form = FormClass(instance=urzadzenie)

    return render(request, 'devices/device_form.html', {'form': form, 'title': f'Edytuj: {urzadzenie.name}'})


def device_delete(request, device_id):
    """
    Widok do usuwania urzadzenia i jego danych.
    Uzywamy metody POST, aby nie kasowac niczego przez przypadek przy wejsciu na URL.
    """
    urzadzenie = get_object_or_404(Device, id=device_id)

    if request.method == 'POST':
        urzadzenie.delete()
        return redirect('device_list')

    # Jesli ktos wejdzie GETem, wracamy na liste
    return redirect('device_list')