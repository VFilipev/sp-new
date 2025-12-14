from django.contrib import admin
from django.utils.html import format_html
from .models import LodgeType, Lodge, LodgeImage


class LodgeImageInline(admin.TabularInline):
    """Inline для изображений размещения"""
    model = LodgeImage
    extra = 1
    fields = ['image', 'alt_text', 'order']
    ordering = ['order']


@admin.register(LodgeType)
class LodgeTypeAdmin(admin.ModelAdmin):
    """Админка для типов размещения"""
    list_display = ['name', 'slug', 'is_active', 'order']
    list_filter = ['is_active']
    search_fields = ['name', 'description', 'subtitle']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order', 'name']

    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'slug', 'subtitle', 'description', 'is_active', 'order')
        }),
        ('Медиа', {
            'fields': ('hero_image',)
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


@admin.register(Lodge)
class LodgeAdmin(admin.ModelAdmin):
    """Админка для размещений"""
    list_display = ['name', 'lodge_type', 'capacity', 'area', 'price_from', 'is_active', 'order']
    list_filter = ['lodge_type', 'is_active']
    search_fields = ['name', 'description', 'short_description', 'location_description']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [LodgeImageInline]
    ordering = ['order', 'name']

    fieldsets = (
        ('Основная информация', {
            'fields': ('lodge_type', 'name', 'slug', 'description', 'short_description', 'is_active', 'order')
        }),
        ('Характеристики', {
            'fields': ('capacity', 'area', 'price_from', 'location_description')
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


@admin.register(LodgeImage)
class LodgeImageAdmin(admin.ModelAdmin):
    """Админка для изображений размещения"""
    list_display = ['lodge', 'alt_text', 'order', 'image_preview']
    list_filter = ['lodge']
    search_fields = ['lodge__name', 'alt_text']
    ordering = ['lodge', 'order', 'id']

    def image_preview(self, obj):
        """Превью изображения"""
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.image.url)
        return '-'
    image_preview.short_description = 'Превью'
