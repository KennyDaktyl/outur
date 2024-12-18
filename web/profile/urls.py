from django.urls import path
from .views import MessageFormView, UserEventMessagesView, UserEventsCreated, UserEventsJoined, ProfileUpdateView

app_name = "profile"


urlpatterns = [
    path('aktualizuj-profil/', ProfileUpdateView.as_view(), name='update_profile'),
    path('moje-wydarzenia/', UserEventsCreated.as_view(), name='user_events'),
    path('moje-wydarzenia-zapisane/', UserEventsJoined.as_view(), name='user_events_joined'),
    path('moje-wiadomosci/', UserEventMessagesView.as_view(), name='user_event_messages'),
    path('wyslij-wiadomosc/<int:event_id>/', MessageFormView.as_view(), name='send_message'),
]
