from django.db import models
from django.core.exceptions import ValidationError
from solo.models import SingletonModel
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from .image_processors import SmartCropProcessor, NoOpProcessor, ResizeToFitWithPadding


class SEOMixin(models.Model):
    """Абстрактная модель для SEO полей"""
    meta_title = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Meta Title',
        help_text='Заголовок страницы для поисковых систем (до 60 символов)'
    )
    meta_description = models.TextField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name='Meta Description',
        help_text='Описание страницы для поисковых систем (до 160 символов)'
    )
    meta_keywords = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Meta Keywords',
        help_text='Ключевые слова через запятую'
    )
    og_title = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='OG Title',
        help_text='Заголовок для Open Graph (социальные сети)'
    )
    og_description = models.TextField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name='OG Description',
        help_text='Описание для Open Graph (социальные сети)'
    )
    og_image = models.ImageField(
        upload_to='og_images/',
        blank=True,
        null=True,
        verbose_name='OG Image',
        help_text='Изображение для Open Graph (рекомендуемый размер: 1200x630px)'
    )
    canonical_url = models.URLField(
        blank=True,
        null=True,
        verbose_name='Canonical URL',
        help_text='Канонический URL страницы'
    )
    robots_meta = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        default='index, follow',
        verbose_name='Robots Meta',
        help_text='Директива для поисковых роботов (например: noindex, nofollow)'
    )

    class Meta:
        abstract = True


class SiteSettings(SingletonModel, SEOMixin):
    """Настройки сайта (Singleton - только одна запись)"""
    site_name = models.CharField(
        max_length=255,
        default='Строгановские Просторы',
        verbose_name='Название сайта'
    )
    logo = models.ImageField(
        upload_to='site/',
        blank=True,
        null=True,
        verbose_name='Логотип'
    )
    phone_primary = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Основной телефон'
    )
    phone_secondary = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Дополнительный телефон'
    )
    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name='Email'
    )
    address = models.TextField(
        blank=True,
        null=True,
        verbose_name='Адрес'
    )
    telegram_url = models.URLField(
        blank=True,
        null=True,
        verbose_name='Telegram URL'
    )
    vk_url = models.URLField(
        blank=True,
        null=True,
        verbose_name='VK URL'
    )
    registry_number = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Номер в реестре'
    )
    registry_url = models.URLField(
        blank=True,
        null=True,
        verbose_name='Ссылка на реестр'
    )
    national_projects_logo = models.ImageField(
        upload_to='site/',
        blank=True,
        null=True,
        verbose_name='Логотип национальных проектов'
    )
    hero_image = models.ImageField(
        upload_to='site/',
        blank=True,
        null=True,
        verbose_name='Главное изображение'
    )
    # Варианты размеров для hero_image
    hero_image_full_webp = ImageSpecField(
        source='hero_image',
        processors=[SmartCropProcessor(1920, 1080)],
        format='WEBP',
        options={'quality': 85}
    )
    hero_image_thumb_webp = ImageSpecField(
        source='hero_image',
        processors=[ResizeToFill(400, 225)],
        format='WEBP',
        options={'quality': 75}
    )
    hero_image_placeholder_webp = ImageSpecField(
        source='hero_image',
        processors=[NoOpProcessor()],
        format='WEBP',
        options={'quality': 50}
    )
    hero_title = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Заголовок главной секции'
    )
    hero_subtitle = models.TextField(
        blank=True,
        null=True,
        verbose_name='Подзаголовок главной секции'
    )
    base_plan_image = models.ImageField(
        upload_to='site/',
        blank=True,
        null=True,
        verbose_name='Изображение плана базы'
    )
    # Варианты размеров для base_plan_image
    plan_full_webp = ImageSpecField(
        source='base_plan_image',
        processors=[ResizeToFill(1388, 972)],
        format='WEBP',
        options={'quality': 85}
    )
    plan_thumb_webp = ImageSpecField(
        source='base_plan_image',
        processors=[ResizeToFill(400, 280)],
        format='WEBP',
        options={'quality': 75}
    )
    plan_placeholder_webp = ImageSpecField(
        source='base_plan_image',
        processors=[NoOpProcessor()],
        format='WEBP',
        options={'quality': 50}
    )
    base_plan_description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание плана базы'
    )

    class Meta:
        verbose_name = 'Настройки сайта'
        verbose_name_plural = 'Настройки сайта'

    def __str__(self):
        return self.site_name


class Statistic(models.Model):
    """Статистика для отображения на сайте"""
    number = models.CharField(
        max_length=50,
        verbose_name='Число',
        help_text='Число для отображения (например: "150" или "50+")'
    )
    label = models.CharField(
        max_length=255,
        verbose_name='Подпись',
        help_text='Текст под числом (например: "Гостей в год")'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание',
        help_text='Дополнительное описание статистики'
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
        verbose_name = 'Статистика'
        verbose_name_plural = 'Статистика'
        ordering = ['order', 'id']

    def __str__(self):
        return f'{self.number} - {self.label}'


class GalleryImage(models.Model):
    """Изображения для галереи"""
    POSITION_CHOICES = [
        ('main', 'Основная галерея'),
        ('hero', 'Hero секция'),
        ('lodge', 'Размещение'),
        ('activity', 'Активности'),
    ]

    COLUMN_CHOICES = [
        ('left', 'Левая колонка'),
        ('center', 'Центральная колонка'),
        ('right', 'Правая колонка'),
    ]

    image = models.ImageField(
        upload_to='gallery/',
        verbose_name='Изображение'
    )
    image_webp = ImageSpecField(
        source='image',
        processors=[NoOpProcessor()],
        format='WEBP',
        options={'quality': 85}
    )
    # Новые варианты размеров для Gallery изображений
    gallery_large_webp = ImageSpecField(
        source='image',
        processors=[ResizeToFill(1410, 940)],
        format='WEBP',
        options={'quality': 85}
    )
    gallery_medium_webp = ImageSpecField(
        source='image',
        processors=[ResizeToFill(626, 456)],
        format='WEBP',
        options={'quality': 80}
    )
    gallery_small_webp = ImageSpecField(
        source='image',
        processors=[ResizeToFill(414, 296)],
        format='WEBP',
        options={'quality': 75}
    )
    gallery_placeholder_webp = ImageSpecField(
        source='image',
        processors=[NoOpProcessor()],
        format='WEBP',
        options={'quality': 50}
    )
    alt_text = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Alt текст',
        help_text='Альтернативный текст для изображения'
    )
    position = models.CharField(
        max_length=20,
        choices=POSITION_CHOICES,
        default='main',
        verbose_name='Позиция',
        help_text='Где отображается изображение'
    )
    column = models.CharField(
        max_length=10,
        choices=COLUMN_CHOICES,
        blank=True,
        null=True,
        verbose_name='Колонка',
        help_text='Колонка для основной галереи (left/center/right). Используется только для position="main"'
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок сортировки'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активно'
    )

    class Meta:
        verbose_name = 'Изображение галереи'
        verbose_name_plural = 'Изображения галереи'
        ordering = ['position', 'column', 'order', 'id']

    def __str__(self):
        return f'{self.get_position_display()} - {self.alt_text or "Без названия"}'


class HeroSection(SEOMixin):
    """Hero секция (главная секция сайта)"""
    DISPLAY_TYPE_CHOICES = [
        ('image', 'Изображение'),
        ('video', 'Видео'),
        ('slider', 'Слайдер'),
    ]

    title = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Заголовок',
        help_text='Заголовок Hero секции'
    )
    subtitle = models.TextField(
        blank=True,
        null=True,
        verbose_name='Подзаголовок',
        help_text='Подзаголовок Hero секции'
    )
    preview_image = models.ImageField(
        upload_to='hero/',
        blank=True,
        null=True,
        verbose_name='Превью изображение',
        help_text='Изображение для превью (постер для видео)'
    )
    preview_image_webp = ImageSpecField(
        source='preview_image',
        processors=[ResizeToFill(1920, 1080)],
        format='WEBP',
        options={'quality': 85}
    )
    # Новые варианты размеров для preview_image
    preview_image_hero_full_webp = ImageSpecField(
        source='preview_image',
        processors=[SmartCropProcessor(1920, 1080)],
        format='WEBP',
        options={'quality': 85}
    )
    preview_image_hero_thumb_webp = ImageSpecField(
        source='preview_image',
        processors=[ResizeToFill(400, 225)],
        format='WEBP',
        options={'quality': 75}
    )
    preview_image_hero_placeholder_webp = ImageSpecField(
        source='preview_image',
        processors=[NoOpProcessor()],
        format='WEBP',
        options={'quality': 50}
    )
    promo_video = models.FileField(
        upload_to='hero/videos/',
        blank=True,
        null=True,
        verbose_name='Промо видео',
        help_text='Видеофайл для Hero секции'
    )
    video_poster = models.ImageField(
        upload_to='hero/posters/',
        blank=True,
        null=True,
        verbose_name='Постер видео',
        help_text='Постер для видео (отображается до загрузки видео)'
    )
    display_type = models.CharField(
        max_length=20,
        choices=DISPLAY_TYPE_CHOICES,
        default='image',
        verbose_name='Тип отображения',
        help_text='Как отображать Hero секцию'
    )
    autoplay_video = models.BooleanField(
        default=True,
        verbose_name='Автовоспроизведение видео',
        help_text='Автоматически воспроизводить видео'
    )
    loop_video = models.BooleanField(
        default=True,
        verbose_name='Зациклить видео',
        help_text='Повторять видео по кругу'
    )
    mute_video = models.BooleanField(
        default=True,
        verbose_name='Без звука',
        help_text='Воспроизводить видео без звука'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активна',
        help_text='Отображать Hero секцию на сайте'
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок сортировки'
    )

    class Meta:
        verbose_name = 'Hero секция'
        verbose_name_plural = 'Hero секции'
        ordering = ['order', 'id']

    def __str__(self):
        return self.title or f'Hero секция #{self.id}'

    def clean(self):
        """Валидация Singleton - только одна активная запись"""
        if self.is_active:
            # Проверяем, есть ли другие активные Hero секции
            other_active = HeroSection.objects.filter(is_active=True).exclude(pk=self.pk)
            if other_active.exists():
                raise ValidationError(
                    'Может быть только одна активная Hero секция. '
                    'Сначала деактивируйте другие активные секции.'
                )

    def save(self, *args, **kwargs):
        """Переопределение save для валидации Singleton"""
        self.full_clean()
        super().save(*args, **kwargs)

    @classmethod
    def get_active_hero(cls):
        """Возвращает активную Hero секцию"""
        try:
            return cls.objects.filter(is_active=True).first()
        except cls.DoesNotExist:
            return None


class HeroImage(models.Model):
    """Изображения для Hero секции (для слайдера)"""
    hero_section = models.ForeignKey(
        HeroSection,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Hero секция'
    )
    image = models.ImageField(
        upload_to='hero/images/',
        verbose_name='Изображение'
    )
    image_webp = ImageSpecField(
        source='image',
        processors=[ResizeToFill(1920, 1080)],
        format='WEBP',
        options={'quality': 85}
    )
    # Новые варианты размеров для Hero изображений
    hero_full_webp = ImageSpecField(
        source='image',
        processors=[SmartCropProcessor(1920, 1080)],
        format='WEBP',
        options={'quality': 85}
    )
    hero_thumb_webp = ImageSpecField(
        source='image',
        processors=[ResizeToFill(400, 225)],
        format='WEBP',
        options={'quality': 75}
    )
    hero_placeholder_webp = ImageSpecField(
        source='image',
        processors=[NoOpProcessor()],
        format='WEBP',
        options={'quality': 50}
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
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активно'
    )
    transition_duration = models.PositiveIntegerField(
        default=5000,
        verbose_name='Длительность перехода (мс)',
        help_text='Время показа изображения в слайдере в миллисекундах'
    )

    class Meta:
        verbose_name = 'Изображение Hero секции'
        verbose_name_plural = 'Изображения Hero секции'
        ordering = ['order', 'id']

    def __str__(self):
        return f'{self.hero_section} - Изображение {self.order}'
