from django.views.generic.edit import UpdateView
from django.shortcuts import render
from django.db.models.functions import Length
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Event
from .forms import AddEventForm
from dal import autocomplete
from datetime import datetime


def home(request):
    values = {}
    next_event = Event.objects.annotate(name_len=Length('name')).filter(date__gt=datetime.now(), name_len__gt=0, approved=True).order_by('date').first()
    values['next_event'] = next_event

    return render(request, "upcoming.html", values)


def user(request, username):
    values = {}
    user = User.objects.filter(username=username).first()
    upcoming_talks = Event.objects.filter(speakers__username=username, date__gt=datetime.now(), approved=True).exclude(name='').all()
    past_talks = Event.objects.filter(speakers__username=username, date__lt=datetime.now(), approved=True).exclude(name='').all()
    values['upcoming_talks'] = upcoming_talks
    values['past_talks'] = past_talks
    values['user'] = user

    return render(request, "user.html", values)


def events(request):
    values = {}
    upcoming_events = Event.objects.annotate(name_len=Length('name')).filter(date__gt=datetime.now(), name_len__gt=0, approved=True).order_by('date').all()
    past_events = Event.objects.annotate(name_len=Length('name')).filter(date__lt=datetime.now(), name_len__gt=0, approved=True).order_by('date').all()

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
            event.speakers = form.cleaned_data['speakers']

            event.save()

            print("Title: ", form.cleaned_data['title'])
            print("Date: ", form.cleaned_data['date'])
            print("Description: ", form.cleaned_data['description'])

            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/events/')
        else:
            print("nope")

            # if a GET (or any other method) we'll create a blank form
    else:
        form = AddEventForm(current_user=request.user)

    values['form'] = form

    return render(request, 'add_event.html', values)

class EventUpdate(UpdateView):
    model = Event
    fields = ['name', 'description']
    template_name_suffix = '_update_form'

class UserAutocomplete(autocomplete.Select2QuerySetView):
    def get_result_label(self, obj):
        if len(obj.first_name) > 0 and len(obj.last_name) > 0:
            return "{} {}".format(obj.first_name, obj.last_name)
        else:
            return "<{}>".format(obj.username)

    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return User.objects.none()

        qs = User.objects.all()

        if self.q:
            qs = qs.filter(Q(first_name__istartswith=self.q) | Q(last_name__istartswith=self.q) | Q(username__istartswith=self.q))

        return qs
