from django.views.generic import TemplateView, DeleteView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from web.events.forms import EventFilterForm
from web.models.events import Event



class HomeView(TemplateView):
    template_name = 'home/home.html'
    paginate_by = 20
    
    def get_queryset(self):
        return Event.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        events = self.get_queryset()

        page = self.request.GET.get('page', 1) 
        paginator = Paginator(events, self.paginate_by)
        
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        context['filter_form'] = EventFilterForm(self.request.GET or None)
        context['search_form_on'] = True
        context['events'] = page_obj.object_list  
        context['page_obj'] = page_obj  
        context['paginator'] = paginator  
        return context
    

class EventDetails(DeleteView):
    model = Event
    template_name = 'home/event_details.html'
    context_object_name = 'event'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Szczegóły wydarzenia'
        return context