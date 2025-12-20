#!/usr/bin/env python3
"""
Скрипт для сжатия изображений с заданным качеством
Принимает название файла и процент сжатия (1-90)
Создает новую фотографию с добавлением -plc к названию
"""

import os
import sys
from pathlib import Path
from PIL import Image

# Получаем путь к текущей директории (папка resort)
current_dir = Path(__file__).parent.absolute()


def compress_image(filename: str, quality: int) -> bool:
    """
    Сжимает изображение с заданным качеством

    Args:
        filename: Название файла с расширением (например, hero.webp)
        quality: Процент сжатия от 1 до 90 (где 1 - максимальное сжатие, 90 - минимальное)

    Returns:
        True если сжатие успешно, False в противном случае
    """
    try:
        # Проверяем качество
        if not (1 <= quality <= 90):
            print(f"✗ Ошибка: качество должно быть от 1 до 90, получено: {quality}")
            return False

        # Создаем путь к исходному файлу
        input_path = current_dir / filename

        # Проверяем существование файла
        if not input_path.exists():
            print(f"✗ Ошибка: файл {filename} не найден в директории {current_dir}")
            return False

        # Получаем расширение файла
        file_extension = input_path.suffix.lower()

        # Проверяем, что это изображение
        supported_formats = {'.jpg', '.jpeg', '.png', '.webp', '.JPG', '.JPEG', '.PNG', '.WEBP'}
        if file_extension not in supported_formats:
            print(f"✗ Ошибка: неподдерживаемый формат {file_extension}")
            print(f"Поддерживаемые форматы: {', '.join(supported_formats)}")
            return False

        # Создаем имя выходного файла (добавляем -plc перед расширением)
        # Например: hero.webp -> hero-plc.webp
        stem = input_path.stem  # имя без расширения
        output_filename = f"{stem}-plc{file_extension}"
        output_path = current_dir / output_filename

        # Пропускаем, если файл уже существует
        if output_path.exists():
            print(f"⚠ Файл {output_filename} уже существует. Пропуск.")
            return True

        print(f"Сжимаю: {filename} -> {output_filename} (качество: {quality})")

        # Открываем изображение
        with Image.open(input_path) as img:
            # Определяем формат для сохранения
            save_format = None
            save_kwargs = {}

            if file_extension in {'.jpg', '.jpeg', '.JPG', '.JPEG'}:
                save_format = 'JPEG'
                # Конвертируем в RGB, если нужно
                if img.mode in ('RGBA', 'LA', 'P'):
                    rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    rgb_img.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                    img = rgb_img
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                save_kwargs = {'quality': quality, 'optimize': True}

            elif file_extension == '.webp':
                save_format = 'WEBP'
                save_kwargs = {'quality': quality, 'method': 6}

            elif file_extension == '.png':
                save_format = 'PNG'
                # Для PNG используем optimize и compress_level
                # quality для PNG работает по-другому, поэтому используем compress_level
                # Преобразуем quality (1-90) в compress_level (0-9), где 0 - без сжатия, 9 - максимальное
                compress_level = int((90 - quality) / 10)  # Инвертируем: 90 -> 0, 1 -> 8
                save_kwargs = {'optimize': True, 'compress_level': min(compress_level, 9)}

            # Сохраняем сжатое изображение
            img.save(output_path, save_format, **save_kwargs)

        # Получаем размеры файлов для сравнения
        original_size = input_path.stat().st_size
        compressed_size = output_path.stat().st_size
        compression_ratio = (1 - compressed_size / original_size) * 100

        print(f"✓ Успешно: {output_filename} "
              f"(сжатие: {compression_ratio:.1f}%, "
              f"{original_size / 1024:.1f}KB -> {compressed_size / 1024:.1f}KB)")
        return True

    except Exception as error:
        print(f"✗ Ошибка при сжатии {filename}: {error}")
        return False


def main():
    """Основная функция скрипта"""
    if len(sys.argv) != 3:
        print("Использование: python compress_image.py <имя_файла> <качество>")
        print("Пример: python compress_image.py hero.webp 50")
        print("\nПараметры:")
        print("  <имя_файла> - название файла с расширением (например, hero.webp)")
        print("  <качество>  - процент сжатия от 1 до 90 (1 - максимальное сжатие, 90 - минимальное)")
        sys.exit(1)

    filename = sys.argv[1]

    try:
        quality = int(sys.argv[2])
    except ValueError:
        print(f"✗ Ошибка: качество должно быть числом, получено: {sys.argv[2]}")
        sys.exit(1)

    print("=" * 60)
    print("Сжатие изображения")
    print("=" * 60)
    print(f"Директория: {current_dir}\n")

    success = compress_image(filename, quality)

    if success:
        print("\n" + "=" * 60)
        print("✓ Сжатие завершено успешно")
        print("=" * 60)
        sys.exit(0)
    else:
        print("\n" + "=" * 60)
        print("✗ Ошибка при сжатии")
        print("=" * 60)
        sys.exit(1)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nПрервано пользователем.")
        sys.exit(1)
    except Exception as error:
        print(f"\nКритическая ошибка: {error}")
        sys.exit(1)







