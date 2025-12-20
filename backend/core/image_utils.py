"""
Утилиты для работы с изображениями
"""
import base64
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def generate_placeholder_base64(image_field, quality=50):
    """
    Генерирует base64 placeholder из изображения с низким качеством
    Сохраняет оригинальный размер изображения, но сжимает качество

    Args:
        image_field: Поле ImageField модели
        quality: Качество WebP (по умолчанию 50, как в compress_image.py)

    Returns:
        str: Base64 строка для data URI или None
    """
    if not image_field or not image_field.name:
        return None

    try:
        # Открываем изображение
        img = Image.open(image_field)

        # Конвертируем в RGB если нужно (для JPEG совместимости)
        if img.mode in ('RGBA', 'LA', 'P'):
            rgb_img = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            rgb_img.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
            img = rgb_img
        elif img.mode != 'RGB':
            img = img.convert('RGB')

        # Сохраняем с низким качеством (как в compress_image.py)
        buffer = BytesIO()
        img.save(buffer, format='WEBP', quality=quality, method=6)
        buffer.seek(0)

        # Кодируем в base64
        base64_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return f"data:image/webp;base64,{base64_str}"

    except Exception as e:
        # Логируем ошибку, но не прерываем выполнение
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Ошибка генерации placeholder: {e}")
        return None


def generate_placeholder_file(image_field, upload_to, quality=50):
    """
    Генерирует файл placeholder с низким качеством
    Сохраняет оригинальный размер изображения, но сжимает качество

    Args:
        image_field: Поле ImageField модели
        upload_to: Путь для сохранения (например, 'placeholders/hero/')
        quality: Качество WebP (по умолчанию 50, как в compress_image.py)

    Returns:
        str: Путь к сохраненному файлу или None
    """
    if not image_field or not image_field.name:
        return None

    try:
        # Открываем изображение
        img = Image.open(image_field)

        # Конвертируем в RGB если нужно (для JPEG совместимости)
        if img.mode in ('RGBA', 'LA', 'P'):
            rgb_img = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            rgb_img.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
            img = rgb_img
        elif img.mode != 'RGB':
            img = img.convert('RGB')

        # Сохраняем с низким качеством (как в compress_image.py)
        buffer = BytesIO()
        img.save(buffer, format='WEBP', quality=quality, method=6)
        buffer.seek(0)

        # Генерируем имя файла
        original_name = image_field.name
        name_without_ext = original_name.rsplit('.', 1)[0]
        filename = f"{name_without_ext}_placeholder.webp"
        filepath = f"{upload_to}{filename}"

        # Сохраняем файл
        file_content = ContentFile(buffer.getvalue())
        saved_path = default_storage.save(filepath, file_content)

        return saved_path

    except Exception as e:
        # Логируем ошибку
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Ошибка генерации placeholder файла: {e}")
        return None

