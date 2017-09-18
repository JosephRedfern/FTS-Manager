from django import forms
from .models import Event
from django.contrib.auth.models import User
from datetime import datetime

class AddEventForm(forms.Form):
    def __init__(self, *args, **kwargs):
        """
        We override __init__ so that we can pass in the current user so that the form gets pre-populated with whoever
        is logged in.
        :param args:
        :param kwargs:
        """
        super(AddEventForm, self).__init__(*args)

        if kwargs.get('current_user') is not None:
            self.fields['speakers'].initial = kwargs.get('current_user')

        self.fields['speakers'].label_from_instance = self.label_from_instance

    @staticmethod
    def label_from_instance(obj):
        """
        This method swaps out the default for ModelMultipleChoiceField, which by default just calls __string__ on the
        object. In the case of a user object, this would normally be the username, which for COMSC has no relation to
        the actual name of the person. If first or last name are empty, we revert to the username (but this should be
        rare)
        :param obj:
        :return:
        """
        if len(obj.first_name) > 0 and len(obj.last_name) > 0:
            return "{} {}".format(obj.first_name, obj.last_name)
        else:
            return "<{}>".format(obj.username)

    title = forms.CharField(label='Talk Title')
    date = forms.ModelChoiceField(queryset=Event.objects.filter(name=''))
    description = forms.CharField(widget=forms.Textarea, label="Talk Description")
    speakers = forms.ModelMultipleChoiceField(queryset=User.objects.filter(date_gt=datetime.now()).exclude(first_name='', last_name='').all())
