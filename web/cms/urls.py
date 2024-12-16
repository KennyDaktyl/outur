from django.urls import path
from .views import EventCreateView, EventUpdateView

app_name = "cms"


urlpatterns = [
    path('dodaj-wydarzenie/', EventCreateView.as_view(), name='create_event'),
    path('edytuj-wydarzenie/<int:pk>/', EventUpdateView.as_view(), name='update_event'),
]
