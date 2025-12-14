from django.db import models
from django.core.exceptions import ValidationError
from solo.models import SingletonModel
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from core.models import SEOMixin


class Restaurant(SingletonModel, SEOMixin):
    """Ресторан (Singleton - только одна запись)"""
    title = models.CharField(
        max_length=255,
        default='Ресторан',
        verbose_name='Название',
        help_text='Название ресторана'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание',
        help_text='Подробное описание ресторана'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активен'
    )

    class Meta:
        verbose_name = 'Ресторан'
        verbose_name_plural = 'Ресторан'

    def __str__(self):
        return self.title

    def clean(self):
        """Валидация Singleton - только одна запись"""
        if not self.pk:
            if Restaurant.objects.exists():
                raise ValidationError('Может быть только одна запись ресторана')

    def save(self, *args, **kwargs):
        """Переопределение save для валидации Singleton"""
        self.full_clean()
        super().save(*args, **kwargs)

    def get_schema_org_json(self):
        """Генерирует JSON-LD для Schema.org (Restaurant)"""
        site_settings = None
        try:
            from core.models import SiteSettings
            site_settings = SiteSettings.objects.get()
        except Exception:
            pass

        schema = {
            "@context": "https://schema.org",
            "@type": "Restaurant",
            "name": self.title,
            "description": self.description[:500] if self.description else "",
        }

        if site_settings and site_settings.address:
            schema["address"] = {
                "@type": "PostalAddress",
                "addressLocality": site_settings.address
            }

        if site_settings and site_settings.phone_primary:
            schema["telephone"] = site_settings.phone_primary

        return schema


class RestaurantImage(models.Model):
    """Изображения ресторана"""
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Ресторан'
    )
    image = models.ImageField(
        upload_to='restaurant/images/',
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
        verbose_name = 'Изображение ресторана'
        verbose_name_plural = 'Изображения ресторана'
        ordering = ['order', 'id']

    def __str__(self):
        return f'{self.restaurant.title} - Изображение {self.order}'


class MealType(models.Model):
    """Тип приема пищи (Завтрак, Обед, Ужин и т.д.)"""
    name = models.CharField(
        max_length=255,
        verbose_name='Название',
        help_text='Название типа приема пищи (например: Завтрак)'
    )
    icon_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Название иконки',
        help_text='Название иконки для отображения (например: breakfast)'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание',
        help_text='Описание типа приема пищи'
    )
    time_start = models.TimeField(
        blank=True,
        null=True,
        verbose_name='Время начала',
        help_text='Время начала приема пищи'
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок сортировки'
    )

    class Meta:
        verbose_name = 'Тип приема пищи'
        verbose_name_plural = 'Типы приема пищи'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class RestaurantBenefit(models.Model):
    """Преимущества ресторана"""
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='benefits',
        verbose_name='Ресторан'
    )
    text = models.CharField(
        max_length=255,
        verbose_name='Текст',
        help_text='Текст преимущества'
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок сортировки'
    )

    class Meta:
        verbose_name = 'Преимущество ресторана'
        verbose_name_plural = 'Преимущества ресторана'
        ordering = ['order', 'id']

    def __str__(self):
        return self.text
