import requests
from django.utils.dateparse import parse_datetime
from datetime import datetime, timedelta
from functools import wraps

#from .test_data import nb_events

# Throttle API hits with a decorator, taken & modified from:
# https://gist.github.com/ChrisTM/5834503
class throttle:
    """
    Decorator that prevents a function from being called more than once every
    time period.
    To create a function that cannot be called more than once a minute:
        @throttle(minutes=1)
        def my_fun():
            pass
    """
    def __init__(self, seconds=3):
        self.throttle_period = timedelta(seconds=seconds)
        self.time_of_last_call = datetime.min
        self.last_return = None

    def __call__(self, fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            now = datetime.now()
            time_since_last_call = now - self.time_of_last_call
            if time_since_last_call > self.throttle_period:
                self.time_of_last_call = now
                self.last_return = fn(*args, **kwargs)
            return self.last_return
        return wrapper

DOMAIN = 'http://{slug}.nationbuilder.com'
PATH = 'api/v1/sites/{slug}/pages'
QUERYSTRING = '{page}&access_token={token}'
TEMPLATE = '/'.join([DOMAIN, PATH, QUERYSTRING])

def _url(page):
    link = TEMPLATE.format(
        slug=settings.NB_SITE_SLUG,
        token=settings.NB_TOKEN,
        page=page,
    )
    return link

@throttle()
def get_upcoming_events():
    response = requests.get(_url('events?limit=30&__proto__='))
    nb_events = response.json()
    results = []
    for event in nb_events['results']:
        #start_time = parse_datetime(event['start_time'])
        #end_time = parse_datetime(event['end_time'])
        results.append({
            'slug': event['slug'],
            'name': event['name'],
            'start_time': event['start_time'],
            'end_time': event['end_time'],
        })
    return results

