from django.utils import timezone

from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

from django.shortcuts import render

from web.models.events import Event
from .forms import EventForm


@method_decorator(login_required, name="dispatch")
class EventCreateView(CreateView):
    model = Event
    form_class = EventForm
    template_name = "cms/forms/event_create_form.html"
    success_url = reverse_lazy("home:home")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        return render(self.request, self.template_name, {"form": form})
    

@method_decorator(login_required, name="dispatch")
class EventUpdateView(UpdateView):
    model = Event
    form_class = EventForm
    template_name = "cms/forms/event_update_form.html"
    success_url = reverse_lazy("home:home")
    
    def get_initial(self):
        """Ustawienie początkowych wartości formularza."""
        initial = super().get_initial()
        if self.object and self.object.location:
            initial['latitude'] = f"{self.object.location.y:.8f}"
            initial['longitude'] = f"{self.object.location.x:.8f}" 
        return initial
    
    def form_invalid(self, form):
        return render(self.request, self.template_name, {"form": form})
    
    def form_valid(self, form):
        form.instance.update_at = timezone.now()
        return super().form_valid(form)
