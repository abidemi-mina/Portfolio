"""
Core views — thin view layer that delegates to the service layer.
Views handle HTTP; services handle logic. (Single Responsibility)
"""
from django.views.generic import TemplateView
from django.http import JsonResponse
from .services import HomePageService


class HomeView(TemplateView):
    """
    Portfolio homepage. Uses HomePageService to assemble all context data.
    All business logic lives in the service, keeping this view thin.
    """
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(HomePageService.get_context())
        return context


class HealthCheckView(TemplateView):
    """Simple health-check endpoint for deployment monitoring."""
    def get(self, request, *args, **kwargs):
        return JsonResponse({'status': 'ok', 'service': 'portfolio-platform'})
