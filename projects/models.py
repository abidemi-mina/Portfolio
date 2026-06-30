"""
Projects app models.
Category is now a proper model with M2M — a project can belong to
multiple categories (e.g. an "AI + Backend" system).
"""
from django.db import models
from core.models import PublishableModel, TimeStampedModel,TechStack




class Category(TimeStampedModel):
    """
    Project category — now a standalone model so a project can belong
    to more than one category. e.g. GrowthPath is both AI and Automation.
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Project(PublishableModel):
    """
    Core project entity. Inherits slug, timestamps, publish flag, and SEO fields.
    categories is now M2M — pick as many as apply.
    """
    STATUS_CHOICES = [
        ('production', 'Production'),
        ('development', 'In Development'),
        ('research', 'Research'),
        ('archived', 'Archived'),
    ]

    subtitle = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    long_description = models.TextField(blank=True, help_text='Markdown supported')

    # M2M — a project can have multiple categories
    categories = models.ManyToManyField(
        Category,
        related_name='projects',
        blank=True,
        help_text='Pick all that apply. Hold Ctrl / Cmd to select multiple.'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='production')
    technologies = models.ManyToManyField(TechStack, related_name='projects', blank=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0, help_text='Lower = shown first')

    # Media — upload in admin; displayed on cards and detail page
    cover_image = models.ImageField(
        upload_to='projects/covers/',
        blank=True, null=True,
        help_text='Large image shown at the top of the project detail page.'
    )
    thumbnail = models.ImageField(
        upload_to='projects/thumbnails/',
        blank=True, null=True,
        help_text='Small image shown on project cards and the homepage list.'
    )

    # Links
    github_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)
    case_study_url = models.URLField(blank=True)

    # Metrics
    metric_label = models.CharField(max_length=60, blank=True, help_text='e.g. "Recovery rate"')
    metric_value = models.CharField(max_length=40, blank=True, help_text='e.g. "98.1%"')

    class Meta(PublishableModel.Meta):
        ordering = ['order', '-created_at']
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('projects:detail', kwargs={'slug': self.slug})

    def category_names(self):
        """Returns comma-separated category names for admin list_display."""
        return ', '.join(self.categories.values_list('name', flat=True))
    category_names.short_description = 'Categories'

    def primary_image(self):
        """Returns thumbnail if set, else cover_image, else None."""
        return self.thumbnail or self.cover_image or None


class ProjectHighlight(TimeStampedModel):
    """Bullet-point highlights for a project."""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='highlights')
    text = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.project.title} — {self.text}'
