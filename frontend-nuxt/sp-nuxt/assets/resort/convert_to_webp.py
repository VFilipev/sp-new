#!/usr/bin/env python3
"""
Скрипт для конвертации JPG файлов в WebP формат с качеством 80%
Обрабатывает все JPG/JPEG файлы в текущей папке resort
"""

import os
from pathlib import Path
from PIL import Image
import sys

# Получаем путь к текущей директории (папка resort)
current_dir = Path(__file__).parent.absolute()

# Расширения для конвертации
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.JPG', '.JPEG'}

# Качество WebP (80%)
WEBP_QUALITY = 80


def is_image_file(filepath: Path) -> bool:
    """Проверяет, является ли файл изображением JPG/JPEG"""
    return filepath.suffix in IMAGE_EXTENSIONS


def convert_to_webp(input_path: Path) -> bool:
    """
    Конвертирует изображение в WebP формат

    Args:
        input_path: Путь к исходному JPG файлу

    Returns:
        True если конвертация успешна, False в противном случае
    """
    try:
        # Создаем имя выходного файла (заменяем расширение на .webp)
        output_path = input_path.with_suffix('.webp')

        # Пропускаем, если WebP файл уже существует
        if output_path.exists():
            print(f"⚠ Пропущен: {input_path.name} (WebP уже существует)")
            return True

        print(f"Конвертирую: {input_path.name} -> {output_path.name}")

        # Открываем и конвертируем изображение
        with Image.open(input_path) as img:
            # Конвертируем в RGB, если изображение в другом режиме (например, RGBA)
            if img.mode in ('RGBA', 'LA', 'P'):
                # Создаем белый фон для прозрачных изображений
                rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                rgb_img.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                img = rgb_img
            elif img.mode != 'RGB':
                img = img.convert('RGB')

            # Сохраняем в WebP с качеством 80%
            img.save(output_path, 'WEBP', quality=WEBP_QUALITY, method=6)

        # Получаем размеры файлов для сравнения
        original_size = input_path.stat().st_size
        webp_size = output_path.stat().st_size
        compression_ratio = (1 - webp_size / original_size) * 100

        print(f"✓ Успешно: {output_path.name} "
              f"(сжатие: {compression_ratio:.1f}%, "
              f"{original_size / 1024:.1f}KB -> {webp_size / 1024:.1f}KB)")
        return True

    except Exception as error:
        print(f"✗ Ошибка при конвертации {input_path.name}: {error}")
        return False


def main():
    """Основная функция скрипта"""
    print("=" * 60)
    print("Конвертация JPG файлов в WebP (качество 80%)")
    print("=" * 60)
    print(f"Директория: {current_dir}\n")

    # Находим все JPG файлы
    image_files = [
        filepath for filepath in current_dir.iterdir()
        if filepath.is_file() and is_image_file(filepath)
    ]

    if not image_files:
        print("JPG файлы не найдены в текущей директории.")
        return

    print(f"Найдено {len(image_files)} JPG файлов для конвертации.\n")

    success_count = 0
    error_count = 0
    skipped_count = 0

    # Конвертируем каждый файл
    for image_file in image_files:
        result = convert_to_webp(image_file)
        if result:
            # Проверяем, был ли файл пропущен (уже существует)
            webp_path = image_file.with_suffix('.webp')
            if webp_path.exists() and webp_path.stat().st_mtime < image_file.stat().st_mtime:
                skipped_count += 1
            else:
                success_count += 1
        else:
            error_count += 1

    # Выводим итоговую статистику
    print("\n" + "=" * 60)
    print("=== Результаты ===")
    print(f"Успешно конвертировано: {success_count}")
    if skipped_count > 0:
        print(f"Пропущено (уже существует): {skipped_count}")
    print(f"Ошибок: {error_count}")
    print(f"Всего обработано: {len(image_files)}")
    print("=" * 60)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nПрервано пользователем.")
        sys.exit(1)
    except Exception as error:
        print(f"\nКритическая ошибка: {error}")
        sys.exit(1)







