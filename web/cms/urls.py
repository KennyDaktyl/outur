from django.urls import path
from .views import EventCreateView, EventUpdateView

app_name = "cms"


urlpatterns = [
    path('create_event/', EventCreateView.as_view(), name='create_event'),
    path('update_event/<int:pk>/', EventUpdateView.as_view(), name='update_event'),
]
