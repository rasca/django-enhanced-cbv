import os
from django.conf import settings


def fetch_resources(uri, rel):
    """
    Callback to allow pisa/reportlab to retrieve Images,Stylesheets, etc.
    `uri` is the href attribute from the html link element.
    `rel` gives a relative path, but it's not used here.
    """
    path = os.path.join(settings.STATIC_ROOT, uri.replace(settings.STATIC_URL, ""))
    return path

