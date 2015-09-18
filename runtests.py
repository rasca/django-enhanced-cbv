#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "enhanced_cbv.tests.test_settings")
    os.environ.setdefault("PYTHONPATH", os.path.dirname(__file__))

    import django
    django.setup()

    from django.core.management import execute_from_command_line
    args = sys.argv[1:] and sys.argv[1:] or ['enhanced_cbv']
    execute_from_command_line(['django-admin.py', 'test'] + args)
