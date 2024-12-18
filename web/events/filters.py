from web.events.forms import EventFilterForm
from web.models.events import Event


def filter_events(request):
    """
    Funkcja pomocnicza do filtrowania eventów i zarządzania sesją filtrów.
    """
    # Pobierz dane GET lub wartości z sesji
    session_filters = request.session.get("event_filters", {})
    request_filters = request.GET or session_filters
    
    filter_form = EventFilterForm(request_filters)

    if filter_form.is_valid():
        # Konwersja QuerySet na listę ID dla 'categories'
        cleaned_data = filter_form.cleaned_data.copy()
        if cleaned_data['categories']:
            cleaned_data['categories'] = list(cleaned_data['categories'].values_list('id', flat=True))
        else:
            cleaned_data['categories'] = []
        # Aktualizuj sesję tylko dla prostych danych
        request.session["event_filters"] = cleaned_data

        events = Event.objects.all()
        if cleaned_data.get('categories'):
            events = events.filter(categories__id__in=cleaned_data['categories']).distinct()
        if cleaned_data.get('location_type'):
            events = events.filter(location_type=cleaned_data['location_type'])
        if cleaned_data.get('entry_type'):
            events = events.filter(entry_type=cleaned_data['entry_type'])
        if cleaned_data.get('added_by'):
            events = events.filter(added_by=cleaned_data['added_by'])
    else:
        # Jeśli formularz jest niepoprawny lub GET puste - wyczyść sesję
        request.session.pop("event_filters", None)
        events = Event.objects.all()
    print(request.session["event_filters"])
    return events, filter_form
