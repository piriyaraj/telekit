# your_app/management/commands/update_points_per_day.py
from django.core.management.base import BaseCommand
from user_profile.models import Linkpin
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(subject, body, to_email):
    # Email configuration
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
   
subject = "Pinned Link status updated - Telekit.link"


class Command(BaseCommand):
    body = f"""
    Dear Telekit.link member,

    your group pinning time expired. Dont worry you can pin it again and get lot of members to your telegram.

    Pin_link


    Thank you
    Regards
    Telekit.link
    """
    help = 'Update points per day for Linkpin instances'

    def handle(self, *args, **options):
        linkpins = Linkpin.objects.all()
        for linkpin in linkpins:
            status = linkpin.update_points_per_day()
            if(status == "Removed"):
                to_mail = linkpin.user.email
                self.body = self.body.replace("Pin_link","https://telekit.link/pin/"+linkpin.linkId)
                send_email(subject,self.body,to_mail)
        self.stdout.write(self.style.SUCCESS('Successfully updated points per day'))
