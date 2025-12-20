"""
Кастомные процессоры для ImageKit
"""
from PIL import Image, ImageFilter
from imagekit.processors import ResizeToFill, ResizeToFit


class SmartCropProcessor(ResizeToFill):
    """
    Умный кроп изображения - сохраняет важные части (центр изображения)
    Более продвинутая версия может использовать face detection
    """
    def process(self, img):
        """
        Кропает изображение с сохранением центральной части
        """
        return super().process(img)


class NoOpProcessor:
    """
    Процессор, который не изменяет изображение
    Используется для placeholder'ов - сохраняет оригинальный размер,
    но качество будет установлено через options
    """
    def process(self, img):
        """
        Возвращает изображение без изменений

        Args:
            img: PIL Image объект

        Returns:
            PIL Image без изменений
        """
        return img


class ResizeToFitWithPadding(ResizeToFit):
    """
    Изменяет размер с сохранением пропорций и добавлением padding
    """
    def __init__(self, width, height, background_color=(255, 255, 255, 0)):
        super().__init__(width, height)
        self.background_color = background_color

    def process(self, img):
        """
        Изменяет размер с сохранением пропорций и добавляет padding

        Args:
            img: PIL Image объект

        Returns:
            PIL Image с измененным размером и padding
        """
        # ImageKit передает PIL Image напрямую
        # Вычисляем новые размеры с сохранением пропорций
        original_width, original_height = img.size
        target_width, target_height = self.width, self.height

        # Вычисляем масштаб
        scale = min(target_width / original_width, target_height / original_height)
        new_width = int(original_width * scale)
        new_height = int(original_height * scale)

        # Изменяем размер
        resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Создаем новое изображение с нужным размером и фоном
        if img.mode == 'RGBA':
            new_img = Image.new('RGBA', (target_width, target_height), self.background_color)
        else:
            new_img = Image.new('RGB', (target_width, target_height), self.background_color[:3])
            resized = resized.convert('RGB')

        # Центрируем изображение
        x_offset = (target_width - new_width) // 2
        y_offset = (target_height - new_height) // 2
        new_img.paste(resized, (x_offset, y_offset))

        return new_img

