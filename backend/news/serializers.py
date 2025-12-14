from rest_framework import serializers
from .models import News


class NewsListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка новостей (краткая версия)"""
    image_url = serializers.SerializerMethodField()
    image_webp_url = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = [
            'id', 'title', 'slug', 'short_description', 'excerpt',
            'image_url', 'image_webp_url', 'published_at', 'reading_time'
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


class NewsDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для детальной страницы новости (полная версия)"""
    image_url = serializers.SerializerMethodField()
    image_webp_url = serializers.SerializerMethodField()
    schema_org_json = serializers.SerializerMethodField()
    seo_fields = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = [
            'id', 'title', 'slug', 'content', 'short_description', 'excerpt',
            'image_url', 'image_webp_url', 'published_at', 'is_published',
            'reading_time', 'created_at', 'updated_at',
            'schema_org_json', 'seo_fields'
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

    def get_schema_org_json(self, obj):
        """Возвращает Schema.org JSON-LD"""
        return obj.get_schema_org_json()

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

