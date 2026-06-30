"""
Projects service layer — all query and filter logic lives here.
category filter now uses categories__slug (M2M lookup).
"""
from django.db.models import Q
from .models import Project, Category


class ProjectQueryService:

    @staticmethod
    def get_published():
        return (Project.objects
                .filter(is_published=True)
                .prefetch_related('categories', 'technologies', 'highlights'))

    @staticmethod
    def get_featured():
        return ProjectQueryService.get_published().filter(is_featured=True).order_by('order')

    @staticmethod
    def get_by_category(slug: str):
        return ProjectQueryService.get_published().filter(categories__slug=slug)

    @staticmethod
    def get_all_with_filters(category_slug: str = '', query: str = ''):
        qs = ProjectQueryService.get_published()
        if category_slug:
            qs = qs.filter(categories__slug=category_slug)
        if query:
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(technologies__name__icontains=query) |
                Q(categories__name__icontains=query)
            ).distinct()
        return qs

    @staticmethod
    def get_detail(slug: str):
        return (Project.objects
                .filter(slug=slug, is_published=True)
                .prefetch_related('categories', 'technologies', 'highlights')
                .first())

    @staticmethod
    def get_all_categories():
        """Returns all categories that have at least one published project."""
        return Category.objects.filter(projects__is_published=True).distinct().order_by('name')
