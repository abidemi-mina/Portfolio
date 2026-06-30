"""
Custom middleware for SEO and security headers.
"""
from django.conf import settings


class SEOMiddleware:
    """Adds canonical URL and Open Graph meta to response context."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.canonical_url = f"{settings.SITE_URL}{request.path}"
        response = self.get_response(request)
        return response
