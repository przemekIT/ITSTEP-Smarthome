from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Rule
from .engine import evaluate_all

def rules_home(request):
    rules = Rule.objects.select_related('sensor', 'target').all().order_by('-enabled', 'name')
    return render(request, 'rules/rules.html', {'rules': rules})

def run_rules(request):
    if request.method != 'POST':
        return redirect('rules_home')

    qs = Rule.objects.filter(enabled=True).select_related('sensor', 'target')
    triggered, total = evaluate_all(qs)
    if total == 0:
        messages.info(request, "Brak aktywnych reguł do sprawdzenia.")
    else:
        messages.success(request, f"Reguły wykonane: {triggered} uruchomione z {total} aktywnych.")
    return redirect('rules_home')
