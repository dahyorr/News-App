from django.apps import AppConfig


class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'News'

    def ready(self):
        """
        runs Scheduler
        :return:
        """
        print('Starting Scheduler...')
        from news_scheduler import newsUpdater
        newsUpdater.start()
