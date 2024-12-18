import folium

from django.views.generic import TemplateView, ListView
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.template.loader import render_to_string
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.urls import reverse
from django.db.models import Q, Count

from bs4 import BeautifulSoup

from web.events.forms import AbuseReportForm, EventFilterForm
from web.models.events import Event


class EventsView(ListView):
    template_name = 'events/events_listing_list.html'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Event.objects.all().annotate(
            participants_count=Count('participants')
        )
        search_query = self.request.GET.get('search', '').strip()
        sort_option = self.request.GET.get('sort', 'newest')

        if search_query:
            queryset = queryset.filter(Q(name__icontains=search_query))

        if sort_option == 'newest':
            queryset = queryset.order_by('-created_at', 'name') 
        elif sort_option == 'popularity':
            queryset = queryset.order_by('-popularity', '-created_at')
        elif sort_option == 'participants':
            queryset = queryset.order_by('-participants_count', '-created_at')
        elif sort_option == 'nearest':
            pass

        return queryset

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

        session_data = self.request.session.get("event_filters", {})
        
        context['filter_form'] = EventFilterForm(self.request.GET or None, session_data=session_data)
        context['form_action'] = reverse('events:events_list')
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
        
        event = self.object
        user = self.request.user
        if user.is_authenticated:
            event.is_liked = event.likes.filter(user=user).exists()
        else:
            event.is_liked = False
        context['event'] = event
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

        context['event'] = event
        
        map_html = folium_map._repr_html_()
        context['map_html'] = map_html.replace(
        'style="position:relative;width:100%;height:0;padding-bottom:60%;"',
        'style="position:relative;" id="map-container"'
        )
        
        return context


class EventsMapView(TemplateView):
    template_name = "events/events_listing_map.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        session_data = self.request.session.get("event_filters", {})
        context['filter_form'] = EventFilterForm(self.request.GET or None, session_data=session_data)
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
        'style="position:relative;" id="map-container"'
        )
        return context