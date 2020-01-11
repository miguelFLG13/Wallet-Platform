from .base import *

DEBUG = True

ALLOWED_HOSTS = [LOCAL_IP, 'web', '3.120.116.4']

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

REDIS_HOST = 'redis'
REDIS_PORT = 6379