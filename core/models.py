"""
Core models — abstract base classes and site-wide content models.
All models in the platform inherit from TimeStampedModel for audit trails.
"""
from django.db import models
from django.utils.text import slugify


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SluggedModel(TimeStampedModel):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class PublishableModel(SluggedModel):
    is_published = models.BooleanField(default=False)
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.TextField(max_length=160, blank=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']

    def get_meta_title(self):
        return self.meta_title or self.title

    def get_meta_description(self):
        return self.meta_description


class SiteConfig(TimeStampedModel):
    """
    Singleton. Controls every piece of dynamic content across the site.
    brand_name drives the logo wordmark — change it here, updates everywhere.
    """
    # Brand identity
    brand_name = models.CharField(max_length=60, default='MinaDXplorer',
        help_text='Wordmark shown in nav and footer alongside the logo')
    logo_image = models.ImageField(upload_to='brand/', blank=True, null=True,
        help_text='Your logo image. If blank the default SVG mark is used.')
    site_name = models.CharField(max_length=100, default='Dev Mina')
    tagline = models.CharField(max_length=200, default='Software Engineer & AI Systems Developer')

    # Hero
    hero_headline = models.CharField(max_length=300, default='I build software that makes businesses smarter.')
    hero_subheadline = models.TextField(blank=True)

    # About
    about_text = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profile/', blank=True, null=True,
        help_text='Profile photo shown in the About section.')

    # CTA
    resume_url = models.URLField(blank=True)
    is_available = models.BooleanField(default=True, help_text='Show "Open to work" badge')

    # Social links
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    email = models.EmailField(blank=True)

    class Meta:
        verbose_name = 'Site Configuration'
        verbose_name_plural = 'Site Configuration'

    def __str__(self):
        return 'Site Configuration'

    @classmethod
    def get_config(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)


class Experience(TimeStampedModel):
    """
    Work, education, and volunteer history — rendered as a timeline on the homepage.
    Lives in core because it has no views, URLs, or independent routing of its own.
    """
    TYPE_CHOICES = [
        ('work', 'Work Experience'),
        ('education', 'Education'),
        ('volunteer', 'Volunteer / Leadership'),
    ]
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='work')
    role = models.CharField(max_length=200)
    organization = models.CharField(max_length=200)
    location = models.CharField(max_length=100, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True, help_text='Leave blank if current')
    is_current = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    is_published = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-start_date']
        verbose_name = 'Experience'
        verbose_name_plural = 'Experience'

    def __str__(self):
        return f'{self.role} @ {self.organization}'

    def date_range(self):
        end = 'Present' if self.is_current else (self.end_date.strftime('%b %Y') if self.end_date else '')
        return f"{self.start_date.strftime('%b %Y')} \u2014 {end}"


class Certification(TimeStampedModel):
    """
    Professional credentials and certifications — displayed as cards on the homepage.
    Lives in core because it has no views, URLs, or independent routing of its own.
    """
    name = models.CharField(max_length=200)
    issuer = models.CharField(max_length=200)
    credential_id = models.CharField(max_length=100, blank=True)
    issue_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    credential_url = models.URLField(blank=True)
    badge_image = models.ImageField(upload_to='certifications/', blank=True, null=True)
    is_featured = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-issue_date']
        verbose_name = 'Certification'
        verbose_name_plural = 'Certifications'

    def __str__(self):
        return f'{self.name} \u2014 {self.issuer}'


class TechStack(TimeStampedModel):
    CATEGORY_CHOICES = [
        ('language', 'Languages'),
        ('framework', 'Frameworks'),
        ('database', 'Databases'),
        ('ai_ml', 'AI & Machine Learning'),
        ('automation', 'Automation'),
        ('tool', 'Tools & DevOps'),
        ('cloud', 'Cloud & Infrastructure'),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    icon_class = models.CharField(max_length=100, blank=True)
    proficiency = models.PositiveIntegerField(default=80)
    order = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['category', 'order', 'name']
        verbose_name = 'Technology'
        verbose_name_plural = 'Technologies'

    def __str__(self):
        return f'{self.name} ({self.get_category_display()})'
