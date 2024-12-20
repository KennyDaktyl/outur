from django.urls import path

from web.events.views import EventDetails, EventMapView, EventsMapView, EventsView
from .views_ajax import add_user_to_event, ajax_filter_events, ajax_filter_events_map, add_like_event

app_name = "events"


urlpatterns = [
   path('add-user-to-event/<int:event_id>/', add_user_to_event, name='add_user_to_event'),
   path('add-like-event/<int:event_id>/', add_like_event, name='add_like_event'),
   path('ajax/filter-events/', ajax_filter_events, name='ajax_filter_events'),
   path('ajax/filter-events-map/', ajax_filter_events_map, name='ajax_filter_events_map'),
   
   path('<slug:slug>/<int:pk>/', EventDetails.as_view(), name='event_details'),
   path('mapa/<int:pk>/', EventMapView.as_view(), name='event_map'),
   path('mapa/', EventsMapView.as_view(), name='events_map'),
   path('lista/', EventsView.as_view(), name='events_list'),
]
