from django.db import models
from core.models import PublishableModel, TimeStampedModel


class Tag(TimeStampedModel):
    name = models.CharField(max_length=60, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Post(PublishableModel):
    excerpt    = models.TextField(max_length=300, blank=True)
    body       = models.TextField(help_text='Markdown supported')
    cover_image = models.ImageField(
        upload_to='blog/covers/', blank=True, null=True,
        help_text='Displayed as a full-width banner on the post page and as a card thumbnail on the list page.'
    )
    tags       = models.ManyToManyField(Tag, related_name='posts', blank=True)
    read_time  = models.PositiveIntegerField(default=5, help_text='Estimated minutes')
    views_count = models.PositiveIntegerField(default=0)

    class Meta(PublishableModel.Meta):
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('blog:detail', kwargs={'slug': self.slug})

    def increment_views(self):
        self.views_count += 1
        self.save(update_fields=['views_count'])

    def like_count(self):
        return self.likes.count()

    def comment_count(self):
        return self.comments.filter(approved=True).count()


class Like(TimeStampedModel):
    """
    One like per IP address per post.
    No user auth required — tracked by IP.
    """
    post       = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    ip_address = models.GenericIPAddressField()

    class Meta:
        unique_together = ('post', 'ip_address')
        verbose_name = 'Like'

    def __str__(self):
        return f'Like on "{self.post.title}" from {self.ip_address}'


class Comment(TimeStampedModel):
    """
    Reader comment on a post. Requires admin approval before showing.
    """
    post     = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name     = models.CharField(max_length=100)
    email    = models.EmailField(help_text='Never published — for moderation only.')
    body     = models.TextField()
    approved = models.BooleanField(default=False, help_text='Only approved comments are shown to readers.')

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Comment'

    def __str__(self):
        return f'{self.name} on "{self.post.title}"'


class ExternalLink(TimeStampedModel):
    PLATFORM_CHOICES = [
        ('linkedin', 'LinkedIn'), ('medium', 'Medium'), ('devto', 'Dev.to'),
        ('hashnode', 'Hashnode'), ('twitter', 'X / Twitter'),
        ('youtube', 'YouTube'),  ('podcast', 'Podcast'), ('other', 'Other'),
    ]
    title          = models.CharField(max_length=200)
    description    = models.TextField(max_length=300, blank=True)
    url            = models.URLField()
    platform       = models.CharField(max_length=20, choices=PLATFORM_CHOICES, default='linkedin')
    published_date = models.DateField(null=True, blank=True)
    is_active      = models.BooleanField(default=True)
    order          = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-published_date']
        verbose_name = 'External Link'
        verbose_name_plural = 'External Links'

    def __str__(self):
        return f'{self.title} ({self.get_platform_display()})'
