from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from core.models import SEOMixin


class LodgeType(SEOMixin):
    """Тип размещения (Коттеджи, Модульные дома и т.д.)"""
    name = models.CharField(
        max_length=255,
        verbose_name='Название',
        help_text='Название типа размещения (например: Коттеджи)'
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name='URL-адрес',
        help_text='Уникальный URL-адрес для типа размещения'
    )
    subtitle = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Подзаголовок',
        help_text='Краткий подзаголовок для типа размещения'
    )
    hero_image = models.ImageField(
        upload_to='lodges/types/',
        blank=True,
        null=True,
        verbose_name='Главное изображение'
    )
    hero_image_webp = ImageSpecField(
        source='hero_image',
        processors=[ResizeToFill(1920, 1080)],
        format='WEBP',
        options={'quality': 85}
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание',
        help_text='Подробное описание типа размещения'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активен'
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок сортировки'
    )

    class Meta:
        verbose_name = 'Тип размещения'
        verbose_name_plural = 'Типы размещения'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Автоматическое создание slug из названия"""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Возвращает URL для типа размещения"""
        return reverse('lodges:type-detail', kwargs={'slug': self.slug})


class Lodge(SEOMixin):
    """Размещение (конкретный коттедж, дом и т.д.)"""
    lodge_type = models.ForeignKey(
        LodgeType,
        on_delete=models.CASCADE,
        related_name='lodges',
        verbose_name='Тип размещения'
    )
    name = models.CharField(
        max_length=255,
        verbose_name='Название',
        help_text='Название размещения (например: Коттедж №1)'
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name='URL-адрес',
        help_text='Уникальный URL-адрес для размещения'
    )
    description = models.TextField(
        verbose_name='Описание',
        help_text='Подробное описание размещения'
    )
    short_description = models.TextField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name='Краткое описание',
        help_text='Краткое описание для списков и превью'
    )
    capacity = models.PositiveIntegerField(
        verbose_name='Вместимость',
        help_text='Количество человек'
    )
    area = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name='Площадь',
        help_text='Площадь в квадратных метрах'
    )
    price_from = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='Цена от',
        help_text='Минимальная цена за размещение'
    )
    location_description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание расположения',
        help_text='Описание расположения на территории базы'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активно'
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок сортировки'
    )

    class Meta:
        verbose_name = 'Размещение'
        verbose_name_plural = 'Размещения'
        ordering = ['order', 'name']

    def __str__(self):
        return f'{self.lodge_type.name} - {self.name}'

    def save(self, *args, **kwargs):
        """Автоматическое создание slug из названия"""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Возвращает URL для размещения"""
        return reverse('lodges:detail', kwargs={'slug': self.slug})

    def get_schema_org_json(self):
        """Генерирует JSON-LD для Schema.org (LodgingBusiness)"""
        site_settings = None
        try:
            from core.models import SiteSettings
            site_settings = SiteSettings.objects.get()
        except Exception:
            pass

        schema = {
            "@context": "https://schema.org",
            "@type": "LodgingBusiness",
            "name": self.name,
            "description": self.short_description or self.description[:200] if self.description else "",
            "address": {
                "@type": "PostalAddress",
                "addressLocality": site_settings.address if site_settings else ""
            }
        }

        if self.price_from:
            schema["priceRange"] = f"от {self.price_from} руб."

        if self.capacity:
            schema["numberOfRooms"] = str(self.capacity)

        return schema

    def get_breadcrumbs(self):
        """Генерирует хлебные крошки для навигации"""
        breadcrumbs = [
            {
                "name": "Главная",
                "url": "/"
            },
            {
                "name": self.lodge_type.name,
                "url": self.lodge_type.get_absolute_url() if hasattr(self.lodge_type, 'get_absolute_url') else f"/lodges/{self.lodge_type.slug}/"
            },
            {
                "name": self.name,
                "url": self.get_absolute_url()
            }
        ]
        return breadcrumbs


class LodgeImage(models.Model):
    """Изображения для размещения"""
    lodge = models.ForeignKey(
        Lodge,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Размещение'
    )
    image = models.ImageField(
        upload_to='lodges/images/',
        verbose_name='Изображение'
    )
    image_webp = ImageSpecField(
        source='image',
        processors=[ResizeToFill(1920, 1080)],
        format='WEBP',
        options={'quality': 85}
    )
    alt_text = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Alt текст',
        help_text='Альтернативный текст для изображения'
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок сортировки'
    )

    class Meta:
        verbose_name = 'Изображение размещения'
        verbose_name_plural = 'Изображения размещения'
        ordering = ['order', 'id']

    def __str__(self):
        return f'{self.lodge.name} - Изображение {self.order}'
