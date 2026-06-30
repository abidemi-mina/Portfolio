from django.contrib import admin
from .models import Project, ProjectHighlight, Category


class ProjectHighlightInline(admin.TabularInline):
    model = ProjectHighlight
    extra = 3


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'description']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'category_names', 'status', 'is_featured', 'is_published', 'order']
    list_filter = ['categories', 'status', 'is_featured', 'is_published']
    list_editable = ['is_featured', 'is_published', 'order']
    prepopulated_fields = {'slug': ('title',)}
    # Both categories and technologies use the horizontal filter widget
    filter_horizontal = ['categories', 'technologies']
    inlines = [ProjectHighlightInline]
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'subtitle', 'description', 'long_description')
        }),
        ('Classification', {
            'fields': ('categories', 'status', 'is_featured', 'is_published', 'order'),
            'description': 'Hold Ctrl (Windows) or Cmd (Mac) to select multiple categories.',
        }),
        ('Technologies', {
            'fields': ('technologies',)
        }),
        ('Media', {
            'fields': ('cover_image', 'thumbnail'),
            'description': (
                'cover_image: large banner shown on the detail page. '
                'thumbnail: small image shown on cards and the homepage list.'
            ),
        }),
        ('Links', {
            'fields': ('github_url', 'live_url', 'case_study_url')
        }),
        ('Metric', {
            'fields': ('metric_label', 'metric_value')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
    )



