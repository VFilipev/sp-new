"""
Management command для обработки существующих изображений
Создает все варианты размеров для существующих изображений
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import HeroImage, GalleryImage, SiteSettings
from lodges.models import LodgeImage, LodgeType
from news.models import News
from events.models import EventType
from restaurant.models import RestaurantImage


class Command(BaseCommand):
    help = 'Обрабатывает существующие изображения, создавая все варианты размеров'

    def add_arguments(self, parser):
        parser.add_argument(
            '--model',
            type=str,
            help='Обработать только указанную модель (например, LodgeImage)',
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Обработать все модели',
        )

    def handle(self, *args, **options):
        models_to_process = []

        if options['all']:
            models_to_process = [
                ('HeroImage', HeroImage),
                ('GalleryImage', GalleryImage),
                ('SiteSettings', SiteSettings),
                ('LodgeImage', LodgeImage),
                ('LodgeType', LodgeType),
                ('News', News),
                ('EventType', EventType),
                ('RestaurantImage', RestaurantImage),
            ]
        elif options['model']:
            model_name = options['model']
            model_map = {
                'HeroImage': HeroImage,
                'GalleryImage': GalleryImage,
                'SiteSettings': SiteSettings,
                'LodgeImage': LodgeImage,
                'LodgeType': LodgeType,
                'News': News,
                'EventType': EventType,
                'RestaurantImage': RestaurantImage,
            }
            if model_name in model_map:
                models_to_process = [(model_name, model_map[model_name])]
            else:
                self.stdout.write(
                    self.style.ERROR(f'Неизвестная модель: {model_name}')
                )
                return
        else:
            self.stdout.write(
                self.style.ERROR('Укажите --model или --all')
            )
            return

        total_processed = 0

        for model_name, model_class in models_to_process:
            self.stdout.write(f'Обработка модели: {model_name}')

            # Получаем все объекты с изображениями
            if model_name == 'SiteSettings':
                # SiteSettings - Singleton
                try:
                    obj = model_class.objects.get()
                    if obj.hero_image or obj.base_plan_image:
                        self._process_object(obj, model_name)
                        total_processed += 1
                except model_class.DoesNotExist:
                    self.stdout.write(
                        self.style.WARNING(f'{model_name} не существует')
                    )
            else:
                # Обычные модели
                queryset = model_class.objects.all()
                if hasattr(model_class, 'image'):
                    queryset = queryset.exclude(image__isnull=True).exclude(image='')
                elif hasattr(model_class, 'hero_image'):
                    queryset = queryset.exclude(hero_image__isnull=True).exclude(hero_image='')
                elif hasattr(model_class, 'base_plan_image'):
                    queryset = queryset.exclude(base_plan_image__isnull=True).exclude(base_plan_image='')

                count = queryset.count()
                self.stdout.write(f'  Найдено объектов: {count}')

                for obj in queryset:
                    self._process_object(obj, model_name)
                    total_processed += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Обработка завершена. Обработано объектов: {total_processed}'
            )
        )

    def _process_object(self, obj, model_name):
        """Обрабатывает один объект, генерируя все варианты"""
        try:
            # Получаем все ImageSpecField
            image_fields = []

            if hasattr(obj, 'image') and obj.image:
                image_fields.append('image')
            if hasattr(obj, 'hero_image') and obj.hero_image:
                image_fields.append('hero_image')
            if hasattr(obj, 'preview_image') and obj.preview_image:
                image_fields.append('preview_image')
            if hasattr(obj, 'base_plan_image') and obj.base_plan_image:
                image_fields.append('base_plan_image')

            for field_name in image_fields:
                image_field = getattr(obj, field_name)
                if image_field:
                    # Генерируем все варианты, обращаясь к ним
                    # ImageKit создаст файлы при первом обращении
                    self._generate_variants(obj, field_name)

            self.stdout.write(f'  ✓ {model_name} #{obj.pk}')

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'  ✗ Ошибка при обработке {model_name} #{obj.pk}: {e}')
            )

    def _generate_variants(self, obj, field_name):
        """Генерирует все варианты для поля изображения"""
        # Получаем все атрибуты объекта, которые могут быть ImageSpecField
        for attr_name in dir(obj):
            if attr_name.startswith('_') or attr_name == field_name:
                continue

            try:
                attr = getattr(obj, attr_name)
                # Проверяем, является ли это ImageSpecField
                if hasattr(attr, 'url'):
                    # Пытаемся получить URL - это заставит ImageKit создать файл
                    try:
                        url = attr.url
                        # Если успешно, вариант создан
                    except Exception:
                        # Если вариант не существует, пропускаем
                        pass
            except Exception:
                pass

