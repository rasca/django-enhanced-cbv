import os

BASE_DIR = os.path.dirname(__file__)

INSTALLED_APPS = (
    'enhanced_cbv',
    'enhanced_cbv.tests',
)

ROOT_URLCONF = 'enhanced_cbv.tests.urls'

DEBUG_PROPAGATE_EXCEPTIONS = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    },
}

