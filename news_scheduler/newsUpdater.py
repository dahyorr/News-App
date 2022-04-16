from django.utils import timezone
from django.db.models import Max
from datetime import datetime
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from News.models import Story, Comment, Job, PollOption, Poll, Base

model_ref = {
    "job": Job,
    "comment": Comment,
    "story": Story,
    "poll": Poll,
    "pollopt": PollOption,
}


def sort_news(news_item):
    """
    Sorts news items by type into various models
    :param news_item: data retrieved from hacker news api
    """
    function_store = {
        'job': lambda item: Job(
            author=item['by'],
            time_created=timezone.make_aware(datetime.fromtimestamp(item['time'])),
            reference_id=item['id'],
            title=item['title'],
            url=item['url'],
            score=item['score'],
            text=item['text'] if 'text' in item else '',
            fetched=True,
        ).save(),

        'story': lambda item: Story(
            author=item['by'],
            time_created=timezone.make_aware(datetime.fromtimestamp(item['time'])),
            reference_id=item['id'],
            title=item['title'],
            url=item['url'] if 'url' in item else '',
            score=item['score'],
            descendants=item['descendants'] if 'descendants' in item else None,
            fetched=True,
        ).save(),

        'poll': lambda item: Poll(
            author=item['by'],
            time_created=timezone.make_aware(datetime.fromtimestamp(item['time'])),
            reference_id=item['id'],
            title=item['title'],
            text=item['text'],
            score=item['score'],
            descendants=item['descendants'] if 'descendants' in item else None,
            fetched=True,
        ).save(),

        'pollopt': lambda item: PollOption(
            time_created=timezone.make_aware(datetime.fromtimestamp(item['time'])),
            reference_id=item['id'],
            text=item['text'],
            score=item['score'],
            parent=Base.objects.get(reference_id=item['poll']),
            fetched=True,
        ).save(),

        'comment': lambda item: Comment(
            author=item['by'],
            time_created=timezone.make_aware(datetime.fromtimestamp(item['time'])),
            reference_id=item['id'],
            parent=Base.objects.get(reference_id=item['parent']),
            text=item['text'] if 'text' in item else '',
            fetched=True,
        ).save(),

    }
    function_store.get(news_item['type'], lambda x: f'{x.type} Does not exits')(news_item)


def update_news(news_item):
    """
    Update previously stored data with new data
    :param news_item: data retrieved from hacker news api
    """
    print("Updating Instead")
    item = model_ref.get(news_item['type']).objects.get(reference_id=news_item['id'])
    item.dead = news_item['dead'] if 'dead' in news_item else item.dead
    item.deleted = news_item['deleted'] if 'deleted' in news_item else item.deleted
    item.score = news_item['score'] if 'score' in news_item else None
    item.descendants = news_item['descendants'] if 'descendants' in news_item else None
    item.text = news_item['text'] if 'text' in news_item else None
    item.save()


def check_if_exists(news_item):
    """
    Initiates process of deciding if to update or create new model instance
    :param news_item: data retrieved from hacker news api
    """
    print(news_item)
    if Base.objects.filter(reference_id=news_item['id']).exists():
        update_news(news_item)
    else:
        sort_news(news_item)


def check_for_parent(news_item):
    """
    Checks if data returned from hacker news api has a parent
    :param news_item: data retrieved from hacker news api
    """
    tree = []
    while 'parent' in news_item or 'poll' in news_item:
        tree.append(news_item)
        if 'parent' in news_item:
            news_item = requests.get(f'https://hacker-news.firebaseio.com/v0/item/{news_item["parent"]}.json').json()
        else:
            news_item = requests.get(f'https://hacker-news.firebaseio.com/v0/item/{news_item["poll"]}.json').json()
    else:
        tree.append(news_item)
    if len(tree) > 0:
        for tree_item in reversed(tree):
            check_if_exists(tree_item)
    else:
        check_if_exists(news_item)


def get_last_100():
    """
    Gets last 100 news items from hacker news api
    """
    print("Getting last  100 items")
    last_item = requests.get('https://hacker-news.firebaseio.com/v0/maxitem.json').json()
    items = list(range(last_item - 99, last_item + 1))
    for item in items:
        r = requests.get(f'https://hacker-news.firebaseio.com/v0/item/{item}.json').json()
        if 'deleted' in r:
            continue
        check_for_parent(r)


def sync_news_list():
    """
    Syncs new news items from hacker news api based on last item in database
    :return:
    """
    print(f'Syncing latest News items at{datetime.now()}...')
    max_item = requests.get('https://hacker-news.firebaseio.com/v0/maxitem.json').json()
    last_item = Base.objects.aggregate(Max('reference_id'))['reference_id__max']
    items = list(range(last_item + 1, max_item + 1))
    for item in items:
        if Base.objects.filter(reference_id=item).exists():
            r = requests.get(f'https://hacker-news.firebaseio.com/v0/item/{item}.json').json()
            update_news(r)
            continue
        else:
            r = requests.get(f'https://hacker-news.firebaseio.com/v0/item/{item}.json').json()
            if 'deleted' in r:
                continue
            check_for_parent(r)
    print(f'Done at {datetime.now()}')


def start():
    """
    Starts scheduler to run sync_news_list every 5 minutes
    :return:
    """
    scheduler = BackgroundScheduler()
    scheduler.add_job(sync_news_list, "interval", minutes=5, id='news1', replace_existing=True)
    scheduler.start()
