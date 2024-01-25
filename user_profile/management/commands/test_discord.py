from discordwebhook import Discord
def DiscordNotification(Msg):
    webHookUrl = "https://discord.com/api/webhooks/1132597585824202813/8XDNjpwwOIsistL4nThyY7NjVo67UVHckbtOAAdGAf96_TZ7dTS3tOpDmle646rF_ZDX"
    discord = Discord(url = webHookUrl)
    discord.post(content=Msg)



from django.core.management.base import BaseCommand
from user_profile.models import Linkpin

class Command(BaseCommand):
    help = 'Update points per day for Linkpin instances'

    def handle(self, *args, **options):
        DiscordNotification("test message")