from django.contrib import admin
from .models import Post, Tag, ExternalLink, Comment, Like


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display  = ['title', 'is_published', 'read_time', 'views_count', 'like_count', 'comment_count', 'created_at']
    list_editable = ['is_published']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal   = ['tags']

    def like_count(self, obj):
        return obj.like_count()
    like_count.short_description = 'Likes'

    def comment_count(self, obj):
        return obj.comment_count()
    comment_count.short_description = 'Comments'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display   = ['name', 'post', 'approved', 'created_at']
    list_filter    = ['approved', 'post']
    list_editable  = ['approved']
    actions        = ['approve_comments']
    readonly_fields = ['name', 'email', 'body', 'post', 'created_at']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)
    approve_comments.short_description = 'Approve selected comments'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ExternalLink)
class ExternalLinkAdmin(admin.ModelAdmin):
    list_display  = ['title', 'platform', 'published_date', 'is_active', 'order']
    list_filter   = ['platform', 'is_active']
    list_editable = ['is_active', 'order']


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['post', 'ip_address', 'created_at']
    list_filter  = ['post']
