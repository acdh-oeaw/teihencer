import os
from .base import *

SECRET_KEY = 'd3j@zo1psh*&-u35#ayi'

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True
DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.sqlite3',
       'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
   }
}
