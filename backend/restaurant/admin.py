from django.contrib import admin
from django.utils.html import format_html
from solo.admin import SingletonModelAdmin
from .models import Restaurant, RestaurantImage, MealType, RestaurantBenefit


class RestaurantImageInline(admin.TabularInline):
    """Inline для изображений ресторана"""
    model = RestaurantImage
    extra = 1
    fields = ['image', 'alt_text', 'order']
    ordering = ['order']


class RestaurantBenefitInline(admin.TabularInline):
    """Inline для преимуществ ресторана"""
    model = RestaurantBenefit
    extra = 1
    fields = ['text', 'order']
    ordering = ['order']


@admin.register(Restaurant)
class RestaurantAdmin(SingletonModelAdmin):
    """Админка для ресторана"""
    inlines = [RestaurantImageInline, RestaurantBenefitInline]

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'is_active')
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


@admin.register(RestaurantImage)
class RestaurantImageAdmin(admin.ModelAdmin):
    """Админка для изображений ресторана"""
    list_display = ['restaurant', 'alt_text', 'order', 'image_preview']
    list_filter = ['restaurant']
    search_fields = ['alt_text']
    ordering = ['restaurant', 'order', 'id']

    def image_preview(self, obj):
        """Превью изображения"""
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.image.url)
        return '-'
    image_preview.short_description = 'Превью'


@admin.register(MealType)
class MealTypeAdmin(admin.ModelAdmin):
    """Админка для типов приема пищи"""
    list_display = ['name', 'icon_name', 'time_start', 'order']
    search_fields = ['name', 'description']
    ordering = ['order', 'name']

    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'icon_name', 'description', 'time_start', 'order')
        }),
    )


@admin.register(RestaurantBenefit)
class RestaurantBenefitAdmin(admin.ModelAdmin):
    """Админка для преимуществ ресторана"""
    list_display = ['restaurant', 'text', 'order']
    list_filter = ['restaurant']
    search_fields = ['text']
    ordering = ['restaurant', 'order', 'id']
