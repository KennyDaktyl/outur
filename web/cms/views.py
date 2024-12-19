from django.utils import timezone

from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib import messages

from django.shortcuts import render

from web.models.events import Event
from .forms import EventForm


@method_decorator(login_required, name="dispatch")
class EventCreateView(CreateView):
    model = Event
    form_class = EventForm
    template_name = "cms/forms/event_form.html"
    success_url = reverse_lazy("profile:user_events")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['is_update'] = False
        return kwargs
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, "Wydarzenie zostało dodane.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Popraw pola w formularzu.")
        return render(self.request, self.template_name, {"form": form})
    

@method_decorator(login_required, name="dispatch")
class EventUpdateView(UpdateView):
    model = Event
    form_class = EventForm
    template_name = "cms/forms/event_form.html"
    success_url = reverse_lazy("profile:user_events")
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['is_update'] = True 
        return kwargs
    
    def get_initial(self):
        """Ustawienie początkowych wartości formularza."""
        initial = super().get_initial()
        if self.object and self.object.location:
            initial['latitude'] = f"{self.object.location.y:.8f}"
            initial['longitude'] = f"{self.object.location.x:.8f}" 
        return initial
    
    def form_invalid(self, form):
        messages.error(self.request, "Popraw pola w formularzu.")
        return render(self.request, self.template_name, {"form": form})
    
    def form_valid(self, form):
        form.instance.update_at = timezone.now()
        messages.success(self.request, "Wydarzenie zostało zaktualizowane.")
        return super().form_valid(form)
