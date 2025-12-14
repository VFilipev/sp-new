"""
Утилиты для работы с изображениями и WebP
"""
from django.core.files.images import get_image_dimensions


def get_webp_url(obj, field_name='image_webp', fallback_field='image', request=None):
    """
    Универсальная функция для получения WebP URL с fallback

    Args:
        obj: Объект модели с ImageSpecField
        field_name: Имя поля ImageSpecField (по умолчанию 'image_webp')
        fallback_field: Имя поля оригинального изображения (по умолчанию 'image')
        request: Request объект для построения абсолютного URL

    Returns:
        str: URL WebP изображения или оригинального изображения
    """
    original_image = getattr(obj, fallback_field, None)
    if not original_image:
        return None

    try:
        webp_field = getattr(obj, field_name, None)
        if webp_field and hasattr(webp_field, 'url'):
            webp_url = webp_field.url
            if request:
                return request.build_absolute_uri(webp_url)
            return webp_url
    except (AttributeError, ValueError, Exception):
        pass

    # Fallback на оригинальное изображение
    try:
        original_url = original_image.url
        if request:
            return request.build_absolute_uri(original_url)
        return original_url
    except (AttributeError, ValueError, Exception):
        return None


def get_image_url(obj, field_name='image', request=None):
    """
    Универсальная функция для получения URL изображения

    Args:
        obj: Объект модели
        field_name: Имя поля изображения
        request: Request объект для построения абсолютного URL

    Returns:
        str: URL изображения или None
    """
    image = getattr(obj, field_name, None)
    if not image:
        return None

    try:
        image_url = image.url
        if request:
            return request.build_absolute_uri(image_url)
        return image_url
    except (AttributeError, ValueError, Exception):
        return None

