'''
Required for inital setup configuration of django
'''
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'thender.settings')
django.setup()
