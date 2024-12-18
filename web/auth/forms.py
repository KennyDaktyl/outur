from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    
    
class RegistrationForm(forms.Form):
    username = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=9, required=True)
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean_username(self):
        email = self.cleaned_data.get("username")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Użytkownik z podanym adresem e-mail już istnieje.")
        return email


class ActivationForm(forms.Form):
    verification_code = forms.CharField(
        max_length=4,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Kod weryfikacyjny"}),
        label="Kod weryfikacyjny",
    )