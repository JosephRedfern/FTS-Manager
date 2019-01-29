from django.core.management.base import BaseCommand, CommandError
from django.template import defaultfilters
from django.conf import settings
from events.models import Event, SentNotification, Notification
from django.utils import timezone
from django.core.mail import send_mail, send_mass_mail
from django.template import Context
from django.template import Template
import kronos
import time


@kronos.register('*/5 * * * *')
class Command(BaseCommand):
    help = 'Send scheduled emails'

    def handle(self, *args, **options):
        future_events = Event.objects.filter(send_notifications=True, approved=True, date__gt=timezone.now())
        notifications = Notification.objects.filter(active=True)

        # look at every future event
        for event in future_events:
            # look at every potential notification
            for notification in notifications:
                print(f"Notification <{notification}> found for <{event}>")
                # check if it's time to send the notification yet, and that the event hasn't already occuret, and that the event hasn't already occured
                if event.date - notification.notice <= timezone.now() and event.date > timezone.now():
                    # make sure we've not sent it already
                    if SentNotification.objects.filter(event=event, notification=notification).count() == 0:
                        print(f"In date and never sent before -- sending!")

                        # if we're only sending to speakers, use their email addresses, otherwise send to fts-list.
                        if notification.speakers_only or notification.abstract_reminder:
                            emails = [e.email for e in event.speakers.all()]
                        else:
                            emails = ["fts-list@cs.cf.ac.uk"]

                        emails.append("redfernjm@cs.cf.ac.uk")

                        # We only want to send abstract reminders if the current abstract is empty.
                        # I'm define "empty" as <= 3 words (since a common placeholder is "to do" or "TBA")
                        if notification.abstract_reminder and len(event.description.strip().split(" ")) > 3:
                            continue

                        subject_template = Template(notification.subject)
                        message_template = Template(notification.message)

                        # so we can provide pre-formatted in the template.
                        speakers_formatted = ", ".join(["{} {}".format(s.first_name, s.last_name) if len(s.first_name) > 0 else s.username for s in event.speakers.all()])

                        # template context that will be used to populate the template
                        ctx = Context({'event': event, 'speakers': speakers_formatted, 'time': defaultfilters.date(event.date, 'g:i')}, autoescape=False)

                        # actually render the templates to get out the text that we're going to include in our email.
                        rendered_subject = subject_template.render(ctx)
                        rendered_message = message_template.render(ctx)

                        # BAM.
                        send_mail(rendered_subject,
                                  rendered_message,
                                  "FTS Manager <fts-list-owner@cs.cardiff.ac.uk>",
                                  emails,
                                  fail_silently=False)

                        print("Sent email(s) to {} for notification {} about event {}".format(emails, notification, event))
                        sn = SentNotification(event=event, notification=notification)
                        sn.save()
