from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_activate_email_by_django(subject, user, token):
    subject, from_email, to = subject, settings.EMAIL_HOST_USER, user.email
    html_content = render_to_string(
        "auth/activation_email.html",
        {
            "button_link": f"{settings.DOMAIN_URL}/auth/aktywacja-konta/{token}",
            "user": user,
        },
    )
    html_content = html_content
    msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    

def send_activate_info_email_by_django(user):
    subject, from_email, to = (
        f"Nowy użytkownik w serwisie {user.email}",
        settings.EMAIL_HOST_USER,
        settings.EMAIL_HOST_USER,
    )

    html_content = render_to_string(
        "auth/activation_info_email.html",
        {
            "user": user,
        },
    )
    html_content = html_content
    msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
