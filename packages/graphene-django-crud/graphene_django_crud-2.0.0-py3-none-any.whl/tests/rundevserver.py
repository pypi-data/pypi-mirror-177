#!/usr/bin/env python
import os
import sys
import django
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

if __name__ == '__main__':
    os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.test_settings'
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(["./manage.py", "runserver"] + sys.argv[1:])