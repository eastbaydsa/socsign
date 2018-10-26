import json

from django.contrib import admin
from django import forms
from socsign.signin.models import EventForm, InterestChoice
from django.utils.html import format_html

from . import nbapi

def get_event_label(event):
    event_date = event.get('start_time', '').split('T')[0]
    return '%s - %s' % (event['name'], event_date)

def get_event_choices():
    upcoming_events = nbapi.get_upcoming_events()
    upcoming_events.sort(key=lambda event: event.get('start_time'))
    return [
        (event['slug'], get_event_label(event))
        for event in reversed(upcoming_events)
    ]

class AdminEventChooserWidget(forms.widgets.RadioSelect):
    template_name = "signin/admin_event_chooser.html"

    def get_context(self, *args, **kwargs):
        ctx = super().get_context(*args, **kwargs)
        events_json = json.dumps(nbapi.get_upcoming_events(), indent=2)
        ctx['events_json'] = events_json
        return ctx


class EventFormAdminForm(forms.ModelForm):

    class Meta:
        model = EventForm
        fields = (
            'event_id',
            'event_tag',
            'event_title',
            'start_time',
            'end_time',
            'variant',
            'interest_choices',
        )

    event_id = forms.ChoiceField(
        required=True,
        label="Event",
        choices=get_event_choices,
        widget=AdminEventChooserWidget,
    )

    '''
    def save(self, commit=True):
        event = super().save(commit=commit)
        event_id = self.cleaned_data.get('event_id', None)
        event_title = dict(get_event_choices())[event_id]
        event.event_id = event_id
        event.event_title = event_title
        return event
    '''


@admin.register(EventForm)
class EventFormAdmin(admin.ModelAdmin):
    list_display = (
        'event_title', 'event_tag', 'start_time', 'end_time',
        'submission_count', 'form_url_column'
    )

    # We are not doing select related for submissions, so as a hack we cap the
    # pagination to 10 to prevent too many queries
    list_per_page = 10

    exclude = ('public_hex', 'secret_hex')
    form = EventFormAdminForm

    def submission_count(self, obj):
        return obj.get_submission_count()
    submission_count.short_description = 'Count'

    def form_url_column(self, obj):
        url = obj.get_absolute_url()
        return format_html('<a target="_blank" href="{0}">{0}</a>', url)
    form_url_column.short_description = 'Display URL'

@admin.register(InterestChoice)
class InterestChoiceAdmin(admin.ModelAdmin):
    list_display = ('caption', 'tag')



