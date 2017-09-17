from django import forms
from .models import Event
from django.contrib.auth.models import User



class AddEventForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(AddEventForm, self).__init__(*args)

        if kwargs.get('current_user') is not None:
            self.fields['speakers'].initial = kwargs.get('current_user')

        self.fields['speakers'].label_from_instance = self.label_from_instance

    @staticmethod
    def label_from_instance(obj):
        if len(obj.first_name) > 0 and len(obj.last_name) > 0:
            return "{} {}".format(obj.first_name, obj.last_name)
        else:
            return "<{}>".format(obj.username)


    title = forms.CharField(label='Talk Title')
    date = forms.ModelChoiceField(queryset=Event.objects.filter(name=''))
    description = forms.CharField(widget=forms.Textarea, label="Talk Description")
    speakers = forms.ModelMultipleChoiceField(queryset=User.objects.all())
