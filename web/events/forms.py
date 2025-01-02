from django import forms

from web.constans import ADDED_BY_CHOICES, ENTRY_CHOICES, LOCATION_CHOICES, DATE_CHOICES
from web.models.categories import Category


class EventFilterForm(forms.Form):
    date_filter = forms.ChoiceField(
        choices=DATE_CHOICES,
        widget=forms.Select(attrs={'id': 'date-filter'}),
        label="Kiedy"
    )
    selected_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'id': 'selected-date'}),
        label="Wybierz datę"
    )
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.filter(is_active=True),
        widget=forms.CheckboxSelectMultiple,
        label="Rodzaj",
        required=False
    )
    location_type = forms.ChoiceField(
        choices=LOCATION_CHOICES,
        widget=forms.RadioSelect,
        label="Gdzie",
        required=False
    )
    entry_type = forms.ChoiceField(
        choices=ENTRY_CHOICES,
        widget=forms.RadioSelect,
        label="Wstęp",
        required=False
    )
    added_by = forms.ChoiceField(
        choices=ADDED_BY_CHOICES,
        widget=forms.RadioSelect,
        label="Dodane przez",
        required=False
    )
    
    def __init__(self, *args, **kwargs):
        session_data = kwargs.pop('session_data', {})
        super().__init__(*args, **kwargs)

        for field_name, value in session_data.items():
            if field_name in self.fields:
                self.fields[field_name].initial = value
    

class AbuseReportForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Temat zgłoszenia',
        }),
        label="Temat zgłoszenia", 
    )
    description = forms.CharField(
        max_length=500,
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Podaj treść zgłoszenia',
            'rows': 3,
        }),
        label="Treść zgłoszenia",
    )


class MessageForm(forms.Form):
    event = forms.IntegerField(
        required=True,
        widget=forms.HiddenInput(),
    )
    user = forms.IntegerField(
        required=True,
        widget=forms.HiddenInput(),
    )
    message = forms.CharField(
        max_length=300,
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Wpisz maksymalnie 300 znaków',
            'rows': 3,
        }),
        label="Wiadomość",
    )