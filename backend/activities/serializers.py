from rest_framework import serializers
from .models import Activity


class ActivitySerializer(serializers.ModelSerializer):
    """Сериализатор для активности"""
    image_url = serializers.SerializerMethodField()
    image_webp_url = serializers.SerializerMethodField()
    video_url = serializers.SerializerMethodField()
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    season_display = serializers.CharField(source='get_season_display', read_only=True)
    seo_fields = serializers.SerializerMethodField()

    class Meta:
        model = Activity
        fields = [
            'id', 'category', 'category_display', 'season', 'season_display',
            'title', 'slug', 'description', 'image_url', 'image_webp_url',
            'video_url', 'is_active', 'order', 'seo_fields'
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

    def get_video_url(self, obj):
        """Возвращает URL видео"""
        if obj.video:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.video.url)
            return obj.video.url
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

