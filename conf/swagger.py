from django.urls import path

from rest_framework.permissions import AllowAny
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from conf.settings import API_VERSION, BACKEND_DOMAIN


def get_dynamic_description(domain) -> str:
    """
    Get the API description based on the subdomain.
    """
    host = domain.split(':')[0]
    subdomain = host.split('.')[0]
    if subdomain == "test":
        return "Development API"
    elif subdomain == "api":
        return "Production API"
    else:
        return "Generic API"



# Add `never_cache` to prevent caching of the schema view
urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
