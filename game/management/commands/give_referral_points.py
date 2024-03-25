# your_app/management/commands/update_points_per_day.py
import time
from django.core.management.base import BaseCommand
from game.models import ReferralCount,ReferralVisit
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(body, to_email,subject):

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

Keep up the excellent work, and continue spreading the word about our platform by sharing your referral link: [referral_link]

Best regards,
Telekit.link
"""
        body_not_win ="""
Dear [Username],

We want to extend our sincere appreciation for your participation in our Referral Game!

While you may not have won today's competition, your efforts and engagement have not gone unnoticed. Your dedication to spreading the word about our platform is invaluable to us.

As a token of our gratitude, we've credited your account with 100 points for your participation.

Thank you for being an active member of our community, and we encourage you to continue sharing your referral link: [referral_link]. Every effort counts towards building a stronger community!

Best regards,
Telekit.link
        """
        referral_list = ReferralCount.objects.all().order_by("-count")
        if referral_list:
            referral = referral_list[0]
            referral.user.points = referral.user.points + 1000
            referral.user.save()
            body = body.replace("[Username]",referral.user.username)
            body = body.replace("[referral_link]",f"https://telekit.link/ref/telekit{referral.user.id}")
            subject = "Congratulations! You're Today's Referral Game Champion! Telekit.link"
            try:
                send_email(body, referral.user.email, subject)
            except:
                pass
            referral.delete()
        for ref in referral_list[1:]: 
            referral = ref
            referral.user.save()
            referral.user.points = referral.user.points + 100
            body_not_win = body_not_win.replace("[Username]",referral.user.username)
            body_not_win = body_not_win.replace("[referral_link]",f"https://telekit.link/ref/telekit{referral.user.id}")
            subject = "Thank You for Participating in Our Referral Game!"
            try:
                send_email(body_not_win,referral.user.email, subject)
            except:
                pass
            referral.delete()
            time.sleep(5)
        ReferralVisit.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully updated points per day'))
