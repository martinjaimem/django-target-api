from django.contrib.gis.db import models

from applications.users.models import User


class Topic(models.Model):
    name = models.CharField(max_length=50, blank=False, default='')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Target(models.Model):
    location = models.PointField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    radius = models.PositiveIntegerField()
    title = models.CharField(max_length=100, blank=False)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, blank=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
