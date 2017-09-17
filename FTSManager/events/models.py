from django.db import models
from django.contrib.auth.models import User


class Location(models.Model):
    room_number = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.room_number


class Event(models.Model):
    name = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    date = models.DateTimeField()
    location = models.ForeignKey(Location, blank=True, null=True)
    speakers = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return "{}".format(self.date)

