import folium

from django.views.generic import TemplateView, ListView
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.template.loader import render_to_string
from django.views.generic import TemplateView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from bs4 import BeautifulSoup

from web.events.forms import AbuseReportForm, EventFilterForm
from web.models.events import Event



class EventsView(ListView):
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
    
    
class EventDetails(DetailView):
    model = Event
    template_name = 'events/event_details.html'
    context_object_name = 'event'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Szczegóły wydarzenia'
        context['form'] = AbuseReportForm()
        return context
    
    
class EventMapView(TemplateView):
    template_name = "events/includes/event_map.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        event_id = self.kwargs.get('pk')
        event = get_object_or_404(Event, id=event_id)

        if not event.location:
            raise Http404("Lokalizacja wydarzenia nie jest dostępna.")

        latitude = event.location.y
        longitude = event.location.x

        folium_map = folium.Map(location=[latitude, longitude], zoom_start=15)
        folium.Marker(
            [latitude, longitude],
            popup=event.name,
            tooltip="Kliknij, aby zobaczyć szczegóły"
        ).add_to(folium_map)

        context['map_html'] = folium_map._repr_html_()
        context['event'] = event
        return context


class EventsMapView(TemplateView):
    template_name = "events/includes/events_listing_map.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = EventFilterForm(self.request.GET or None)
        context['search_form_on'] = True

        events = Event.objects.all()

        map_center = [52.0, 19.0] 
        folium_map = folium.Map(location=map_center, zoom_start=6)

        for event in events:
            if event.location:
                latitude = event.location.y
                longitude = event.location.x

                popup_content = render_to_string("events/includes/popup_content.html", {"event": event})

                folium.Marker(
                    location=[latitude, longitude],
                    popup=folium.Popup(popup_content, max_width=600),
                    tooltip=event.name,
                    icon=folium.Icon(color="blue", icon="info-sign")
                ).add_to(folium_map)

        map_html = folium_map._repr_html_()
        

        soup = BeautifulSoup(map_html, 'html.parser')
        for span in soup.find_all("span", string=lambda text: "Make this Notebook Trusted" in text if text else False):
            span.decompose()  

        map_html_cleaned = str(soup)
        context['map_html'] = map_html_cleaned.replace(
            'style="position:relative;width:100%;height:0;padding-bottom:60%;"',
            'style="position:relative;width:100%;height: 600px;"'
        )
        return context