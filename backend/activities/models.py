from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from core.models import SEOMixin


class Activity(SEOMixin):
    """Активности (активный и спокойный отдых)"""
    CATEGORY_CHOICES = [
        ('active', 'Активный отдых'),
        ('peaceful', 'Спокойный отдых'),
    ]

    SEASON_CHOICES = [
        ('winter', 'Зима'),
        ('summer', 'Лето'),
    ]

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        verbose_name='Категория',
        help_text='Тип активности'
    )
    season = models.CharField(
        max_length=20,
        choices=SEASON_CHOICES,
        blank=True,
        null=True,
        verbose_name='Сезон',
        help_text='Сезон активности (зима или лето)'
    )
    title = models.CharField(
        max_length=255,
        verbose_name='Название',
        help_text='Название активности'
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name='URL-адрес',
        help_text='Уникальный URL-адрес для активности'
    )
    description = models.TextField(
        verbose_name='Описание',
        help_text='Подробное описание активности'
    )
    image = models.ImageField(
        upload_to='activities/',
        blank=True,
        null=True,
        verbose_name='Изображение'
    )
    image_webp = ImageSpecField(
        source='image',
        processors=[ResizeToFill(1920, 1080)],
        format='WEBP',
        options={'quality': 85}
    )
    video = models.FileField(
        upload_to='activities/videos/',
        blank=True,
        null=True,
        verbose_name='Видео',
        help_text='Видеофайл для активности'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активна'
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок сортировки'
    )

    class Meta:
        verbose_name = 'Активность'
        verbose_name_plural = 'Активности'
        ordering = ['category', 'season', 'order', 'title']

    def __str__(self):
        return f'{self.get_category_display()} - {self.title}'

    def save(self, *args, **kwargs):
        """Автоматическое создание slug из названия"""
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Возвращает URL для активности"""
        return reverse('activities:detail', kwargs={'slug': self.slug})
