from django.utils import timezone

from campusos.models import Notifications


VALID_NOTIFICATION_TYPES = {
    "MEMBERSHIP",
    "MEMBERSHIP_SUBMITTED",
    "MEMBERSHIP_REQUEST",
    "MEMBERSHIP_REVIEWED",
    "EVENT_APPROVAL",
    "EVENT_REGISTRATION",
    "ANNOUNCEMENT",
    "GENERAL",
}


def create_notification(
    user_id,
    title,
    message,
    notification_type="GENERAL",
    link=None,
):
    """Save an in-app notification for a user in MySQL."""
    if not user_id or not title or not message:
        return None

    # Prevent invalid values from reaching the MySQL ENUM column.
    if notification_type not in VALID_NOTIFICATION_TYPES:
        notification_type = "GENERAL"

    return Notifications.objects.create(
        user_id=user_id,
        title=title[:200],
        message=message,
        type=notification_type,
        is_read=0,
        created_at=timezone.now(),
        link=link[:255] if link else None,
    )