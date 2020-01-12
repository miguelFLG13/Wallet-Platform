from .base import *

DEBUG = True

ALLOWED_HOSTS = [LOCAL_IP]

ROOT_URLCONF = 'wallet_platform.urls.urls'

CACHES = {
    'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
}

ROOT_URLCONF = 'wallet_platform.urls.urls_local'