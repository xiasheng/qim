
import os,sys

os.environ['DJANGO_SETTINGS_MODULE']='im.settings'

path = '/var/www/im'
if path not in sys.path:
        sys.path.append(path)

import django.core.handlers.wsgi

application=django.core.handlers.wsgi.WSGIHandler()

