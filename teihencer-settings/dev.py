import os
from apis_settings.base import *

SECRET_KEY = 'd3j@zo1psh*&-u35#ayi'

INSTALLED_APPS += ('teimporter',)

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True
DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.sqlite3',
       'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
   }
}

ROOT_URLCONF = 'custom_urls.urls'
