import os

BASE_DIR = os.path.dirname(__file__)

INSTALLED_APPS = (
    'enhanced_cbv',
    'enhanced_cbv.tests',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    },
}

