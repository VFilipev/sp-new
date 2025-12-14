from rest_framework import serializers
from .models import Restaurant, RestaurantImage, MealType, RestaurantBenefit


class RestaurantImageSerializer(serializers.ModelSerializer):
    """Сериализатор для изображений ресторана"""
    image_url = serializers.SerializerMethodField()
    image_webp_url = serializers.SerializerMethodField()

    class Meta:
        model = RestaurantImage
        fields = ['id', 'image_url', 'image_webp_url', 'alt_text', 'order']

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


class MealTypeSerializer(serializers.ModelSerializer):
    """Сериализатор для типа приема пищи"""
    class Meta:
        model = MealType
        fields = ['id', 'name', 'icon_name', 'description', 'time_start', 'order']


class RestaurantBenefitSerializer(serializers.ModelSerializer):
    """Сериализатор для преимуществ ресторана"""
    class Meta:
        model = RestaurantBenefit
        fields = ['id', 'text', 'order']


class RestaurantSerializer(serializers.ModelSerializer):
    """Сериализатор для ресторана"""
    images = RestaurantImageSerializer(many=True, read_only=True)
    meal_types = MealTypeSerializer(many=True, read_only=True)
    benefits = RestaurantBenefitSerializer(many=True, read_only=True)
    schema_org_json = serializers.SerializerMethodField()
    seo_fields = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = [
            'id', 'title', 'description', 'is_active',
            'images', 'meal_types', 'benefits',
            'schema_org_json', 'seo_fields'
        ]

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

