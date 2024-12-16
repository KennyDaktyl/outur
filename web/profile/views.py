from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404

from web.events.forms import MessageForm
from web.models.events import Event, EventMessage, EventParticipant


@method_decorator(login_required, name='dispatch')
class UserEventsCreated(ListView):
    model = Event
    template_name = 'profile/user_events.html'
    context_object_name = 'events'
    paginate_by = 20
    

    def get_queryset(self):
        return Event.objects.filter(created_by=self.request.user.id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Moje wydarzenia'
        context['form'] = MessageForm()
        return context


@method_decorator(login_required, name='dispatch')
class UserEventsJoined(ListView):
    model = Event
    template_name = 'profile/user_events_joined.html'
    context_object_name = 'events'
    paginate_by = 20

    def get_queryset(self):
        return Event.objects.filter(participants__user=self.request.user).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Wydarzenia, na które się zapisałem'
        return context


@method_decorator(login_required, name='dispatch')
class UserEventMessagesView(ListView):
    model = EventMessage
    template_name = 'profile/user_event_messages.html'
    context_object_name = 'messages'
    paginate_by = 20

    def get_queryset(self):
        user_events = EventParticipant.objects.filter(user=self.request.user).values_list('event', flat=True)

        return EventMessage.objects.filter(event__in=user_events).select_related('event', 'user').order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Wiadomości z moich wydarzeń'
        return context
    
    
class MessageFormView(LoginRequiredMixin, FormView):
    form_class = MessageForm
    success_url = reverse_lazy("profile:user_events") 

    def form_valid(self, form):
        event_id = form.cleaned_data['event']
        message_content = form.cleaned_data['message']

        event = get_object_or_404(Event, id=event_id)

        EventMessage.objects.create(
            event=event,
            user=self.request.user, 
            message=message_content
        )

        messages.success(self.request, "Wiadomość została wysłana!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Wysłanie wiadomości nie powiodło się. Popraw błędy.")
        return super().form_invalid(form)
    