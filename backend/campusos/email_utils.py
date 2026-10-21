import logging

from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


def send_notification_email(recipient, subject, message):
    """Send a notification email without breaking the main workflow."""

    if not recipient:
        logger.warning("Notification email skipped: missing recipient.")
        return False

    try:
        sent = send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient],
            fail_silently=False,
        )

        return sent == 1

    except Exception:
        logger.exception("CampusOS notification email failed.")
        return False