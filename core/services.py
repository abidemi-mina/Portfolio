"""
Core service layer — business logic separated from views (SRP).
Services handle data retrieval, aggregation, and cross-cutting concerns.
"""
from django.conf import settings
from .models import SiteConfig, TechStack, Experience, Certification
from projects.models import Project
from projects.services import ProjectQueryService
from blog.models import Post


class SiteConfigService:
    """Provides access to dynamic site configuration."""

    @staticmethod
    def get_config():
        return SiteConfig.get_config()


class HomePageService:
    """
    Orchestrates all data needed to render the homepage.
    Single responsibility: assemble the home page context.
    """

    @staticmethod
    def get_context() -> dict:
        config = SiteConfig.get_config()
        featured_projects = ProjectQueryService.get_featured()[:6]

        tech_stack = TechStack.objects.filter(is_featured=True).order_by('category', 'order')
        grouped_tech = {}
        for tech in tech_stack:
            cat = tech.get_category_display()
            grouped_tech.setdefault(cat, []).append(tech)

        recent_posts = Post.objects.filter(is_published=True).order_by('-created_at')[:3]
        certifications = Certification.objects.filter(is_featured=True).order_by('order', '-issue_date')
        experiences = Experience.objects.filter(is_published=True).order_by('order')

        build_categories = [
            {
                'title': 'AI-Powered Applications',
                'description': 'Intelligent systems that leverage AI, machine learning, and LLMs to automate processes and generate insights.',
                'icon': 'ai',
                'color': 'purple',
            },
            {
                'title': 'Backend Systems',
                'description': 'Scalable APIs, databases, and server-side applications designed for reliability and performance.',
                'icon': 'backend',
                'color': 'blue',
            },
            {
                'title': 'Workflow Automation',
                'description': 'Automated business processes that eliminate manual effort and improve operational efficiency.',
                'icon': 'automation',
                'color': 'indigo',
            },
            {
                'title': 'Business Intelligence',
                'description': 'Data platforms that transform raw information into decisions executives can act on.',
                'icon': 'bi',
                'color': 'violet',
            },
            {
                'title': 'Enterprise Software',
                'description': 'Systems supporting business operations, resource management, and organizational workflows.',
                'icon': 'enterprise',
                'color': 'fuchsia',
            },
        ]

        return {
            'config': config,
            'featured_projects': featured_projects,
            'grouped_tech': grouped_tech,
            'recent_posts': recent_posts,
            'certifications': certifications,
            'experiences': experiences,
            'build_categories': build_categories,
            'page_title': f'{config.site_name} — {config.tagline}',
            'meta_description': settings.SITE_DESCRIPTION,
        }
