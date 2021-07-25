from django.db import models
from django.utils import timezone
# Create your models here.


class Base(models.Model):
    TYPES = (
        ('job', 'Job'),
        ('story', 'Story'),
        ('poll', 'Poll'),
        ('pollopt', 'Poll option'),
        ('comment', 'Comment'),
    )
    author = models.CharField(max_length=50)
    deleted = models.BooleanField(default=False, editable=False)
    dead = models.BooleanField(default=False, editable=False)
    fetched = models.BooleanField(default=False, editable=False)
    time_created = models.DateTimeField(default=timezone.now)
    reference_id = models.IntegerField(unique=True, null=True, blank=True)
    type = models.CharField(max_length=10, choices=TYPES, editable=False)

    class Meta:
        ordering = ['-time_created']

    def __str__(self):
        return f'{self.author}  {self.time_created}'


class NewsItem(Base):
    title = models.CharField(max_length=255)
    url = models.URLField(null=True, blank=True)
    score = models.IntegerField()

    class Meta:
        ordering = ['-time_created']

    def __str__(self):
        return self.title


class Story(NewsItem):
    descendants = models.IntegerField(null=True)

    def save(self, *args, **kwargs):
        self.type = 'story'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Stories'


class Job(NewsItem):
    text = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.type = 'job'
        super().save(*args, **kwargs)


class Comment(Base):
    parent = models.ForeignKey(Base, on_delete=models.CASCADE, related_name='comments', null=True)
    text = models.TextField()

    def save(self, *args, **kwargs):
        self.type = 'comment'
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.author}|{self.author}'


class Poll(Base):
    title = models.CharField(max_length=255)
    score = models.IntegerField()
    descendants = models.IntegerField(null=True)
    text = models.TextField()

    def save(self, *args, **kwargs):
        self.type = 'poll'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class PollOption(Base):
    author = None
    deleted = None
    dead = None
    score = models.IntegerField()
    text = models.TextField()
    parent = models.ForeignKey(Base, on_delete=models.CASCADE, related_name='pollOptions', null=True)

    def save(self, *args, **kwargs):
        self.type = 'pollopt'
        super().save(*args, **kwargs)

    def __str__(self):
        return f'pollOption {self.reference_id}'
