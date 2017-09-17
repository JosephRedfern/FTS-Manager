from django import forms
from .models import Event
from django.contrib.auth.models import User


class AddEventForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(AddEventForm, self).__init__(*args)

        if kwargs.get('current_user') is not None:
            self.fields['speakers'].initial = kwargs.get('current_user')

    title = forms.CharField(label='Talk Title')
    date = forms.ModelChoiceField(queryset=Event.objects.filter(speakers__isnull=True))
    description = forms.CharField(widget=forms.Textarea, label="Talk Description")
    speakers = forms.ModelMultipleChoiceField(queryset=User.objects.all())