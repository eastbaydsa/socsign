from django.contrib import admin
from django import forms
from socsign.signin.models import EventForm, InterestChoice

from . import nbapi

def get_event_choices():
    upcoming_events = nbapi.get_upcoming_events()
    return [
        (event['site_slug'], event['name'])
        for event in upcoming_events
    ]


class EventFormAdminForm(forms.ModelForm):

    class Meta:
        model = EventForm
        fields = ('event', 'variant', 'start_time',
        'end_time', 'interest_choices')

    event = forms.ChoiceField(
        required=True,
        choices=get_event_choices,
        widget=forms.RadioSelect,
    )


    def clean(self):
        cleaned_data = super().clean()
        self.cleaned_data['event_id'] = self.cleaned_data.get('event', None)
        self.cleaned_data['event_title'] = dict(get_event_choices())[event_id]

    #def save(self, commit=True):
    #    event.event_id = event_id
    #    event.event_title = event_title
    #    return event


@admin.register(EventForm)
class EventFormAdmin(admin.ModelAdmin):
    list_display = ('event_title', 'event_id', 'start_time', 'end_time')
    exclude = ('public_hex', 'secret_hex')
    form = EventFormAdminForm


@admin.register(InterestChoice)
class InterestChoiceAdmin(admin.ModelAdmin):
    list_display = ('caption', 'tag')



