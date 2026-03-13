from rest_framework import serializers
from .models import Statistic, GalleryImage, HeroSection, HeroImage, SiteSettings
from .serializer_mixins import ImageVariantsMixin


class StatisticSerializer(serializers.ModelSerializer):
    """Сериализатор для статистики"""
    class Meta:
        model = Statistic
        fields = ['id', 'number', 'label', 'description', 'is_active', 'order']


class GalleryImageSerializer(ImageVariantsMixin, serializers.ModelSerializer):
    """Сериализатор для изображений галереи"""
    image_url = serializers.SerializerMethodField()
    image_webp_url = serializers.SerializerMethodField()
    image_placeholder_url = serializers.SerializerMethodField()
    image_variants = serializers.SerializerMethodField()
    position_display = serializers.CharField(source='get_position_display', read_only=True)
    column_display = serializers.CharField(source='get_column_display', read_only=True)

    class Meta:
        model = GalleryImage
        fields = [
            'id', 'image_url', 'image_webp_url', 'image_placeholder_url',
            'image_variants', 'alt_text',
            'position', 'position_display', 'column', 'column_display', 'order', 'is_active'
        ]

    def get_image_url(self, obj):
        """Возвращает URL оригинального изображения"""
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

    def get_image_webp_url(self, obj):
        """Возвращает URL WebP изображения с fallback на оригинал"""
        if not obj.image:
            return None

        request = self.context.get('request')
        try:
            # Пытаемся получить WebP версию (может быть сгенерирована на лету)
            if hasattr(obj, 'image_webp') and obj.image_webp:
                webp_url = obj.image_webp.url
                if request:
                    return request.build_absolute_uri(webp_url)
                return webp_url
        except Exception:
            # Если WebP не может быть получен, используем оригинал
            pass

        # Fallback на оригинальное изображение
        return self.get_image_url(obj)

    def get_image_placeholder_url(self, obj):
        """Возвращает URL placeholder"""
        if not obj.image:
            return None

        request = self.context.get('request')
        try:
            placeholder_field = getattr(obj, 'gallery_placeholder_webp', None)
            if placeholder_field:
                url = placeholder_field.url
                if request:
                    url = request.build_absolute_uri(url)
                return url
        except Exception:
            pass

        return None

    def get_image_variants(self, obj):
        """Возвращает варианты размеров изображения"""
        variant_fields = {
            'large': 'gallery_large_webp',
            'medium': 'gallery_medium_webp',
            'small': 'gallery_small_webp',
        }
        return super().get_image_variants(obj, variant_fields, 'image')


class HeroImageSerializer(ImageVariantsMixin, serializers.ModelSerializer):
    """Сериализатор для изображений Hero секции"""
    image_url = serializers.SerializerMethodField()
    image_webp_url = serializers.SerializerMethodField()
    image_placeholder_url = serializers.SerializerMethodField()
    image_variants = serializers.SerializerMethodField()

    class Meta:
        model = HeroImage
        fields = [
            'id', 'image_url', 'image_webp_url', 'image_placeholder_url',
            'image_variants', 'alt_text',
            'order', 'is_active', 'transition_duration'
        ]

    def get_image_url(self, obj):
        """Возвращает URL оригинального изображения"""
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

    def get_image_webp_url(self, obj):
        """Возвращает URL WebP изображения с fallback на оригинал"""
        if obj.image:
            request = self.context.get('request')
            try:
                # Используем hero_full_webp как основной вариант
                webp_url = obj.hero_full_webp.url if hasattr(obj, 'hero_full_webp') and obj.hero_full_webp else None
                if not webp_url:
                    webp_url = obj.image_webp.url if hasattr(obj, 'image_webp') and obj.image_webp else None
                if webp_url:
                    if request:
                        return request.build_absolute_uri(webp_url)
                    return webp_url
            except:
                pass
            # Fallback на оригинальное изображение
            return self.get_image_url(obj)
        return None

    def get_image_placeholder_url(self, obj):
        """Возвращает URL placeholder"""
        return super().get_image_placeholder_url(obj, 'hero_placeholder_webp', 'image')

    def get_image_variants(self, obj):
        """Возвращает варианты размеров изображения"""
        variant_fields = {
            'full': 'hero_full_webp',
            'thumb': 'hero_thumb_webp',
        }
        return super().get_image_variants(obj, variant_fields, 'image')


class HeroSectionSerializer(ImageVariantsMixin, serializers.ModelSerializer):
    """Сериализатор для Hero секции"""
    images = HeroImageSerializer(many=True, read_only=True)
    preview_image_url = serializers.SerializerMethodField()
    preview_image_webp_url = serializers.SerializerMethodField()
    preview_image_placeholder_url = serializers.SerializerMethodField()
    preview_image_variants = serializers.SerializerMethodField()
    video_poster_url = serializers.SerializerMethodField()
    promo_video_url = serializers.SerializerMethodField()
    display_type_display = serializers.CharField(source='get_display_type_display', read_only=True)
    seo_fields = serializers.SerializerMethodField()

    class Meta:
        model = HeroSection
        fields = [
            'id', 'title', 'subtitle', 'preview_image_url', 'preview_image_webp_url',
            'preview_image_placeholder_url',
            'preview_image_variants', 'promo_video_url', 'video_poster_url',
            'display_type', 'display_type_display',
            'autoplay_video', 'loop_video', 'mute_video', 'is_active', 'order',
            'images', 'seo_fields'
        ]

    def get_preview_image_url(self, obj):
        """Возвращает URL оригинального превью изображения"""
        if obj.preview_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.preview_image.url)
            return obj.preview_image.url
        return None

    def get_preview_image_webp_url(self, obj):
        """Возвращает URL WebP превью изображения с fallback на оригинал"""
        if obj.preview_image:
            request = self.context.get('request')
            try:
                # Используем preview_image_hero_full_webp как основной вариант
                webp_url = obj.preview_image_hero_full_webp.url if hasattr(obj, 'preview_image_hero_full_webp') and obj.preview_image_hero_full_webp else None
                if not webp_url:
                    webp_url = obj.preview_image_webp.url if hasattr(obj, 'preview_image_webp') and obj.preview_image_webp else None
                if webp_url:
                    if request:
                        return request.build_absolute_uri(webp_url)
                    return webp_url
            except:
                pass
            # Fallback на оригинальное изображение
            return self.get_preview_image_url(obj)
        return None

    def get_preview_image_placeholder_url(self, obj):
        """Возвращает URL placeholder для preview_image"""
        if not obj.preview_image:
            return None
        request = self.context.get('request')
        try:
            placeholder_field = obj.preview_image_hero_placeholder_webp if hasattr(obj, 'preview_image_hero_placeholder_webp') else None
            if placeholder_field and hasattr(placeholder_field, 'url'):
                url = placeholder_field.url
                if request:
                    url = request.build_absolute_uri(url)
                return url
        except:
            pass
        return None

    def get_preview_image_variants(self, obj):
        """Возвращает варианты размеров preview_image"""
        if not obj.preview_image:
            return None
        variant_fields = {
            'full': 'preview_image_hero_full_webp',
            'thumb': 'preview_image_hero_thumb_webp',
        }
        return super().get_image_variants(obj, variant_fields, 'preview_image')

    def get_video_poster_url(self, obj):
        """Возвращает URL постера видео"""
        if obj.video_poster:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.video_poster.url)
            return obj.video_poster.url
        return None

    def get_promo_video_url(self, obj):
        """Возвращает URL промо видео"""
        if obj.promo_video:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.promo_video.url)
            return obj.promo_video.url
        return None

    def get_seo_fields(self, obj):
        """Возвращает SEO поля"""
        return {
            'meta_title': obj.meta_title,
            'meta_description': obj.meta_description,
            'meta_keywords': obj.meta_keywords,
            'og_title': obj.og_title,
            'og_description': obj.og_description,
            'og_image': obj.og_image.url if obj.og_image else None,
            'canonical_url': obj.canonical_url,
            'robots_meta': obj.robots_meta,
        }


class HeroSectionPatchSerializer(serializers.ModelSerializer):
    """Сериализатор для редактирования текстов Hero секции."""
    class Meta:
        model = HeroSection
        fields = ['title', 'subtitle']


class StatisticPatchSerializer(serializers.ModelSerializer):
    """Сериализатор для редактирования карточек статистики."""
    class Meta:
        model = Statistic
        fields = ['number', 'label', 'description']


class GalleryImageUploadSerializer(serializers.ModelSerializer):
    """Создание изображения галереи через edit API."""
    class Meta:
        model = GalleryImage
        fields = ['id', 'image', 'alt_text', 'position', 'column', 'order', 'is_active']
        read_only_fields = ['id']

    def validate(self, attrs):
        position = attrs.get('position', 'main')
        column = attrs.get('column')
        if position == 'main' and not column:
            raise serializers.ValidationError({
                'column': 'Для позиции "main" необходимо указать column.'
            })
        return attrs


class GalleryLayoutItemSerializer(serializers.Serializer):
    """Одна запись раскладки галереи для bulk-обновления."""
    target_id = serializers.IntegerField(min_value=1)
    source_image_id = serializers.IntegerField(min_value=1, required=False, allow_null=True)
    position = serializers.ChoiceField(choices=GalleryImage.POSITION_CHOICES)
    column = serializers.ChoiceField(
        choices=GalleryImage.COLUMN_CHOICES,
        required=False,
        allow_null=True
    )
    order = serializers.IntegerField(min_value=0)
    alt_text = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    is_active = serializers.BooleanField(required=False, default=True)

    def validate(self, attrs):
        if attrs.get('position') == 'main' and not attrs.get('column'):
            raise serializers.ValidationError({
                'column': 'Для позиции "main" необходимо указать column.'
            })
        return attrs


class GalleryLayoutApplySerializer(serializers.Serializer):
    """Bulk payload для применения раскладки галереи."""
    items = GalleryLayoutItemSerializer(many=True)

    def validate_items(self, items):
        if not items:
            raise serializers.ValidationError('Список items не должен быть пустым.')

        target_ids = set()
        source_ids = set()
        active_slots = set()

        for item in items:
            target_id = item['target_id']
            source_id = item.get('source_image_id') or target_id
            slot_key = (
                item['position'],
                item.get('column'),
                item['order'],
            )

            if target_id in target_ids:
                raise serializers.ValidationError(
                    f'Дублирующийся target_id={target_id} в payload.'
                )
            target_ids.add(target_id)

            if source_id in source_ids:
                raise serializers.ValidationError(
                    f'Один и тот же source_image_id={source_id} указан несколько раз.'
                )
            source_ids.add(source_id)

            if item.get('is_active', True):
                if slot_key in active_slots:
                    raise serializers.ValidationError(
                        'Конфликт активных позиций: повторяются position/column/order.'
                    )
                active_slots.add(slot_key)

        return items


class SiteSettingsSerializer(ImageVariantsMixin, serializers.ModelSerializer):
    """Сериализатор для настроек сайта"""
    logo_url = serializers.SerializerMethodField()
    national_projects_logo_url = serializers.SerializerMethodField()
    hero_image_url = serializers.SerializerMethodField()
    hero_image_variants = serializers.SerializerMethodField()
    hero_image_placeholder_url = serializers.SerializerMethodField()
    base_plan_image_url = serializers.SerializerMethodField()
    base_plan_image_variants = serializers.SerializerMethodField()
    base_plan_image_placeholder_url = serializers.SerializerMethodField()
    seo_fields = serializers.SerializerMethodField()

    class Meta:
        model = SiteSettings
        fields = [
            'id', 'site_name', 'logo_url', 'phone_primary', 'phone_secondary',
            'email', 'address', 'telegram_url', 'vk_url',
            'registry_number', 'registry_url',
            'national_projects_logo_url', 'hero_image_url',
            'hero_image_variants', 'hero_image_placeholder_url',
            'hero_title', 'hero_subtitle',
            'base_plan_image_url', 'base_plan_image_variants',
            'base_plan_image_placeholder_url',
            'base_plan_description', 'seo_fields'
        ]

    def get_logo_url(self, obj):
        """Возвращает URL логотипа"""
        if obj.logo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.logo.url)
            return obj.logo.url
        return None

    def get_national_projects_logo_url(self, obj):
        """Возвращает URL логотипа национальных проектов"""
        if obj.national_projects_logo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.national_projects_logo.url)
            return obj.national_projects_logo.url
        return None

    def get_hero_image_url(self, obj):
        """Возвращает URL главного изображения"""
        if obj.hero_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.hero_image.url)
            return obj.hero_image.url
        return None

    def get_hero_image_variants(self, obj):
        """Возвращает варианты размеров hero_image"""
        if not obj.hero_image:
            return None
        variant_fields = {
            'full': 'hero_image_full_webp',
            'thumb': 'hero_image_thumb_webp',
        }
        return super().get_image_variants(obj, variant_fields, 'hero_image')

    def get_hero_image_placeholder_url(self, obj):
        """Возвращает URL placeholder для hero_image"""
        return super().get_image_placeholder_url(obj, 'hero_image_placeholder_webp', 'hero_image')

    def get_base_plan_image_url(self, obj):
        """Возвращает URL изображения плана базы"""
        if obj.base_plan_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.base_plan_image.url)
            return obj.base_plan_image.url
        return None

    def get_base_plan_image_variants(self, obj):
        """Возвращает варианты размеров base_plan_image"""
        if not obj.base_plan_image:
            return None
        variant_fields = {
            'full': 'plan_full_webp',
            'thumb': 'plan_thumb_webp',
        }
        return super().get_image_variants(obj, variant_fields, 'base_plan_image')

    def get_base_plan_image_placeholder_url(self, obj):
        """Возвращает URL placeholder для base_plan_image"""
        return super().get_image_placeholder_url(obj, 'plan_placeholder_webp', 'base_plan_image')

    def get_seo_fields(self, obj):
        """Возвращает SEO поля"""
        return {
            'meta_title': obj.meta_title,
            'meta_description': obj.meta_description,
            'meta_keywords': obj.meta_keywords,
            'og_title': obj.og_title,
            'og_description': obj.og_description,
            'og_image': obj.og_image.url if obj.og_image else None,
            'canonical_url': obj.canonical_url,
            'robots_meta': obj.robots_meta,
        }

