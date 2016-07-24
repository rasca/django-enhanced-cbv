import os

SECRET_KEY = 'test'

BASE_DIR = os.path.dirname(__file__)

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'enhanced_cbv',
    'enhanced_cbv.tests',
    'django_filters',
)

ROOT_URLCONF = 'enhanced_cbv.tests.urls'

DEBUG_PROPAGATE_EXCEPTIONS = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    },
}

MIDDLEWARE_CLASSES = (
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
)

SECRET_KEY = '1'
