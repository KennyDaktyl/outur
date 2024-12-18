from django.urls import path
from .views import UserLogout, UserRegistrationView, LoginView, ActivateUserAccountByTokenView


app_name = "auth"


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('aktywacja-konta/<token>', ActivateUserAccountByTokenView.as_view(), name='activate_account'),
    path('login/', LoginView.as_view(), name='login'),
    path('wyloguj/', UserLogout.as_view(), name='logout'),
]
