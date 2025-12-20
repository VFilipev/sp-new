"""
Management command для регенерации вариантов изображений
Удаляет существующие варианты и создает их заново
"""
from django.core.management.base import BaseCommand
from imagekit.cachefiles import ImageCacheFile
from imagekit.cachefiles.backends import Simple
from core.models import HeroImage, GalleryImage, SiteSettings
from lodges.models import LodgeImage, LodgeType
from news.models import News
from events.models import EventType
from restaurant.models import RestaurantImage
import os


class Command(BaseCommand):
    help = 'Регенерирует варианты изображений (удаляет старые и создает новые)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--model',
            type=str,
            help='Регенерировать только для указанной модели',
        )
        parser.add_argument(
            '--variant',
            type=str,
            help='Регенерировать только указанный вариант (например, lodge_main_webp)',
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Регенерировать все варианты для всех моделей',
        )

    def handle(self, *args, **options):
        if not options['all'] and not options['model']:
            self.stdout.write(
                self.style.ERROR('Укажите --model или --all')
            )
            return

        if options['all']:
            self._regenerate_all(options.get('variant'))
        elif options['model']:
            self._regenerate_model(options['model'], options.get('variant'))

    def _regenerate_all(self, variant_name=None):
        """Регенерирует все варианты для всех моделей"""
        models = [
            HeroImage,
            GalleryImage,
            SiteSettings,
            LodgeImage,
            LodgeType,
            News,
            EventType,
            RestaurantImage,
        ]

        for model in models:
            self._regenerate_model(model.__name__, variant_name)

    def _regenerate_model(self, model_name, variant_name=None):
        """Регенерирует варианты для указанной модели"""
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

        if model_name not in model_map:
            self.stdout.write(
                self.style.ERROR(f'Неизвестная модель: {model_name}')
            )
            return

        model = model_map[model_name]
        self.stdout.write(f'Регенерация вариантов для: {model_name}')

        # Получаем все объекты
        queryset = model.objects.all()
        if model_name == 'SiteSettings':
            # Singleton
            try:
                queryset = [model.objects.get()]
            except model.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f'{model_name} не существует')
                )
                return

        count = 0
        for obj in queryset:
            if self._regenerate_object_variants(obj, variant_name):
                count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Регенерировано вариантов для {count} объектов'
            )
        )

    def _regenerate_object_variants(self, obj, variant_name=None):
        """Регенерирует варианты для одного объекта"""
        try:
            # Получаем все ImageSpecField
            variant_fields = []

            for attr_name in dir(obj):
                if attr_name.startswith('_'):
                    continue

                try:
                    attr = getattr(obj, attr_name)
                    # Проверяем, является ли это ImageSpecField
                    if isinstance(attr, ImageCacheFile):
                        if variant_name is None or attr_name == variant_name:
                            variant_fields.append(attr_name)
                except Exception:
                    pass

            # Удаляем старые файлы
            for variant_field_name in variant_fields:
                try:
                    variant_field = getattr(obj, variant_field_name)
                    if hasattr(variant_field, 'cachefile') and variant_field.cachefile:
                        cachefile = variant_field.cachefile
                        if hasattr(cachefile, 'path'):
                            filepath = cachefile.path
                            if os.path.exists(filepath):
                                os.remove(filepath)
                                self.stdout.write(f'  Удален: {filepath}')
                except Exception as e:
                    self.stdout.write(
                        self.style.WARNING(f'  Ошибка удаления {variant_field_name}: {e}')
                    )

            # Генерируем новые варианты
            for variant_field_name in variant_fields:
                try:
                    variant_field = getattr(obj, variant_field_name)
                    # Обращаемся к URL - это заставит ImageKit создать файл
                    url = variant_field.url
                    self.stdout.write(f'  Создан: {variant_field_name}')
                except Exception as e:
                    self.stdout.write(
                        self.style.WARNING(f'  Ошибка создания {variant_field_name}: {e}')
                    )

            return True

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Ошибка при регенерации вариантов: {e}')
            )
            return False

