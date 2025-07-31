from django.core.mail import send_mail

def send_email_alert(message):
    send_mail(
        subject='Smart Light Alert',
        message=message,
        from_email=None,
        recipient_list=['admin@example.com'],
        fail_silently=False
    )
