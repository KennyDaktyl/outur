import folium

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.utils.safestring import mark_safe
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string
from web.models.events import Event, EventParticipant
from .forms import EventFilterForm


@login_required
@csrf_exempt
def add_user_to_event(request, event_id):
    if request.method == "POST":
        try:
            event = Event.objects.get(id=event_id)
            participant, created = EventParticipant.objects.get_or_create(event=event, user=request.user)
            if created:
                return JsonResponse({"status": "success", "message": "User added", "users_count": event.users_count})
            else:
                return JsonResponse({"status": "info", "message": "User already added", "users_count": event.users_count})
        except Event.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Event not found"}, status=404)
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)


def ajax_filter_events(request):
    if request.method == "GET":
        filter_form = EventFilterForm(request.GET)
        page = request.GET.get("page", 1)
        
        if filter_form.is_valid():
            events = Event.objects.all()
            if filter_form.cleaned_data.get('categories'):
                events = events.filter(categories__in=filter_form.cleaned_data['categories']).distinct()
            if filter_form.cleaned_data.get('location_type'):
                events = events.filter(location_type=filter_form.cleaned_data['location_type'])
            if filter_form.cleaned_data.get('entry_type'):
                events = events.filter(entry_type=filter_form.cleaned_data['entry_type'])
            if filter_form.cleaned_data.get('added_by'):
                events = events.filter(added_by=filter_form.cleaned_data['added_by'])
        else:
            events = Event.objects.all()

        paginator = Paginator(events, 20) 
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)


        events_html = render_to_string(
            "events/includes/event_listing.html", {"events": page_obj.object_list, "user": request.user}
        )

        pagination_html = render_to_string(
            "utils/pagination.html", {"paginator": paginator, "page_obj": page_obj}
        )
        return JsonResponse({"html": events_html, "pagination": pagination_html})
    return JsonResponse({"error": "Invalid request"}, status=400)


def ajax_filter_events_map(request):
    if request.method == "GET":
        filter_form = EventFilterForm(request.GET)
        if filter_form.is_valid():
            events = Event.objects.all()
            if filter_form.cleaned_data.get('categories'):
                events = events.filter(categories__in=filter_form.cleaned_data['categories']).distinct()
            if filter_form.cleaned_data.get('location_type'):
                events = events.filter(location_type=filter_form.cleaned_data['location_type'])
            if filter_form.cleaned_data.get('entry_type'):
                events = events.filter(entry_type=filter_form.cleaned_data['entry_type'])
            if filter_form.cleaned_data.get('added_by'):
                events = events.filter(added_by=filter_form.cleaned_data['added_by'])
        else:
            events = Event.objects.all()

        # Tworzenie mapy z filtrowanymi wydarzeniami
        map_center = [52.0, 19.0]  # Współrzędne centralne dla mapy
        folium_map = folium.Map(location=map_center, zoom_start=6)

        for event in events:
            if event.location:
                latitude = event.location.y
                longitude = event.location.x
                popup_content = render_to_string("events/includes/popup_content.html", {"event": event})
                folium.Marker(
                    location=[latitude, longitude],
                    popup=folium.Popup(popup_content, max_width=300),
                    tooltip=event.name,
                    icon=folium.Icon(color="blue", icon="info-sign")
                ).add_to(folium_map)

        # Render mapy HTML
        map_html = folium_map._repr_html_()

        return JsonResponse({
            "map_html": map_html,  # Nowa mapa
        })
    return JsonResponse({"error": "Invalid request"}, status=400)
