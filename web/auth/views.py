from datetime import timedelta
import random
from django.utils.timezone import now

from uuid import uuid4
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic.edit import FormView

from web.auth.forms import ActivationForm, LoginForm, RegistrationForm
from web.auth.utils import send_activate_email_by_django, send_activate_info_email_by_django
from web.models.accounts import ActivateToken, Profile
from web.utils import send_sms


class LoginView(FormView):
    template_name = 'auth/login_form.html'
    form_class = LoginForm
    success_url = reverse_lazy('events:events_list')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(self.request, user)
            messages.success(
                self.request,
                "Zalogowano użytkownika",
            )
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        messages.error(self.request, "Niepoprawny login lub hasło.")
        return super().form_invalid(form)
    
    
class UserRegistrationView(FormView):
    template_name = 'auth/registration_form.html'
    form_class = RegistrationForm

    def form_valid(self, form):
        email = form.cleaned_data['username']
        phone_number = form.cleaned_data['phone_number']
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user = User.objects.create_user(username=username, email=email, password=password, is_active=False) 
        user.save()
        
        verification_code = random.randint(1000, 9999)
        Profile.objects.create(user=user, phone_number=phone_number, verification_code=verification_code)
        
        sms_text = f"Twój kod weryfikacyjny to: {verification_code}"
        send_sms(phone_number, sms_text)
        
        token = ActivateToken.objects.create(
                user=user,
                activation_token=str(int(str(uuid4()).split("-")[0], 16)),
            )
        send_activate_email_by_django(
                "Aktywacja konta", user, token.activation_token
            )

        messages.success(self.request, "Rejestracja zakończona sukcesem! Sprawdź swój email w celu aktywacji konta.")
        return redirect('home:home')

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        for field_name in form.fields:
            if field_name in form.cleaned_data:
                form.fields[field_name].initial = form.cleaned_data.get(field_name)

        messages.error(self.request, "Wystąpiły błędy w formularzu. Proszę poprawić zaznaczone pola.")
        return self.render_to_response(context)


class ActivateUserAccountByTokenView(FormView):
    template_name = "auth/activate_account.html"
    form_class = ActivationForm

    def dispatch(self, request, *args, **kwargs):
        self.token = kwargs.get("token")
        self.activate_token = get_object_or_404(ActivateToken, activation_token=self.token)

        if self.activate_token.is_used:
            messages.error(request, "Ten token został już użyty.")
            return redirect("home:home")

        if now() - self.activate_token.created_time > timedelta(days=1):
            messages.error(request, "Ten token stracił ważność.")
            return redirect("home:home")

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        verification_code = form.cleaned_data.get("verification_code")
        user = self.activate_token.user
        profile = user.profile

        if str(profile.verification_code) != verification_code:
            form.add_error("verification_code", "Kod weryfikacyjny jest nieprawidłowy.")
            return self.form_invalid(form)

        user.is_active = True
        user.save()

        self.activate_token.is_used = True
        self.activate_token.save()

        login(self.request, user)
        send_activate_info_email_by_django(user)

        messages.success(self.request, "Twoje konto zostało pomyślnie aktywowane.")
        return redirect("home:home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["token"] = self.token
        return context
    

class UserLogout(View):
    def get(self, request):
        logout(request)
        messages.success(
            request,
            "Wylogowano użytkownika",
        )
        return redirect("events:events_list")
    