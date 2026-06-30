from django.contrib import admin
from .models import SiteConfig, TechStack, Experience, Certification


@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Brand & Identity', {
            'fields': ('brand_name', 'logo_image', 'site_name', 'tagline', 'is_available'),
            'description': 'Upload your logo and set your brand name. Logo appears in the nav and footer.'
        }),
        ('Hero Section', {
            'fields': ('hero_headline', 'hero_subheadline'),
        }),
        ('About Section', {
            'fields': ('profile_image', 'about_text'),
            'description': 'Upload your profile photo. It will appear in the About section.'
        }),
        ('Contact & Links', {
            'fields': ('email', 'github_url', 'linkedin_url', 'twitter_url', 'resume_url'),
        }),
    )


@admin.register(TechStack)
class TechStackAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'proficiency', 'is_featured', 'order']
    list_filter = ['category', 'is_featured']
    list_editable = ['order', 'is_featured', 'proficiency']
    ordering = ['category', 'order']


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['role', 'organization', 'type', 'is_current', 'is_published', 'order']
    list_filter = ['type', 'is_current', 'is_published']
    list_editable = ['order', 'is_published']


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ['name', 'issuer', 'issue_date', 'is_featured', 'order']
    list_editable = ['is_featured', 'order']
