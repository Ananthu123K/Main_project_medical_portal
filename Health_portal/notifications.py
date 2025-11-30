from django.core.mail import send_mail
from django.conf import settings
from webapp.models import DonorRegistrationDb, DonorNotification
import requests

# ------------------------------------
# EMAIL FUNCTION
# ------------------------------------
def send_email(donor_email, subject, body):
    send_mail(
        subject,
        body,
        settings.EMAIL_HOST_USER,
        [donor_email],
        fail_silently=True
    )

# ------------------------------------
# SMS FUNCTION (Fast2SMS)
# ------------------------------------
def send_sms(phone, message):
    api_key = getattr(settings, 'FAST2SMS_API_KEY', '')
    if not api_key or not phone:
        return

    try:
        requests.post(
            "https://www.fast2sms.com/dev/bulkV2",
            json={
                "route": "q",
                "message": message,
                "language": "english",
                "flash": 0,
                "numbers": phone
            },
            headers={
                "authorization": api_key,
                "Content-Type": "application/json"
            },
            timeout=15
        )
    except:
        pass


# ------------------------------------
# NOTIFY DONORS
# ------------------------------------
from django.db import transaction

def notify_donors(blood_request):

    donors = DonorRegistrationDb.objects.filter(
        BloodGroup__iexact=blood_request.blood_group.strip()
    )

    notification_objects = []
    notifications_to_send = []

    message_template = (
        f"Urgent need for {blood_request.blood_group} blood.\n"
        f"Patient: {blood_request.patient_name}\n"
        f"Location: {blood_request.location}\n"
        f"Units: {blood_request.units}"
    )

    with transaction.atomic():  # GUARANTEES DB integrity
        for donor in donors:
            notification_objects.append(
                DonorNotification(
                    donor=donor,
                    blood_request=blood_request,
                    message=message_template,
                    is_seen=False
                )
            )
            notifications_to_send.append((donor, message_template))

        # 🔥 One DB write only → ZERO LOCKS
        DonorNotification.objects.bulk_create(notification_objects)

    # ──────────────────────────────────────
    # SEND EMAIL/SMS OUTSIDE DB TRANSACTION
    # ──────────────────────────────────────
    for donor, message in notifications_to_send:
        try:
            send_email(donor.Email, f"Blood Request: {blood_request.blood_group}", message)
            send_sms(donor.phone, message)
        except:
            pass
