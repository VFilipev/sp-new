from django.contrib import admin
from .models import Activity


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    """Админка для активностей"""
    list_display = ['title', 'category', 'season', 'is_active', 'order']
    list_filter = ['category', 'season', 'is_active']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['category', 'season', 'order', 'title']

    fieldsets = (
        ('Основная информация', {
            'fields': ('category', 'season', 'title', 'slug', 'description', 'is_active', 'order')
        }),
        ('Медиа', {
            'fields': ('image', 'video')
        }),
        ('SEO', {
            'classes': ('collapse',),
            'fields': (
                'meta_title', 'meta_description', 'meta_keywords',
                'og_title', 'og_description', 'og_image',
                'canonical_url', 'robots_meta'
            )
        }),
    )
