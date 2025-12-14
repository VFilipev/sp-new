from django.contrib import admin
from django.utils import timezone
from .models import News


@admin.action(description='Опубликовать выбранные новости')
def make_published(modeladmin, request, queryset):
    """Действие для массовой публикации новостей"""
    queryset.update(is_published=True, published_at=timezone.now())


@admin.action(description='Снять с публикации выбранные новости')
def make_unpublished(modeladmin, request, queryset):
    """Действие для массового снятия с публикации"""
    queryset.update(is_published=False)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    """Админка для новостей"""
    list_display = ['title', 'is_published', 'published_at', 'reading_time', 'created_at']
    list_filter = ['is_published', 'published_at', 'created_at']
    search_fields = ['title', 'content', 'short_description', 'excerpt']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'
    ordering = ['-published_at', '-created_at']
    actions = [make_published, make_unpublished]
    readonly_fields = ['reading_time', 'created_at', 'updated_at']

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'short_description', 'excerpt')
        }),
        ('Содержание', {
            'fields': ('content',)
        }),
        ('Медиа', {
            'fields': ('image',)
        }),
        ('Публикация', {
            'fields': ('is_published', 'published_at', 'reading_time')
        }),
        ('Системная информация', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at')
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
