"""
Global context processors — inject site-wide data into every template.
"""
from django.conf import settings
from .models import SiteConfig


def site_context(request):
    """Makes site config and settings available in every template."""
    config = SiteConfig.get_config()
    return {
        'site_config': config,
        'site_name': settings.SITE_NAME,
        'site_url': settings.SITE_URL,
        'debug': settings.DEBUG,
    }
