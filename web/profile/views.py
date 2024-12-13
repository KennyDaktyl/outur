from web.models.events import Event
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView


@method_decorator(login_required, name='dispatch')
class UserEvents(ListView):
    model = Event
    template_name = 'profile/user_events.html'
    context_object_name = 'events'
    paginate_by = 20
    

    def get_queryset(self):
        return Event.objects.filter(created_by=self.request.user.id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Moje wydarzenia'
        return context