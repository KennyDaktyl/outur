import random

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.views.generic.edit import FormView
from django.http import JsonResponse

from web.auth.forms import LoginForm, RegistrationForm
from web.utils import send_sms


class LoginView(FormView):
    template_name = 'auth/login_form.html'
    form_class = LoginForm

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(self.request, user)
            return JsonResponse({'message': 'Zalogowano pomyślnie.'})
        else:
            return JsonResponse({'message': 'Nieprawidłowe dane logowania.'})

    def form_invalid(self, form):
        return JsonResponse({'errors': form.errors}, status=400)
    
    
class UserRegistrationView(FormView):
    template_name = 'auth/registration_form.html'
    form_class = RegistrationForm

    def form_valid(self, form):
        email = form.cleaned_data['email']
        phone_number = form.cleaned_data['phone_number']
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user = User.objects.create_user(username=username, email=email, password=password)
        user.profile.phone_number = phone_number 
        user.save()

        verification_code = random.randint(1000, 9999)

        sms_text = f"Twój kod weryfikacyjny to: {verification_code}"
        send_sms(phone_number, sms_text)

        self.request.session['verification_code'] = verification_code
        self.request.session['phone_number'] = phone_number

        return JsonResponse({'message': 'Rejestracja udana, kod weryfikacyjny wysłany na SMS.'})

    def form_invalid(self, form):
        return JsonResponse({'errors': form.errors}, status=400)