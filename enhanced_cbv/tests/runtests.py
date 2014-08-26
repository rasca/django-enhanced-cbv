#!/usr/bin/env python

import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'enhanced_cbv.tests.test_settings'
parent = os.path.dirname(os.path.dirname(os.path.dirname(
            os.path.abspath(__file__))))

sys.path.insert(0, parent)

import django
from django.test.runner import DiscoverRunner


def runtests():
    django.setup()
    test_runner = DiscoverRunner(verbosity=1, interactive=True)
    failures = test_runner.run_tests([])
    sys.exit(failures)

if __name__ == '__main__':
    runtests()
