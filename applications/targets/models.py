from django.contrib.gis.db import models

from applications.users.models import User


class Topic(models.Model):
    name = models.CharField(max_length=50, blank=False, default='')

    def __str__(self):
        return self.name


class Target(models.Model):
    location = models.PointField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    radius = models.PositiveIntegerField(default=0)
    title = models.CharField(max_length=100, blank=False, default='')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, blank=False)
