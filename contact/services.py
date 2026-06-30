from django.core.mail import send_mail
from django.conf import settings
from .models import ContactMessage

class ContactService:
    @staticmethod
    def process_submission(form, request) -> ContactMessage:
        message = form.save(commit=False)
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        message.ip_address = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')
        message.save()
        ContactService._send_notification(message)
        return message

    @staticmethod
    def _send_notification(message: ContactMessage):
        try:
            send_mail(
                subject=f'[Portfolio] New message from {message.name}',
                message=f"Name: {message.name}\nEmail: {message.email}\nSubject: {message.subject}\n\n{message.message}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_EMAIL],
                fail_silently=True,
            )
        except Exception:
            pass
