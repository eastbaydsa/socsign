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

class AdminEventChooserWidget(forms.widgets.RadioSelect):
    template_name = "signin/admin_event_chooser.html"

    def get_context(self, *args, **kwargs):
        ctx = super().get_context(*args, **kwargs)
        return ctx


class EventFormAdminForm(forms.ModelForm):

    class Meta:
        model = EventForm
        fields = ('event_id', 'variant', 'start_time', 'end_time',
        'interest_choices')

    event_id = forms.ChoiceField(
        required=True,
        choices=get_event_choices,
        widget=AdminEventChooserWidget,
    )

    def save(self, commit=True):
        event = super().save(commit=commit)
        event_id = self.cleaned_data.get('event_id', None)
        event_title = dict(get_event_choices())[event_id]
        event.event_id = event_id
        event.event_title = event_title
        return event


@admin.register(EventForm)
class EventFormAdmin(admin.ModelAdmin):
    list_display = ('event_title', 'event_id', 'start_time', 'end_time')
    exclude = ('public_hex', 'secret_hex')
    form = EventFormAdminForm


@admin.register(InterestChoice)
class InterestChoiceAdmin(admin.ModelAdmin):
    list_display = ('caption', 'tag')



