from django.contrib import admin
from .models import Story, Comment, Job, PollOption, Poll, NewsItem
# Register your models here.
admin.site.register(NewsItem)
admin.site.register(Story)
admin.site.register(Job)
admin.site.register(Poll)
admin.site.register(PollOption)
admin.site.register(Comment)
