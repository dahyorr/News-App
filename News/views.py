import math
from django.shortcuts import render
from django.views.generic import DetailView
from .models import NewsItem, Story, Job
# Create your views here.


def index(request):
    allowed_filters = ['story', 'job']
    items_per_page = 20
    query_set = NewsItem.objects

    # get query parameters
    search_query = request.GET.get('search', '').strip()
    filter_query = request.GET.get('filter', None)
    filter_query = None if filter_query not in allowed_filters else filter_query
    page_query = request.GET.get('page', 1)

    # filter based on query parameters
    if search_query:
        query_set = query_set.filter(title__icontains=search_query)
    if filter_query:
        query_set = query_set.filter(type=filter_query)
    if (not search_query) and (not filter_query):
        query_set = query_set.all()
    item_count = query_set.count()
    max_page = math.ceil(item_count/items_per_page)

    try:
        page = int(page_query)
        page = 1 if page < 1 or page > max_page else page
    except ValueError:
        page = 1
    query_set = query_set.order_by('-time_created')[(page - 1) * items_per_page:items_per_page * page]
    context = {
        'stories': query_set,
        'pages':  max_page,
        'current_page': page,
        'items_per_page': items_per_page,
        'title': f'Search Results for "{search_query}"' if search_query else'Latest News',
        'search': True if search_query else False
    }
    return render(request, 'News/index.html', context)


class StoryDetail(DetailView):
    model = Story
    template_name = "News/detail.html"


class JobDetail(DetailView):
    model = Job
    template_name = "News/detail.html"
