from django import forms

from django.contrib.auth.models import User


class ProfileForm(forms.ModelForm):
    phone_number = forms.CharField(label="Numer telefonu" ,max_length=9, required=False)
    
    class Meta:
        model = User
        fields = ['first_name', 'username', 'email', 'phone_number']
        labels = {
            'first_name': 'Nazwa',
            'username': 'Login',
            'email': 'Adres e-mail',
            'phone_number': 'Numer telefonu',
        }