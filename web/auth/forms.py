from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    
    
class RegistrationForm(forms.Form):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
