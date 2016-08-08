from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


class Location(models.Model):
    room_number = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.room_number


class Event(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateTimeField()
    location = models.ForeignKey(Location)
    speakers = models.ManyToManyField(User)

    def __str__(self):
        return "{0}: {1}".format(self.name, [speaker for speaker in self.speakers.iterator()])

