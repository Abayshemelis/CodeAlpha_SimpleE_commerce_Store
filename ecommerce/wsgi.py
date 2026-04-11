import os
from django.core.wsgi import get_wsgi_application

# Ensure 'ecommerce.settings' matches your folder name exactly
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')

# This is the variable Django is looking for
application = get_wsgi_application()