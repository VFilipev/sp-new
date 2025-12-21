"""
Миксины для сериализаторов изображений
"""
from rest_framework import serializers


class ImageVariantsMixin:
    """
    Миксин для добавления методов получения вариантов изображений
    """

    def get_image_variants(self, obj, variant_fields, source_field_name='image'):
        """
        Возвращает объект со всеми вариантами размеров изображения

        Args:
            obj: Объект модели
            variant_fields: Словарь с названиями вариантов и их полей
                Например: {'main': 'lodge_main_webp', 'card': 'lodge_card_webp'}
            source_field_name: Имя исходного поля изображения (по умолчанию 'image')

        Returns:
            dict: Словарь с URL вариантов или None
        """
        # Проверяем наличие исходного изображения
        source_image = getattr(obj, source_field_name, None)
        if not source_image:
            return None

        request = self.context.get('request')
        variants = {}

        for variant_name, field_name in variant_fields.items():
            try:
                variant_field = getattr(obj, field_name, None)
                if variant_field and hasattr(variant_field, 'url'):
                    url = variant_field.url
                    if request:
                        url = request.build_absolute_uri(url)
                    variants[variant_name] = url
            except Exception:
                # Если вариант не существует, пропускаем
                pass

        return variants if variants else None

    def get_image_placeholder_url(self, obj, placeholder_field_name, source_field_name='image'):
        """
        Возвращает URL placeholder изображения

        Args:
            obj: Объект модели
            placeholder_field_name: Имя поля placeholder (например, 'hero_placeholder_webp')
            source_field_name: Имя исходного поля изображения (по умолчанию 'image')

        Returns:
            str: URL placeholder или None
        """
        # Проверяем наличие исходного изображения
        source_image = getattr(obj, source_field_name, None)
        if not source_image:
            return None

        request = self.context.get('request')
        try:
            placeholder_field = getattr(obj, placeholder_field_name, None)
            if placeholder_field and hasattr(placeholder_field, 'url'):
                url = placeholder_field.url
                if request:
                    url = request.build_absolute_uri(url)
                return url
        except Exception:
            pass

        return None

