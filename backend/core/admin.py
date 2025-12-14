from django.contrib import admin
from django.core.exceptions import ValidationError
from django.utils.html import format_html
from solo.admin import SingletonModelAdmin
from .models import SiteSettings, Statistic, GalleryImage, HeroSection, HeroImage


@admin.register(SiteSettings)
class SiteSettingsAdmin(SingletonModelAdmin):
    """Админка для настроек сайта"""
    fieldsets = (
        ('Основная информация', {
            'fields': ('site_name', 'logo', 'phone_primary', 'phone_secondary', 'email', 'address')
        }),
        ('Социальные сети', {
            'fields': ('telegram_url', 'vk_url')
        }),
        ('Реестр', {
            'fields': ('registry_number', 'registry_url')
        }),
        ('Главная страница', {
            'fields': ('hero_image', 'hero_title', 'hero_subtitle')
        }),
        ('План базы', {
            'fields': ('base_plan_image', 'base_plan_description')
        }),
        ('Логотипы', {
            'fields': ('national_projects_logo',)
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


@admin.register(Statistic)
class StatisticAdmin(admin.ModelAdmin):
    """Админка для статистики"""
    list_display = ['number', 'label', 'is_active', 'order']
    list_filter = ['is_active']
    search_fields = ['number', 'label', 'description']
    ordering = ['order', 'id']

    fieldsets = (
        ('Основная информация', {
            'fields': ('number', 'label', 'description', 'is_active', 'order')
        }),
    )


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    """Админка для изображений галереи"""
    list_display = ['alt_text', 'position', 'is_active', 'order', 'image_preview']
    list_filter = ['position', 'is_active']
    search_fields = ['alt_text']
    ordering = ['position', 'order', 'id']

    fieldsets = (
        ('Основная информация', {
            'fields': ('image', 'alt_text', 'position', 'is_active', 'order')
        }),
    )

    def image_preview(self, obj):
        """Превью изображения"""
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.image.url)
        return '-'
    image_preview.short_description = 'Превью'


class HeroImageInline(admin.TabularInline):
    """Inline для изображений Hero секции"""
    model = HeroImage
    extra = 1
    fields = ['image', 'alt_text', 'order', 'is_active', 'transition_duration']
    ordering = ['order']


@admin.action(description='Активировать выбранные Hero секции')
def activate_hero(modeladmin, request, queryset):
    """Действие для активации Hero секций"""
    # Деактивируем все остальные
    HeroSection.objects.filter(is_active=True).update(is_active=False)
    # Активируем выбранные
    queryset.update(is_active=True)


@admin.action(description='Деактивировать выбранные Hero секции')
def deactivate_hero(modeladmin, request, queryset):
    """Действие для деактивации Hero секций"""
    queryset.update(is_active=False)


@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    """Админка для Hero секции"""
    list_display = ['title', 'display_type', 'is_active', 'order']
    list_filter = ['display_type', 'is_active']
    search_fields = ['title', 'subtitle']
    inlines = [HeroImageInline]
    ordering = ['order', 'id']
    actions = [activate_hero, deactivate_hero]

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'subtitle', 'display_type', 'is_active', 'order')
        }),
        ('Медиа', {
            'fields': ('preview_image', 'promo_video', 'video_poster')
        }),
        ('Настройки видео', {
            'classes': ('collapse',),
            'fields': ('autoplay_video', 'loop_video', 'mute_video')
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

    def save_model(self, request, obj, form, change):
        """Переопределяем save для валидации Singleton"""
        try:
            super().save_model(request, obj, form, change)
        except ValidationError as e:
            self.message_user(request, str(e), level='error')
            raise


@admin.register(HeroImage)
class HeroImageAdmin(admin.ModelAdmin):
    """Админка для изображений Hero секции"""
    list_display = ['hero_section', 'alt_text', 'is_active', 'order', 'transition_duration', 'image_preview']
    list_filter = ['hero_section', 'is_active']
    search_fields = ['alt_text', 'hero_section__title']
    ordering = ['hero_section', 'order', 'id']

    def image_preview(self, obj):
        """Превью изображения"""
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.image.url)
        return '-'
    image_preview.short_description = 'Превью'
