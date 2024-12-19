from django.db.models import Count, Q
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from django.conf import settings

from web.events.forms import EventFilterForm
from web.models.events import Event


def get_events_base(request):
    queryset = Event.objects.all().annotate(
            participants_count=Count('participants'),
            likes_count=Count('likes'),
        )
    if request.session.get("user_location"):
        user_location = request.session["user_location"]
        queryset = queryset.annotate(
            distance=Distance("location", user_location)
        ).filter(
            location__distance_lte=(user_location, D(km=settings.MAX_DISTANCE))
        )
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
    
    if sort_option == 'newest':
        queryset = queryset.order_by('-created_at', 'name') 
    elif sort_option == 'popularity':
        queryset = queryset.order_by('-likes_count', '-created_at')
    elif sort_option == 'participants':
        queryset = queryset.order_by('-participants_count', '-created_at')
    elif sort_option == 'nearest':
        pass
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
