from rest_framework import serializers
from News.models import NewsItem, Story, Job


class NewsItemSerializer(serializers.ModelSerializer):
    reference_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = NewsItem
        fields = ['id', 'author', 'reference_id', 'title', 'url', 'score', 'type']


class StorySerializer(serializers.ModelSerializer):
    reference_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Story
        fields = ['id', 'author', 'reference_id', 'title', 'url', 'score']


class JobSerializer(serializers.ModelSerializer):
    reference_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Job
        fields = ['id', 'author', 'reference_id', 'title', 'url', 'score', 'text']
