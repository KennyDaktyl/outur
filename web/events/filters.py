from django.contrib.gis.measure import D
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.conf import settings

from datetime import datetime, timedelta
from django.db.models import Case, When, Value, DateTimeField, F, Count, Q
from web.events.forms import EventFilterForm
from web.models.events import Event


def get_events_base(request):
    today = datetime.now().date()
    queryset = Event.objects.annotate(
        participants_count=Count('participants'),
        likes_count=Count('likes'),
    ).filter(
        is_active=True 
    ).exclude(
        Q(event_type='one_day', one_day_date__lt=today) | 
        Q(event_type='multi_day', end_date__lt=today)  
    )
    if request.session.get("user_location"):
        user_location = request.session["user_location"]
        try:
            latitude, longitude = map(float, user_location.split(','))
        except ValueError:
            raise ValueError("Nieprawidłowy format lokalizacji w sesji. Oczekiwany format: 'lat,lng'.")

        user_location_point = Point(longitude, latitude, srid=4326)
        queryset = queryset.annotate(
            distance=Distance("location", user_location_point) / 1000
        )
        # .filter(
        #     location__distance_lte=(user_location_point, D(km=settings.MAX_DISTANCE))
        # )

    return queryset
    
    
def filter_events_base(cleaned_data, queryset):
    if cleaned_data.get('categories'):
        queryset = queryset.filter(categories__id__in=cleaned_data['categories']).distinct()
    if cleaned_data.get('location_type'):
        queryset = queryset.filter(location_type=cleaned_data['location_type'])
    if cleaned_data.get('entry_type'):
        queryset = queryset.filter(entry_type=cleaned_data['entry_type'])
    if cleaned_data.get('added_by'):
        queryset = queryset.filter(added_by=cleaned_data['added_by'])
    return queryset
    
    
def filter_events(request):
    session_filters = request.session.get("event_filters", {})
    
    if not request.GET:
        request.session["event_filters"] = {}
        session_filters = {}
    
    request_filters = request.GET or session_filters
    filter_form = EventFilterForm(request_filters)

    queryset = get_events_base(request)

    if filter_form.is_valid():
        cleaned_data = filter_form.cleaned_data.copy()
        date_filter = cleaned_data.get('date_filter')
        selected_date = cleaned_data.get('selected_date')

        if date_filter == 'today':
            today = datetime.now().date()
            today_name = today.strftime('%A').lower()

            queryset = queryset.filter(
                Q(event_type='one_day', one_day_date__date=today) |
                Q(event_type='multi_day', start_date__date__lte=today, end_date__date__gte=today) |
                Q(event_type='recurring', day_of_week__icontains=today_name)
            )
        elif date_filter == 'tomorrow':
            tomorrow = (datetime.now() + timedelta(days=1)).date()
            tomorrow_name = tomorrow.strftime('%A').lower()

            queryset = queryset.filter(
                Q(event_type='one_day', one_day_date__date=tomorrow) |
                Q(event_type='multi_day', start_date__date__lte=tomorrow, end_date__date__gte=tomorrow) |
                Q(event_type='recurring', day_of_week__icontains=tomorrow_name)
            )
        elif date_filter == 'select_date' and selected_date:
            selected_day_name = selected_date.strftime('%A').lower()

            queryset = queryset.filter(
                Q(event_type='one_day', one_day_date__date=selected_date) |
                Q(event_type='multi_day', start_date__date__lte=selected_date, end_date__date__gte=selected_date) |
                Q(event_type='recurring', day_of_week__icontains=selected_day_name)
            )

        if selected_date and date_filter == 'select_date':
            cleaned_data['selected_date'] = selected_date.strftime('%Y-%m-%d')
        else:
            cleaned_data['selected_date'] = ''

        if cleaned_data['categories']:
            cleaned_data['categories'] = list(cleaned_data['categories'].values_list('id', flat=True))
        else:
            cleaned_data['categories'] = []

        request.session["event_filters"] = cleaned_data

        queryset = filter_events_base(cleaned_data, queryset)
        queryset = sorted_events_ajax(queryset, request)
    else:
        request.session.pop("event_filters", None)
    
    return queryset, filter_form


def sort_base(sort_option, search_query, queryset):
    if search_query:
        queryset = queryset.filter(Q(name__icontains=search_query))

    today = datetime.now()

    queryset = queryset.annotate(
        nearest_day_as_date=Case(
            *[
                When(
                    day_of_week__icontains=day_name,
                    then=Value(today + timedelta(days=(day_index - today.weekday()) % 7))
                )
                for day_name, day_index in {
                    'monday': 0,
                    'tuesday': 1,
                    'wednesday': 2,
                    'thursday': 3,
                    'friday': 4,
                    'saturday': 5,
                    'sunday': 6,
                }.items()
            ],
            default=None, 
            output_field=DateTimeField()
        )
    ).annotate(
        sort_date=Case(
            When(event_type='recurring', then=F('nearest_day_as_date')),
            When(event_type='one_day', then=F('one_day_date')), 
            When(event_type='multi_day', then=F('start_date')), 
            default=None,
            output_field=DateTimeField()
        )
    )

    if sort_option in ['default', 'newest', '']:
        queryset = queryset.order_by('sort_date', 'name') 

    elif sort_option == 'popularity':
        queryset = queryset.order_by('-likes_count', 'sort_date', 'name') 

    elif sort_option == 'participants':
        queryset = queryset.order_by('-participants_count', 'sort_date', 'name') 
    elif sort_option == 'nearest':
        queryset = queryset.order_by('distance', 'sort_date', 'name')

    return queryset

    
def sorted_events_session(queryset, request):
    search_query = request.GET.get('search', '').strip()
    sort_option = request.GET.get('sort', 'newest')
    
    request.session["sort"] = sort_option
    request.session["search"] = search_query
    
    return sort_base(sort_option, search_query, queryset)

def sorted_events_ajax(queryset, request):
    sort_option = request.session["sort"]
    search_query = request.session["search"]
    
    return sort_base(sort_option, search_query, queryset)


def get_filtered_queryset(request):
    session_filters = request.session.get("event_filters", {})
    request_filters = {**session_filters, **request.GET.dict()}
    
    if "user_location" in request_filters:
        request.session["user_location"] = request_filters["user_location"]
        request_filters.pop("user_location")
    else:
        request.session["user_location"] = None

    filter_form = EventFilterForm(request_filters)

    queryset = get_events_base(request)

    if filter_form.is_valid():
        cleaned_data = filter_form.cleaned_data.copy()

        date_filter = cleaned_data.get('date_filter')
        selected_date = cleaned_data.get('selected_date')

        if date_filter == 'today':
            today = datetime.now().date()
            today_name = today.strftime('%A').lower()

            queryset = queryset.filter(
                Q(event_type='one_day', one_day_date__date=today) |
                Q(event_type='multi_day', start_date__date__lte=today, end_date__date__gte=today) |
                Q(event_type='recurring', day_of_week__icontains=today_name)
            )
        elif date_filter == 'tomorrow':
            tomorrow = (datetime.now() + timedelta(days=1)).date()
            tomorrow_name = tomorrow.strftime('%A').lower()

            queryset = queryset.filter(
                Q(event_type='one_day', one_day_date__date=tomorrow) |
                Q(event_type='multi_day', start_date__date__lte=tomorrow, end_date__date__gte=tomorrow) |
                Q(event_type='recurring', day_of_week__icontains=tomorrow_name)
            )
        elif date_filter == 'select_date' and selected_date:
            selected_day_name = selected_date.strftime('%A').lower()

            queryset = queryset.filter(
                Q(event_type='one_day', one_day_date__date=selected_date) |
                Q(event_type='multi_day', start_date__date__lte=selected_date, end_date__date__gte=selected_date) |
                Q(event_type='recurring', day_of_week__icontains=selected_day_name)
            )

        queryset = filter_events_base(cleaned_data, queryset)

        if 'categories' in cleaned_data and cleaned_data['categories']:
            cleaned_data['categories'] = list(cleaned_data['categories'].values_list('id', flat=True))
        if 'selected_date' in cleaned_data and cleaned_data['selected_date']:
            cleaned_data['selected_date'] = cleaned_data['selected_date'].strftime('%Y-%m-%d')

        if cleaned_data['selected_date']:
            cleaned_data['selected_date'] = selected_date.strftime('%Y-%m-%d')
        if cleaned_data['categories'] and cleaned_data['categories'] != []:
            cleaned_data['categories'] = list(cleaned_data['categories'])
        else:
            cleaned_data['categories'] = []
        request.session["event_filters"] = cleaned_data

    queryset = sorted_events_session(queryset, request)

    if not queryset.query.order_by:
        queryset = queryset.order_by('start_date', 'name')

    return queryset