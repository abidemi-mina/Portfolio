from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from projects.models import Project
from blog.models import Post

class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = 'weekly'

    def items(self):
        return ['core:home']

    def location(self, item):
        return reverse(item)

class ProjectSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.8

    def items(self):
        return Project.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at

class BlogSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return Post.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at
