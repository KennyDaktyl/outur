from django.urls import path
from .views_ajax import add_user_to_event, ajax_filter_events

app_name = "events"


urlpatterns = [
   path('add_user_to_event/<int:event_id>/', add_user_to_event, name='add_user_to_event'),
   path('ajax/filter-events/', ajax_filter_events, name='ajax_filter_events'),
]
