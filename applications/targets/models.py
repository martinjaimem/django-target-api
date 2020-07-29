from django.contrib.gis.db import models

from applications.users.models import User


class Topic(models.Model):
    name = models.CharField(max_length=50, default='', unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Target(models.Model):
    MAX_COUNT_TARGETS_PER_USER = 10

    location = models.PointField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    radius = models.PositiveIntegerField()
    title = models.CharField(max_length=100)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
