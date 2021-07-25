from django.core.management.base import BaseCommand

from news_scheduler.newsUpdater import get_last_100


class Command(BaseCommand):
    """
    Django Management command to fetch 100 news items from hacker news api
    """
    help = 'Fetches 100 news items from hacker news api'

    def handle(self, *args, **options):
        get_last_100()
        self.stdout.write(self.style.SUCCESS('Successfully fetched items'))
        return
