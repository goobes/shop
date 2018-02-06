"""
These settings overrides the ones in settings/base.py
"""

SECRET_KEY = 'somestring'
# you can also use environment variables to store secret values
# import os
# SECRET_KEY = os.environ['SECRET_KEY']

INSTAMOJO = {
    'API_KEY': 'test_xxx',
    'AUTH_TOKEN': 'test_xxx',
    'SALT': b'instamojosalt',
    'TEST': True #whether to use the test server or live server
}

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.',
#        'NAME': '',
#        'USER': '',
#        'PASSWORD': '',
#        'HOST': '',
#        'PORT': '',
#    },
#}


