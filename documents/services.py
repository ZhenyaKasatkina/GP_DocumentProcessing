from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER


def send_email_message(subject, message, email):
    """Направляет письмо адресату"""

    send_mail(
        subject=subject,
        message=message,
        from_email=EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )
