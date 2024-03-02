# your_app/management/commands/update_points_per_day.py
from django.core.management.base import BaseCommand
from game.models import ReferralCount,ReferralVisit
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(body, to_email):
    subject = "Congratulations! You're Today's Referral Game Champion! Telekit.link"

    sender_email = "support@telekit.link"
    password = "1998Piriyaraj@"  # Use the email account’s password

    # SMTP server settings
    smtp_server = "telekit.link"
    smtp_port = 465

    # Create a MIMEText object for the email body
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = to_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        # Establish a secure connection with the SMTP server
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            # Log in to the email account
            server.login(sender_email, password)

            # Send the email
            server.sendmail(sender_email, to_email, message.as_string())

        print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {str(e)}")
   
class Command(BaseCommand):
    help = 'give referral points'

    def handle(self, *args, **options):
        body = """
Dear [Username],

Congratulations on being today's champion in our Referral Game!

We're thrilled to announce that you've won by attracting the most visitors to your referral link. As a reward for your outstanding performance, we've credited your account with 1000 points!

This achievement demonstrates your dedication and ability to engage others, and we're grateful for your contribution to our community.

Keep up the excellent work, and continue spreading the word about our platform!

Best regards,
Telekit.link
"""
        referral = ReferralCount.objects.all().order_by("-count")
        if referral:
            referral = referral[0]
            referral.user.points = referral.user.points + 1000
            referral.user.save()
            body = body.replace("[Username]",referral.user.username)
            send_email(body,referral.user.email)
        ReferralCount.objects.all().delete()
        ReferralVisit.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully updated points per day'))
