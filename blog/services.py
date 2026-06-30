import markdown as md
from django.utils.safestring import mark_safe
from .models import Post, Tag, ExternalLink, Like


class PostService:

    @staticmethod
    def get_published():
        return (Post.objects
                .filter(is_published=True)
                .prefetch_related('tags')
                .order_by('-created_at'))

    @staticmethod
    def get_detail(slug):
        post = (Post.objects
                .filter(slug=slug, is_published=True)
                .prefetch_related('tags', 'comments', 'likes')
                .first())
        if post:
            post.increment_views()
        return post

    @staticmethod
    def get_rendered_body(post):
        return mark_safe(md.markdown(
            post.body,
            extensions=['fenced_code', 'tables', 'toc']
        ))

    @staticmethod
    def get_approved_comments(post):
        return post.comments.filter(approved=True).order_by('created_at')

    @staticmethod
    def get_client_ip(request):
        x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
        return x_forwarded.split(',')[0] if x_forwarded else request.META.get('REMOTE_ADDR', '0.0.0.0')

    @staticmethod
    def has_liked(post, ip):
        return Like.objects.filter(post=post, ip_address=ip).exists()

    @staticmethod
    def toggle_like(post, ip):
        """Toggle like. Returns (liked: bool, count: int)."""
        like, created = Like.objects.get_or_create(post=post, ip_address=ip)
        if not created:
            like.delete()
            return False, post.like_count()
        return True, post.like_count()


class ExternalLinkService:
    @staticmethod
    def get_active():
        return ExternalLink.objects.filter(is_active=True).order_by('order', '-published_date')
