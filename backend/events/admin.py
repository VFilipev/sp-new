from django.contrib import admin
from .models import EventType


@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    """Админка для типов мероприятий"""
    list_display = ['title', 'slug', 'is_active', 'order']
    list_filter = ['is_active']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['order', 'title']

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'description', 'is_active', 'order')
        }),
        ('Медиа', {
            'fields': ('image',)
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
