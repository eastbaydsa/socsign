from django.shortcuts import render, get_object_or_404, redirect

from .models import EventForm
from .forms import EventFormStandard, EventFormLabor

from . import nbapi

form_variants = {
    'standard': EventFormStandard,
    'labor': EventFormLabor,
}

def event_form(request, public_hex):
    event = get_object_or_404(EventForm, public_hex=public_hex)

    FormClass = form_variants[event.variant]

    request.session['last_form'] = public_hex

    if request.method == "GET":
        # Is initial GET: Create a blank form
        form = FormClass(event=event)
    else:
        # Is POST: Create a form based on POST data
        form = FormClass(request.POST, event=event)
        if form.is_valid():
            ctx = {
                'show_check': True,
                'timeout': 3.0,
            }

            # let's do a person add API event
            json = nbapi.person_add(form.cleaned_data)
            print('just added person', json)
            return render(request, 'signin/event_form.html', ctx)

    ctx = {
        'form': form,
        'event': event,
    }
    return render(request, 'signin/event_form.html', ctx)
