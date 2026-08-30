from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import Request
from accounts.services.email_service import send_overdue_email


class Command(BaseCommand):
    help = "Send emails to employees who have overdue equipment"

    def handle(self, *args, **kwargs):

        today = timezone.localdate()

        overdue_requests = Request.objects.filter(
            return_date__lt=today,
            overdue_email_sent=False,
        )

        count = 0

        for request in overdue_requests:

            # Vérifier qu'il existe au moins un item
            # qui n'a pas encore été retourné
            has_unreturned_item = request.items.exclude(
                status="Returned"
            ).exists()

            if not has_unreturned_item:
                continue

            # Vérifier qu'un email existe
            if not request.employee_email:
                self.stdout.write(
                    self.style.WARNING(
                        f"No email for request {request.request_id}"
                    )
                )
                continue

            try:

                send_overdue_email(request)

                request.overdue_email_sent = True
                request.save(update_fields=["overdue_email_sent"])

                count += 1

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Email sent for {request.request_id} "
                        f"to {request.employee_email}"
                    )
                )

            except Exception as error:

                self.stdout.write(
                    self.style.ERROR(
                        f"Failed to send email for "
                        f"{request.request_id}: {error}"
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"{count} overdue email(s) sent."
            )
        )