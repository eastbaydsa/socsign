import json
import logging
import requests

from django.utils.dateparse import parse_datetime
from django.conf import settings

from .helpers import throttle, prune_dict


# Get an instance of a logger
logger = logging.getLogger('nbapi')

#from .test_data import nb_events

DOMAIN = 'https://%s.nationbuilder.com' % settings.NB_SITE_SLUG
PARAMS = {'access_token': settings.NB_TOKEN}

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


def _url_base(*path):
    return '/'.join((
        f'https://{settings.NB_SITE_SLUG}.nationbuilder.com',
        'api/v1',
    ) + path)


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

def person_add(info, tags, parse_response=False):
    '''
    Upserts a person with the given info (derived from a form) and tags.
    '''
    info_dict = {
        'email': info['email'],
        'first_name': info['first_name'],
        'last_name': info['last_name'],
        'mobile': str(info['mobile_number']),
        'phone': str(info['home_phone_number']),
        'home_address': {
            'address1': info['address'],
            'city': info['city'],
            'zip': info['zip_code'],
        },
        'tags': tags,
    }

    # Clean up False-y values, and prep JSON dict and URL
    prune_dict(info_dict)
    json_dict = {"person": info_dict}
    url = _url_base('people', 'add')

    # Make request to URL with person API
    if not parse_response:
        requests.put(url, json=json_dict, params=PARAMS)
        return

    # Otherwise, we parse the response
    # Note: Presently dead code
    try:
        response = requests.put(url, json=json_dict, params=PARAMS)
    except Exception as e:
        logger.error('Could not make API call: %s' % str(e))

    try:
        d = response.json()
    except Exception as e:
        logger.error('Could not decode API from response: %s' % str(e))

    # prune_dict(d) # Debugging:
    # print(json.dumps(d, indent=2))

    id_result = d.get('person', {}).get('id')
    logger.info('Registered ID: %s' % str(id_result))
    return id_result

