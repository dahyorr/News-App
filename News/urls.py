from django.urls import path, include
from . import views


app_name = 'News'
urlpatterns = [
    path('', views.index, name="Homepage"),
    path('story/<int:pk>', views.StoryDetail.as_view(), name="Story Detail"),
    path('job/<int:pk>', views.JobDetail.as_view(), name="Job Detail"),
    path('api/', include('News.api.urls')),

]
