from django.urls import path
from .views import HomeView, EventDetails


app_name = "home"


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('event/<int:pk>/', EventDetails.as_view(), name='event_details'),
]
