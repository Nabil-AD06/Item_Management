from django.core.mail import send_mail
from django.conf import settings


def send_overdue_email(request):
    subject = f"Equipment Return Reminder - {request.request_id}"

    message = f"""
Hello {request.employee_name},

This is a reminder that the equipment associated with request
{request.request_id} should have been returned.

Return date: {request.return_date}

Please return the equipment as soon as possible.

Thank you.

Asset Management System
"""

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[request.employee_email],
        fail_silently=False,
    )