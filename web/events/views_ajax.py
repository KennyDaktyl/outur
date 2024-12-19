import folium

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string
from web.events.filters import filter_events, sorted_events_ajax
from web.models.events import Event, EventLike, EventParticipant


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


@login_required
@csrf_exempt
def add_like_event(request, event_id):
    if request.method == 'POST':
        event = Event.objects.filter(id=event_id).first()
        if not event:
            return JsonResponse({'success': False, 'message': 'Wydarzenie nie istnieje'})

        user = request.user
        like, created = EventLike.objects.get_or_create(event=event, user=user)

        if not created:
            like.delete()
            is_liked = False
        else:
            is_liked = True

        likes_count = EventLike.objects.filter(event=event).count()

        return JsonResponse({'success': True, 'likes_count': likes_count, 'is_liked': is_liked})

    return JsonResponse({'success': False, 'message': 'Nieprawidłowe żądanie'})


def ajax_filter_events(request):
    if request.method == "GET":
        events, _ = filter_events(request)
        events = sorted_events_ajax(events, request)
    
        page = request.GET.get("page", 1)

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
        events, _ = filter_events(request)
        events = sorted_events_ajax(events, request)

        map_center = [52.0, 19.0] 
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

        map_html = folium_map._repr_html_()
        map_html = map_html.replace(
        'style="position:relative;width:100%;height:0;padding-bottom:60%;"',
        'style="position:relative;" id="map-container"'
        )
        return JsonResponse({"map_html": map_html})

    return JsonResponse({"error": "Invalid request"}, status=400)
