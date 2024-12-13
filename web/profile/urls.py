from django.urls import path
from .views import UserEvents

app_name = "profile"


urlpatterns = [
    path('moje-wydarzenia/', UserEvents.as_view(), name='user_events'),
]
