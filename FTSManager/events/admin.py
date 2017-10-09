from django.contrib import admin
from .models import Event, Location, Notification, SentNotification

# Register your models here.

admin.site.register(Event)
admin.site.register(Location)
admin.site.register(Notification)
admin.site.register(SentNotification)
