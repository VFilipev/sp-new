from rest_framework import serializers
from .models import LodgeType, Lodge, LodgeImage
from core.serializer_mixins import ImageVariantsMixin


class LodgeImageSerializer(ImageVariantsMixin, serializers.ModelSerializer):
    """Сериализатор для изображений размещения"""
    image_url = serializers.SerializerMethodField()
    image_webp_url = serializers.SerializerMethodField()
    image_placeholder_url = serializers.SerializerMethodField()
    image_placeholder_base64 = serializers.SerializerMethodField()
    image_variants = serializers.SerializerMethodField()

    class Meta:
        model = LodgeImage
        fields = [
            'id', 'image_url', 'image_webp_url', 'image_placeholder_url',
            'image_placeholder_base64', 'image_variants', 'alt_text', 'order'
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
                # Используем lodge_main_webp как основной вариант
                webp_url = obj.lodge_main_webp.url if hasattr(obj, 'lodge_main_webp') and obj.lodge_main_webp else None
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
        return super().get_image_placeholder_url(obj, 'lodge_placeholder_webp', 'image')

    def get_image_placeholder_base64(self, obj):
        """Возвращает base64 placeholder"""
        return super().get_image_placeholder_base64(obj, obj.image)

    def get_image_variants(self, obj):
        """Возвращает варианты размеров изображения"""
        variant_fields = {
            'main': 'lodge_main_webp',
            'card': 'lodge_card_webp',
            'thumb': 'lodge_thumb_webp',
        }
        return super().get_image_variants(obj, variant_fields, 'image')


class LodgeSerializer(serializers.ModelSerializer):
    """Сериализатор для размещения"""
    images = LodgeImageSerializer(many=True, read_only=True)
    lodge_type_name = serializers.CharField(source='lodge_type.name', read_only=True)
    lodge_type_slug = serializers.CharField(source='lodge_type.slug', read_only=True)
    schema_org_json = serializers.SerializerMethodField()
    breadcrumbs = serializers.SerializerMethodField()
    seo_fields = serializers.SerializerMethodField()

    class Meta:
        model = Lodge
        fields = [
            'id', 'name', 'slug', 'lodge_type', 'lodge_type_name', 'lodge_type_slug',
            'description', 'short_description', 'capacity', 'area', 'price_from',
            'location_description', 'is_active', 'order',
            'images', 'schema_org_json', 'breadcrumbs', 'seo_fields'
        ]

    def get_schema_org_json(self, obj):
        """Возвращает Schema.org JSON-LD"""
        return obj.get_schema_org_json()

    def get_breadcrumbs(self, obj):
        """Возвращает хлебные крошки"""
        return obj.get_breadcrumbs()

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


class LodgeTypeSerializer(ImageVariantsMixin, serializers.ModelSerializer):
    """Сериализатор для типа размещения"""
    lodges = LodgeSerializer(many=True, read_only=True)
    hero_image_url = serializers.SerializerMethodField()
    hero_image_webp_url = serializers.SerializerMethodField()
    hero_image_placeholder_url = serializers.SerializerMethodField()
    hero_image_placeholder_base64 = serializers.SerializerMethodField()
    hero_image_variants = serializers.SerializerMethodField()
    seo_fields = serializers.SerializerMethodField()

    class Meta:
        model = LodgeType
        fields = [
            'id', 'name', 'slug', 'subtitle', 'hero_image_url', 'hero_image_webp_url',
            'hero_image_placeholder_url', 'hero_image_placeholder_base64',
            'hero_image_variants', 'description', 'is_active', 'order',
            'lodges', 'seo_fields'
        ]

    def get_hero_image_url(self, obj):
        """Возвращает URL оригинального изображения"""
        if obj.hero_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.hero_image.url)
            return obj.hero_image.url
        return None

    def get_hero_image_webp_url(self, obj):
        """Возвращает URL WebP изображения с fallback на оригинал"""
        if obj.hero_image:
            request = self.context.get('request')
            try:
                # Используем lodge_hero_main_webp как основной вариант
                webp_url = obj.lodge_hero_main_webp.url if hasattr(obj, 'lodge_hero_main_webp') and obj.lodge_hero_main_webp else None
                if not webp_url:
                    webp_url = obj.hero_image_webp.url if hasattr(obj, 'hero_image_webp') and obj.hero_image_webp else None
                if webp_url:
                    if request:
                        return request.build_absolute_uri(webp_url)
                    return webp_url
            except:
                pass
            # Fallback на оригинальное изображение
            return self.get_hero_image_url(obj)
        return None

    def get_hero_image_placeholder_url(self, obj):
        """Возвращает URL placeholder для hero_image"""
        return super().get_image_placeholder_url(obj, 'lodge_hero_placeholder_webp', 'hero_image')

    def get_hero_image_placeholder_base64(self, obj):
        """Возвращает base64 placeholder для hero_image"""
        return super().get_image_placeholder_base64(obj, obj.hero_image)

    def get_hero_image_variants(self, obj):
        """Возвращает варианты размеров hero_image"""
        if not obj.hero_image:
            return None
        variant_fields = {
            'main': 'lodge_hero_main_webp',
            'card': 'lodge_hero_card_webp',
        }
        return super().get_image_variants(obj, variant_fields, 'hero_image')

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

