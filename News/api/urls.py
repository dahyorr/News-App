from django.urls import path, include
from . import views
from rest_framework import routers
router = routers.DefaultRouter()
router.register('news', views.NewsItemApiView, basename='News')
router.register('story', views.StoryApiView, basename='Story')
router.register('job', views.JobApiView, basename='Job')

app_name = 'News'
urlpatterns = [
    path('', include(router.urls)),

]
