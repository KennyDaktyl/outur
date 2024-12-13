from django import forms

from web.constans import ADDED_BY_CHOICES, ENTRY_CHOICES, LOCATION_CHOICES
from web.models.categories import Category


class EventFilterForm(forms.Form):
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