from django.utils import timezone

def compare(value, comparator, threshold):
    if value is None:
        return False
    if comparator == 'lt':
        return value < threshold
    if comparator == 'le':
        return value <= threshold
    if comparator == 'gt':
        return value > threshold
    if comparator == 'ge':
        return value >= threshold
    if comparator == 'eq':
        return value == threshold
    if comparator == 'ne':
        return value != threshold
    return False

def apply_action(device, action):
    
    if action == 'on':
        device.status = True
    elif action == 'off':
        device.status = False
    elif action == 'toggle':
        device.status = not device.status
    device.save(update_fields=['status', 'last_updated'])

def evaluate_rule(rule):
    """
    Zwraca wartość True, jeśli reguła została uruchomiona (wykonano działanie), w przeciwnym razie False.    
    """
    sensor = rule.sensor
    ok = compare(sensor.value, rule.comparator, rule.threshold)
    if ok:
        apply_action(rule.target, rule.action)
        rule.last_triggered = timezone.now()
        rule.save(update_fields=['last_triggered'])
        return True
    return False

def evaluate_all(rules_queryset):
    """
    Ocenia wszystkie aktywowane reguły. Zwraca (wyzwolone, łącznie).
    """
    triggered = 0
    total = 0
    for r in rules_queryset:
        total += 1
        if evaluate_rule(r):
            triggered += 1
    return triggered, total
