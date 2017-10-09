from django.db import models
from django.contrib.auth.models import User
import datetime


class Location(models.Model):
    room_number = models.TextField(unique=True)

    def __str__(self):
        return self.room_number


class Event(models.Model):
    name = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    date = models.DateTimeField()
    location = models.ForeignKey(Location, blank=True, null=True)
    speakers = models.ManyToManyField(User, blank=True)
    approved = models.BooleanField(default=False)
    duration = models.DurationField(default=datetime.timedelta(minutes=50))
    send_notifications = models.BooleanField(default=True)

    def __str__(self):
        if self.name is None or len(self.name) == 0:
            return "{}".format(self.date)
        else:
            return "{}{} - {} ({})".format('[!] ' if not self.approved else '', self.name, ', '.join(["{} {}".format(x.first_name, x.last_name) if len(x.first_name) > 0 else x.username for x in self.speakers.all()]), self.date)


class Notification(models.Model):
    name = models.CharField(max_length=255)
    subject = models.TextField()
    message = models.TextField()
    notice = models.DurationField()
    speakers_only = models.BooleanField(default=True)
    abstract_reminder = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class SentNotification(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    notification = models.ForeignKey(Notification)
    event = models.ForeignKey(Event)

    def __str__(self):
        return "{} for {}".format(self.notification, self.event)