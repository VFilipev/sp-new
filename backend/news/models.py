from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from core.models import SEOMixin


class News(SEOMixin):
    """Новости"""
    title = models.CharField(
        max_length=255,
        verbose_name='Заголовок',
        help_text='Заголовок новости'
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name='URL-адрес',
        help_text='Уникальный URL-адрес для новости'
    )
    content = models.TextField(
        verbose_name='Содержание',
        help_text='Полное содержание новости'
    )
    short_description = models.TextField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name='Краткое описание',
        help_text='Краткое описание для списков и превью'
    )
    excerpt = models.TextField(
        max_length=300,
        blank=True,
        null=True,
        verbose_name='Анонс',
        help_text='Краткий анонс новости (до 300 символов)'
    )
    image = models.ImageField(
        upload_to='news/',
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
    published_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='Дата публикации',
        help_text='Дата и время публикации новости'
    )
    is_published = models.BooleanField(
        default=False,
        verbose_name='Опубликовано',
        help_text='Отображать новость на сайте'
    )
    reading_time = models.PositiveIntegerField(
        default=0,
        verbose_name='Время чтения (минуты)',
        help_text='Примерное время чтения в минутах'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-published_at', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Автоматическое создание slug и расчет времени чтения"""
        if not self.slug:
            self.slug = slugify(self.title)

        # Автоматический расчет времени чтения
        if self.content:
            self.reading_time = self.calculate_reading_time()

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Возвращает URL для новости"""
        return reverse('news:detail', kwargs={'slug': self.slug})

    def calculate_reading_time(self):
        """Рассчитывает примерное время чтения в минутах"""
        # Средняя скорость чтения: 200-250 слов в минуту
        # Берем 200 слов/минуту для консервативной оценки
        words_per_minute = 200

        # Подсчитываем количество слов в тексте
        word_count = len(self.content.split())

        # Рассчитываем время чтения
        reading_time = max(1, round(word_count / words_per_minute))

        return reading_time

    def get_schema_org_json(self):
        """Генерирует JSON-LD для Schema.org (NewsArticle)"""
        site_settings = None
        try:
            from core.models import SiteSettings
            site_settings = SiteSettings.objects.get()
        except Exception:
            pass

        schema = {
            "@context": "https://schema.org",
            "@type": "NewsArticle",
            "headline": self.title,
            "description": self.short_description or self.excerpt or self.content[:200] if self.content else "",
            "datePublished": self.published_at.isoformat() if self.published_at else "",
            "dateModified": self.updated_at.isoformat() if self.updated_at else "",
        }

        if self.image:
            schema["image"] = self.image.url

        if site_settings and site_settings.site_name:
            schema["publisher"] = {
                "@type": "Organization",
                "name": site_settings.site_name
            }

        if self.reading_time:
            schema["timeRequired"] = f"PT{self.reading_time}M"

        return schema
