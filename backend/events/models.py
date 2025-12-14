from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from core.models import SEOMixin


class EventType(SEOMixin):
    """Тип мероприятия"""
    title = models.CharField(
        max_length=255,
        verbose_name='Название',
        help_text='Название типа мероприятия'
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name='URL-адрес',
        help_text='Уникальный URL-адрес для типа мероприятия'
    )
    description = models.TextField(
        verbose_name='Описание',
        help_text='Подробное описание типа мероприятия'
    )
    image = models.ImageField(
        upload_to='events/',
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
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активен'
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок сортировки'
    )

    class Meta:
        verbose_name = 'Тип мероприятия'
        verbose_name_plural = 'Типы мероприятий'
        ordering = ['order', 'title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Автоматическое создание slug из названия"""
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Возвращает URL для типа мероприятия"""
        return reverse('events:detail', kwargs={'slug': self.slug})

    def get_schema_org_json(self):
        """Генерирует JSON-LD для Schema.org (Event)"""
        schema = {
            "@context": "https://schema.org",
            "@type": "Event",
            "name": self.title,
            "description": self.description[:500] if self.description else "",
        }

        if self.image:
            schema["image"] = self.image.url

        return schema
