from django.shortcuts import get_object_or_404, render
from django.db.models.functions import Length
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Event
from .forms import AddEventForm, EditEventForm
from dal import autocomplete
from django_ical.views import ICalFeed
from django.contrib import messages
from django.utils import timezone
from django.core.mail import send_mail


def home(request):
    values = {}
    next_event = Event.objects.annotate(name_len=Length('name')).filter(date__gt=timezone.now(), name_len__gt=0, approved=True).order_by('date').first()
    values['next_event'] = next_event

    return render(request, "upcoming.html", values)


def me(request):
    if request.user is not None and request.user.username is not None and len(request.user.username.strip()) > 0:
        return HttpResponseRedirect(reverse('user', kwargs={'username': request.user.username}))
    else:
        return HttpResponseRedirect(reverse('home'))


def about(request):
    values = {}

    return render(request, "about.html", values)


def user(request, username):
    values = {}
    user = User.objects.filter(username=username).first()
    upcoming_talks = Event.objects.filter(speakers__username=username, date__gt=timezone.now(), approved=True).exclude(name='').all()
    past_talks = Event.objects.filter(speakers__username=username, date__lt=timezone.now(), approved=True).exclude(name='').all()
    values['upcoming_talks'] = upcoming_talks
    values['past_talks'] = past_talks
    values['speaker'] = user

    return render(request, "user.html", values)


def events(request):
    values = {}
    upcoming_events = Event.objects.annotate(name_len=Length('name')).filter(date__gt=timezone.now(), name_len__gt=0, approved=True).order_by('date').all()
    past_events = Event.objects.annotate(name_len=Length('name')).filter(date__lt=timezone.now(), name_len__gt=0, approved=True).order_by('-date').all()

    values['upcoming_events'] = upcoming_events
    values['past_events'] = past_events

    return render(request, "events.html", values)


def event(request, event_id):
    values = {}
    event = Event.objects.get(pk=event_id, approved=True)
    values['event'] = event
    return render(request, "event.html", values)


@login_required
def add_event(request):
    values = {}

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AddEventForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            event = form.cleaned_data['date']
            event.name = form.cleaned_data['title']
            event.description = form.cleaned_data['description']
            event.save()
            event.speakers.set(form.cleaned_data['speakers'])
            send_mail("New FTS talk submitted",
                      "A new FTS talk (title: \"{}\") has been submitted, please check and approve at https://fts.cs.cf.ac.uk/admin/events/event/{}/change/.".format(event.name, event.id),
                      "FTS Manager <fts-list-owner@cs.cf.ac.uk>",
                      ["fts-list-owner@cs.cf.ac.uk"])

            messages.success(request, "Thank you - your event has been received, and is pending approval.")

            return HttpResponseRedirect('/events/')
        else:
            messages.error(request, "There was an error in your form.")

    else:
        form = AddEventForm(current_user=request.user)

    values['form'] = form

    return render(request, 'add_event.html', values)


def edit_event(request, event_id):
    instance = get_object_or_404(Event, id=event_id)

    if not (request.user.is_staff or request.user in instance.speakers.all()):
        raise PermissionDenied("You do not have permission to edit events in which you are not a speaker.")

    form = EditEventForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()

        return HttpResponseRedirect(reverse('event', kwargs={'event_id': event_id}))

    return render(request, "edit_event.html", {'form': form})


class EventFeed(ICalFeed):
    title = "FTS Calendar"
    product_id = '-//example.com//Example//EN'
    timezone = 'UTC'
    file_name = "event.ics"

    def items(self):
        return Event.objects.filter(approved=True).exclude(name='').all()

    def item_title(self, item):
        return "{} - ({})".format(item.name, ','.join(["{} {}".format(x.first_name, x.last_name) for x in item.speakers.all()]))

    def item_description(self, item):
        return item.description

    def item_location(self, item):
        return item.location

    def item_link(self, item):
        return "/events/{}".format(item.id)

    def item_organiser(self, item):
        return ", ".join([str(x) for x in item.speakers])

    def item_start_datetime(self, item):
        return item.date

    def item_end_datetime(self, item):
        return item.date + item.duration


class UserAutocomplete(autocomplete.Select2QuerySetView):
    def get_result_label(self, obj):
        if len(obj.first_name) > 0 and len(obj.last_name) > 0:
            return "{} {}".format(obj.first_name, obj.last_name)
        else:
            return "<{}>".format(obj.username)

    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return User.objects.none()

        qs = User.objects.all()

        if self.q:
            qs = qs.filter(Q(first_name__istartswith=self.q) | Q(last_name__istartswith=self.q) | Q(username__istartswith=self.q))

        return qs
