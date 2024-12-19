from datetime import date, datetime

from django import forms
from django.contrib.gis.geos import Point
from django.core.exceptions import ValidationError

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
            'name', 'location', 'latitude', 'longitude', 'short_description', 'city', 'street', 'postal_code',
            'house_number', 'apartment_number', 'description', 'main_image', 'categories', 'one_day_date',
            'start_date', 'end_date', 'website', 'contact_email', 'event_type', 'location_type', 'entry_type',
            'added_by', 'day_of_week', 'main_image', 'gallery_image_1', 'gallery_image_2', 'gallery_image_3',
            'gallery_image_4',
        ]
        widgets = {
            'categories': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-inline'}),
            'one_day_date': forms.DateInput(attrs={'type': 'text', 'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'type': 'text', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'text', 'class': 'form-control'}),
        }

    is_update = False 
    
    def __init__(self, *args, **kwargs):
        self.is_update = kwargs.pop('is_update', False)
        super().__init__(*args, **kwargs)
        self.fields['categories'].queryset = Category.objects.filter(is_active=True).order_by('name')

        # Formatowanie dat dla pól daty
        self._format_date_field('one_day_date', '%Y-%m-%d %H:%M')
        self._format_date_field('start_date', '%Y-%m-%d')
        self._format_date_field('end_date', '%Y-%m-%d')

    def _format_date_field(self, field_name, date_format):
        """Pomocnicza metoda do formatowania wartości pola daty."""
        if field_name in self.initial and self.initial[field_name]:
            self.initial[field_name] = self.initial[field_name].strftime(date_format)
        elif self.instance and getattr(self.instance, field_name, None):
            self.fields[field_name].initial = getattr(self.instance, field_name).strftime(date_format)

    def clean_date_field(self, field_value, date_format):
        """Pomocnicza metoda do walidacji i konwersji pola daty."""
        if isinstance(field_value, str):
            try:
                return datetime.strptime(field_value, date_format)
            except ValueError:
                raise ValidationError(f"Nieprawidłowy format daty. Użyj formatu {date_format}.")
        return field_value

    def clean_one_day_date(self):
        """Walidacja dla pola `one_day_date`."""
        return self.clean_date_field(self.cleaned_data.get('one_day_date'), '%Y-%m-%d %H:%M')

    def clean_start_date(self):
        """Walidacja dla pola `start_date`."""
        return self.clean_date_field(self.cleaned_data.get('start_date'), '%Y-%m-%d')

    def clean_end_date(self):
        """Walidacja dla pola `end_date`."""
        return self.clean_date_field(self.cleaned_data.get('end_date'), '%Y-%m-%d')

    def clean(self):
        cleaned_data = super().clean()
        latitude = cleaned_data.get('latitude')
        longitude = cleaned_data.get('longitude')
        event_type = cleaned_data.get('event_type')
        one_day_date = cleaned_data.get('one_day_date')
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        day_of_week = cleaned_data.get('day_of_week')

        # Ustawianie lokalizacji
        if latitude and longitude:
            cleaned_data['location'] = Point(longitude, latitude)
        else:
            cleaned_data['location'] = None

        today = date.today()

        # Walidacja dla różnych typów wydarzeń
        if event_type == 'one_day':
            cleaned_data['start_date'], cleaned_data['end_date'] = None, None
            if not one_day_date:
                raise ValidationError({"one_day_date": "Data wydarzenia jednodniowego jest wymagana."})
            
            if isinstance(one_day_date, datetime):
                one_day_date = one_day_date.date()
    
            if not self.is_update and one_day_date < today:
                raise ValidationError({"one_day_date": "Data wydarzenia jednodniowego nie może być z przeszłości."})

        elif event_type == 'multi_day':
            cleaned_data['one_day_date'] = None
            if not start_date or not end_date:
                raise ValidationError({
                    "start_date": "Pola 'Data rozpoczęcia' i 'Data zakończenia' są wymagane dla wydarzenia kilkudniowego.",
                    "end_date": "Pola 'Data rozpoczęcia' i 'Data zakończenia' są wymagane dla wydarzenia kilkudniowego.",
                })
            
            if isinstance(start_date, datetime):
                start_date = start_date.date()
            if isinstance(end_date, datetime):
                end_date = end_date.date()
            
            if not self.is_update and start_date < today:
                raise ValidationError({"start_date": "Data rozpoczęcia nie może być z przeszłości."})
            if not self.is_update and end_date < today:
                raise ValidationError({"end_date": "Data zakończenia nie może być z przeszłości."})
            if start_date > end_date:
                raise ValidationError({"end_date": "Data rozpoczęcia nie może być późniejsza niż data zakończenia."})

        elif event_type == 'recurring':
            cleaned_data['one_day_date'], cleaned_data['start_date'], cleaned_data['end_date'] = None, None, None
            if not day_of_week or len(day_of_week) == 0:
                raise ValidationError({"day_of_week": "Wydarzenie cykliczne wymaga zaznaczenia co najmniej jednego dnia tygodnia."})

        return cleaned_data
