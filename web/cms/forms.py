from django import forms
from django.contrib.gis.geos import Point

from web.constans import ADDED_BY_CHOICES, DAYS_OF_WEEK, ENTRY_CHOICES, EVENT_TYPE_CHOICES, LOCATION_CHOICES
from web.models import Event
from web.models.categories import Category


class EventForm(forms.ModelForm):
    latitude = forms.FloatField(widget=forms.HiddenInput(), required=False)
    longitude = forms.FloatField(widget=forms.HiddenInput(), required=False)
    day_of_week = forms.MultipleChoiceField(
        choices=DAYS_OF_WEEK,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-inline'}),
        required=False,
        label="Dni tygodnia"
    )
    event_type = forms.ChoiceField(
        choices=EVENT_TYPE_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label="Rodzaj wydarzenia",
        
    )
    location_type = forms.ChoiceField(
        choices=LOCATION_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label="Gdzie",
        required=True,
    )
    entry_type = forms.ChoiceField(
        choices=ENTRY_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label="Wstęp",
        required=True,
    )
    added_by = forms.ChoiceField(
        choices=ADDED_BY_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label="Dodane przez",
        required=True,
    )
    
    class Meta:
        model = Event
        fields = [
            'name', 'location', 'latitude', 'longitude', 'short_description', 'city', 'street', 'postal_code', 'house_number', 'apartment_number',
            'description', 'main_image', 'categories',
            'one_day_date', 
            'start_date', 'end_date',  
            'website', 'contact_email', 'event_type', 'location_type', 'entry_type', 'added_by', 'day_of_week', 
        ]
        widgets = {
            'categories': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-inline'}),
            'one_day_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categories'].queryset = Category.objects.filter(is_active=True).order_by('name')

    def clean(self):
        cleaned_data = super().clean()
        latitude = cleaned_data.get('latitude')
        longitude = cleaned_data.get('longitude')

        if latitude and longitude:
            cleaned_data['location'] = Point(longitude, latitude)
        else:
            cleaned_data['location'] = None
        return cleaned_data