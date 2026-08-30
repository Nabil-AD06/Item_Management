from django.core.mail import send_mail
from django.conf import settings


def send_overdue_email(request):

    # Récupérer uniquement les items qui ne sont pas retournés
    items = request.items.exclude(status="Returned")

    # Construire la liste des équipements
    items_text = ""

    for item in items:
        items_text += (
            f"- {item.accessory_req}"
            f" | Brand/Model: {item.brand_model or 'N/A'}"
            f" | Serial Number: {item.serial_Number or 'N/A'}"
            f" | Quantity: {item.quantity}"
            f" | Status: {item.status}\n"
        )

    subject = f"Overdue Equipment - {request.request_id}"

    message = f"""
Hello {request.employee_name or 'Employee'},

Your equipment request {request.request_id} is overdue.

Return date: {request.return_date}

The following equipment has not yet been returned:

{items_text}

Please return the equipment as soon as possible.

Thank you,
Asset Management
"""

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [request.employee_email],
        fail_silently=False,
    )