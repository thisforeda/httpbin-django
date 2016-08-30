
from django.conf.urls import url

from .views import httpbin_handler

urlpatterns = [
    # /[GROUP]?arguments
    
    url(r'([a-zA-Z0-9_-]+)?$', httpbin_handler),
]
