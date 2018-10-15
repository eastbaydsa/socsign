from functools import wraps
from datetime import datetime, timedelta

# Throttle API hits with a decorator, taken & modified from:
# https://gist.github.com/ChrisTM/5834503
class throttle:
    """
    Decorator that prevents a function from being called more than once every
    time period.
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

def prune_dict(d):
    '''
    Prune dict of all non-truthy values, recursively
    '''
    to_delete = set()
    for key in d:
        if not d[key]:
            to_delete.add(key)
        elif isinstance(d[key], dict):
            prune_dict(d[key])
            if not d[key].keys():
                to_delete.add(key)

    for key in to_delete:
        del d[key]



