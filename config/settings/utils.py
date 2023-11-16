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
    

# import os

# from django.core.exceptions import ImproperlyConfigured

# def get_env_variable(var_name):
#     """Get the environment variable or return exception."""
#     try:
#         return os.environ[var_name]
#     except:
#         error_msg = 'Set the {} environment variable'.format(var_name)
#         raise ImproperlyConfigured(error_msg)