import json

import requests
from django.utils.dateparse import parse_datetime
from django.conf import settings

from .helpers import throttle, prune_dict

#from .test_data import nb_events

DOMAIN = 'http://{slug}.nationbuilder.com'

def _url_pages(page):
    template = '/'.join([
        DOMAIN,
        'api/v1/sites/{slug}/pages',
        '{page}&access_token={token}',
    ])
    uri = template.format(
        slug=settings.NB_SITE_SLUG,
        token=settings.NB_TOKEN,
        page=page,
    )
    return uri

def _url_people(verb):
    template = '/'.join([
        DOMAIN,
        'api/v1/people',
        '{page}?access_token={token}',
    ])
    uri = template.format(
        slug=settings.NB_SITE_SLUG,
        token=settings.NB_TOKEN,
        page=verb,
    )
    return uri

@throttle()
def get_upcoming_events():
    response = requests.get(_url_pages('events?limit=30&__proto__='))
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

def person_tag(person_id, info):
    pass

def person_add(info):

    # Upsert person
    info_dict = {
        'email': info['email'],
        'first_name': info['first_name'],
        'last_name': info['last_name'],
        'mobile': info['mobile_number'],
        'phone': info['home_phone_number'],
        'address': info['address'],
        'primary_address': {
            'address1': info['address'],
            'city': info['city'],
            'zip': info['zip_code'],
        },
    }
    prune_dict(info_dict)

    # for some reason we need to put it in a dict
    # called person
    request_dict = {
        "person": info_dict,
    }

    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
    }

    url = _url_people('push')
    print(url)
    print(request_dict)
    #response = requests.post(url, json=request_dict)
    response = requests.post(url, data=json.dumps(request_dict), headers=headers)
    d = response.json()
    return d


#jefflee.nationbuilder.com/api/v1/people/add?access_token=ba7cfd89bac4db76e3433e72c9198355f8034fbc75cfd051ae15077addceda4c
