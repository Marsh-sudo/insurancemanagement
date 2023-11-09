import json
from django.core.exceptions import ImproperlyConfigured

with open('secrets.json') as f:
    secrects = json.load(f)

def get_secret(setting,secrets=secrects):
    '''Get the secret variable or return explicit exception.'''
    try:
        return secrets[setting]
    except KeyError:
        error_msg = 'Set the {0} environment variable'.format(setting)
        raise ImproperlyConfigured(error_msg)