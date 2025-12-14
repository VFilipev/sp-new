# Техническое задание для Backend на Django + DRF

## Обзор проекта

Проект представляет собой сайт базы отдыха "Строгановские Просторы" с информацией о размещении, услугах, мероприятиях, новостях и контактах.

---

## Модели данных

### 1. Модель `LodgeType` (Тип размещения)
**Назначение:** Категории размещения (Коттеджи, Модульные дома)

**Поля:**
- `id` - Primary Key (автоматически)
- `name` - CharField(max_length=100) - Название типа (например, "Коттеджи", "Модульные дома")
- `slug` - SlugField(unique=True) - URL-слаг для SEO
- `subtitle` - TextField - Подзаголовок/краткое описание
- `hero_image` - ImageField - Главное изображение для карточки типа (оригинал)
- `hero_image_webp` - ImageField(upload_to='lodge-types/webp/', blank=True, null=True) - WebP версия hero изображения (опционально)
- `description` - TextField(blank=True) - Полное описание типа размещения
- `is_active` - BooleanField(default=True) - Активен ли тип для отображения
- `order` - PositiveIntegerField(default=0) - Порядок сортировки

**Мета:**
- `verbose_name = "Тип размещения"`
- `verbose_name_plural = "Типы размещения"`
- `ordering = ['order', 'name']`

---

### 2. Модель `Lodge` (Размещение/Дом)
**Назначение:** Конкретные дома/коттеджи/модули для размещения

**Поля:**
- `id` - Primary Key (автоматически)
- `lodge_type` - ForeignKey(LodgeType, on_delete=CASCADE, related_name='lodges')
- `name` - CharField(max_length=200) - Название дома (например, "Дом Кузнеца", "Модуль Панорама")
- `slug` - SlugField(unique=True) - URL-слаг
- `description` - TextField - Описание дома (минимум 200-300 символов для SEO)
- `short_description` - CharField(max_length=200, blank=True) - Краткое описание для карточек (100-150 символов)
- `capacity` - PositiveIntegerField - Вместимость (количество человек)
- `area` - PositiveIntegerField - Площадь в м²
- `price_from` - DecimalField(max_digits=10, decimal_places=2) - Цена от (в рублях)
- `location_description` - TextField(blank=True) - Описание местоположения для SEO
- `is_active` - BooleanField(default=True) - Доступен для бронирования
- `order` - PositiveIntegerField(default=0) - Порядок сортировки
- `created_at` - DateTimeField(auto_now_add=True)
- `updated_at` - DateTimeField(auto_now=True)
- **SEO поля (из SEOMixin):**
  - `meta_title` - CharField(max_length=60, blank=True)
  - `meta_description` - TextField(max_length=160, blank=True)
  - `meta_keywords` - CharField(max_length=255, blank=True)
  - `og_title` - CharField(max_length=95, blank=True)
  - `og_description` - TextField(max_length=200, blank=True)
  - `og_image` - ImageField(upload_to='og-images/', blank=True, null=True)
  - `canonical_url` - URLField(blank=True)
  - `robots_meta` - CharField(max_length=50, default='index, follow')

**Мета:**
- `verbose_name = "Размещение"`
- `verbose_name_plural = "Размещения"`
- `ordering = ['lodge_type', 'order', 'name']`

**Методы:**
- `get_schema_org_json()` - возвращает JSON-LD для Schema.org типа LodgingBusiness
- `get_breadcrumbs()` - возвращает массив breadcrumbs для навигации

---

### 3. Модель `LodgeImage` (Изображения размещения)
**Назначение:** Фотографии домов/коттеджей

**Поля:**
- `id` - Primary Key (автоматически)
- `lodge` - ForeignKey(Lodge, on_delete=CASCADE, related_name='images')
- `image` - ImageField(upload_to='lodges/') - Изображение (оригинал)
- `image_webp` - ImageField(upload_to='lodges/webp/', blank=True, null=True) - WebP версия изображения (опционально, для оптимизации)
- `alt_text` - CharField(max_length=200, blank=True) - Альтернативный текст для SEO
- `order` - PositiveIntegerField(default=0) - Порядок сортировки

**Мета:**
- `verbose_name = "Изображение размещения"`
- `verbose_name_plural = "Изображения размещения"`
- `ordering = ['lodge', 'order']`

**Примечание:** Поле `image_webp` опционально. Рекомендуется использовать автоматическую генерацию WebP через `django-imagekit` (см. раздел "Оптимизация изображений").

---

### 4. Модель `Activity` (Активность/Услуга)
**Назначение:** Активные и спокойные виды отдыха

**Поля:**
- `id` - Primary Key (автоматически)
- `category` - CharField(max_length=20, choices=[('active', 'Активный отдых'), ('peaceful', 'Спокойный отдых')])
- `title` - CharField(max_length=200) - Название активности
- `slug` - SlugField(unique=True) - URL-слаг
- `description` - TextField - Описание активности
- `image` - ImageField(upload_to='activities/') - Основное изображение (оригинал)
- `image_webp` - ImageField(upload_to='activities/webp/', blank=True, null=True) - WebP версия изображения (опционально)
- `video` - FileField(upload_to='activities/videos/', blank=True, null=True) - Видео (опционально)
- `is_active` - BooleanField(default=True) - Активна ли услуга
- `order` - PositiveIntegerField(default=0) - Порядок сортировки
- `created_at` - DateTimeField(auto_now_add=True)
- `updated_at` - DateTimeField(auto_now=True)

**Мета:**
- `verbose_name = "Активность"`
- `verbose_name_plural = "Активности"`
- `ordering = ['category', 'order', 'title']`

---

### 5. Модель `EventType` (Тип мероприятия)
**Назначение:** Категории мероприятий (Свадьбы, Юбилеи, Корпоративы, Выпускные)

**Поля:**
- `id` - Primary Key (автоматически)
- `title` - CharField(max_length=200) - Название типа мероприятия
- `slug` - SlugField(unique=True) - URL-слаг
- `description` - TextField - Описание типа мероприятия
- `image` - ImageField(upload_to='events/') - Изображение для карточки (оригинал)
- `image_webp` - ImageField(upload_to='events/webp/', blank=True, null=True) - WebP версия изображения (опционально)
- `is_active` - BooleanField(default=True) - Активен ли тип
- `order` - PositiveIntegerField(default=0) - Порядок сортировки

**Мета:**
- `verbose_name = "Тип мероприятия"`
- `verbose_name_plural = "Типы мероприятий"`
- `ordering = ['order', 'title']`

---

### 6. Модель `News` (Новости)
**Назначение:** Новости и анонсы базы отдыха

**Поля:**
- `id` - Primary Key (автоматически)
- `title` - CharField(max_length=200) - Заголовок новости
- `slug` - SlugField(unique=True) - URL-слаг
- `content` - TextField(blank=True) - Полный текст новости (для детальной страницы, минимум 300 символов для SEO)
- `short_description` - CharField(max_length=500, blank=True) - Краткое описание для карточек (150-200 символов)
- `excerpt` - TextField(max_length=300, blank=True) - Краткое извлечение для превью (200-300 символов)
- `image` - ImageField(upload_to='news/') - Изображение новости (оригинал)
- `image_webp` - ImageField(upload_to='news/webp/', blank=True, null=True) - WebP версия изображения (опционально)
- `published_at` - DateTimeField - Дата публикации
- `is_published` - BooleanField(default=False) - Опубликована ли новость
- `reading_time` - PositiveIntegerField(blank=True, null=True) - Время чтения в минутах (автоматический расчет)
- **SEO поля (из SEOMixin):**
  - `meta_title` - CharField(max_length=60, blank=True)
  - `meta_description` - TextField(max_length=160, blank=True)
  - `meta_keywords` - CharField(max_length=255, blank=True)
  - `og_title` - CharField(max_length=95, blank=True)
  - `og_description` - TextField(max_length=200, blank=True)
  - `og_image` - ImageField(upload_to='og-images/', blank=True, null=True)
  - `canonical_url` - URLField(blank=True)
  - `robots_meta` - CharField(max_length=50, default='index, follow')

**Мета:**
- `verbose_name = "Новость"`
- `verbose_name_plural = "Новости"`
- `ordering = ['-published_at', '-created_at']`

**Методы:**
- `get_schema_org_json()` - возвращает JSON-LD для Schema.org типа NewsArticle
- `calculate_reading_time()` - автоматически рассчитывает время чтения (200 слов/минуту)

---

### 7. Модель `Restaurant` (Ресторан)
**Назначение:** Информация о ресторане

**Поля:**
- `id` - Primary Key (автоматически)
- `title` - CharField(max_length=200, default='Ресторан') - Название
- `description` - TextField - Описание ресторана
- `is_active` - BooleanField(default=True) - Активен ли ресторан
- `created_at` - DateTimeField(auto_now_add=True)
- `updated_at` - DateTimeField(auto_now=True)

**Мета:**
- `verbose_name = "Ресторан"`
- `verbose_name_plural = "Ресторан"`

---

### 8. Модель `RestaurantImage` (Изображения ресторана)
**Назначение:** Фотографии интерьера ресторана

**Поля:**
- `id` - Primary Key (автоматически)
- `restaurant` - ForeignKey(Restaurant, on_delete=CASCADE, related_name='images')
- `image` - ImageField(upload_to='restaurant/') - Изображение (оригинал)
- `image_webp` - ImageField(upload_to='restaurant/webp/', blank=True, null=True) - WebP версия изображения (опционально)
- `alt_text` - CharField(max_length=200, blank=True) - Альтернативный текст
- `order` - PositiveIntegerField(default=0) - Порядок сортировки
- `created_at` - DateTimeField(auto_now_add=True)

**Мета:**
- `verbose_name = "Изображение ресторана"`
- `verbose_name_plural = "Изображения ресторана"`
- `ordering = ['order']`

---

### 9. Модель `MealType` (Тип питания)
**Назначение:** Завтрак, Обед, Ужин

**Поля:**
- `id` - Primary Key (автоматически)
- `name` - CharField(max_length=50) - Название (Завтрак, Обед, Ужин)
- `icon_name` - CharField(max_length=50, blank=True) - Название иконки (Coffee, Sun, Moon)
- `description` - CharField(max_length=200) - Описание времени (например, "Плотный завтрак с 8:00")
- `time_start` - TimeField(blank=True, null=True) - Время начала
- `order` - PositiveIntegerField(default=0) - Порядок сортировки
- `created_at` - DateTimeField(auto_now_add=True)

**Мета:**
- `verbose_name = "Тип питания"`
- `verbose_name_plural = "Типы питания"`
- `ordering = ['order']`

---

### 10. Модель `RestaurantBenefit` (Преимущества ресторана)
**Назначение:** Список преимуществ ресторана

**Поля:**
- `id` - Primary Key (автоматически)
- `restaurant` - ForeignKey(Restaurant, on_delete=CASCADE, related_name='benefits')
- `text` - CharField(max_length=500) - Текст преимущества
- `order` - PositiveIntegerField(default=0) - Порядок сортировки
- `created_at` - DateTimeField(auto_now_add=True)

**Мета:**
- `verbose_name = "Преимущество ресторана"`
- `verbose_name_plural = "Преимущества ресторана"`
- `ordering = ['order']`

---

### 11. Модель `Statistic` (Статистика)
**Назначение:** Цифры и факты о базе отдыха

**Поля:**
- `id` - Primary Key (автоматически)
- `number` - CharField(max_length=50) - Число/цифра (может быть "20", "200", "365" и т.д.)
- `label` - CharField(max_length=200) - Подпись (например, "гектаров природы")
- `description` - CharField(max_length=500) - Описание
- `is_active` - BooleanField(default=True) - Отображать ли статистику
- `order` - PositiveIntegerField(default=0) - Порядок сортировки

**Мета:**
- `verbose_name = "Статистика"`
- `verbose_name_plural = "Статистика"`
- `ordering = ['order']`

---

### 12. Модель `HeroSection` (Главная секция)
**Назначение:** Hero-секция на главной странице с поддержкой слайдера изображений и проморолика

**Поля:**
- `id` - Primary Key (автоматически)
- `title` - CharField(max_length=200) - Главный заголовок (например, "уютные коттеджи и глэмпинг")
- `subtitle` - TextField - Подзаголовок/описание (например, "Уединённый отдых в хвойном лесу...")
- `preview_image` - ImageField(upload_to='hero/preview/', blank=True, null=True) - Изображение для превью (показывается до загрузки видео или как fallback)
- `preview_image_webp` - ImageField(upload_to='hero/preview/webp/', blank=True, null=True) - WebP версия превью изображения
- `promo_video` - FileField(upload_to='hero/videos/', blank=True, null=True) - Проморолик (видео файл)
- `video_poster` - ImageField(upload_to='hero/posters/', blank=True, null=True) - Постер для видео (превью кадр)
- `is_active` - BooleanField(default=True) - Активна ли секция
- `display_type` - CharField(max_length=20, choices=[
    ('image', 'Одно изображение'),
    ('slider', 'Слайдер изображений'),
    ('video', 'Видео с превью'),
    ('slider_video', 'Слайдер + видео')
], default='image') - Тип отображения
- `autoplay_video` - BooleanField(default=False) - Автовоспроизведение видео
- `loop_video` - BooleanField(default=True) - Зацикливание видео
- `mute_video` - BooleanField(default=True) - Беззвучное воспроизведение
- `order` - PositiveIntegerField(default=0) - Порядок сортировки (если несколько вариантов)
- **SEO поля (из SEOMixin):**
  - `meta_title` - CharField(max_length=60, blank=True)
  - `meta_description` - TextField(max_length=160, blank=True)
  - `og_title` - CharField(max_length=95, blank=True)
  - `og_description` - TextField(max_length=200, blank=True)
  - `og_image` - ImageField(upload_to='hero/og/', blank=True, null=True)

**Мета:**
- `verbose_name = "Hero секция"`
- `verbose_name_plural = "Hero секции"`
- `ordering = ['order', '-created_at']`

**Особенность:** Должна быть только одна активная запись для главной страницы. Можно использовать Singleton pattern или проверку в save().

**Валидация в модели:**
```python
def save(self, *args, **kwargs):
    if self.is_active:
        # Деактивировать все остальные записи
        HeroSection.objects.filter(is_active=True).exclude(pk=self.pk).update(is_active=False)
    super().save(*args, **kwargs)
```

**Методы:**
- `get_active_hero()` - класс-метод для получения активной Hero секции

---

### 13. Модель `HeroImage` (Изображения для Hero слайдера)
**Назначение:** Изображения для слайдера в Hero-секции

**Поля:**
- `id` - Primary Key (автоматически)
- `hero_section` - ForeignKey(HeroSection, on_delete=CASCADE, related_name='images')
- `image` - ImageField(upload_to='hero/slider/') - Изображение (оригинал)
- `image_webp` - ImageField(upload_to='hero/slider/webp/', blank=True, null=True) - WebP версия изображения (опционально)
- `alt_text` - CharField(max_length=200, blank=True) - Альтернативный текст для SEO
- `order` - PositiveIntegerField(default=0) - Порядок сортировки в слайдере
- `is_active` - BooleanField(default=True) - Отображать ли изображение
- `transition_duration` - PositiveIntegerField(default=5000) - Длительность показа в миллисекундах (для автопрокрутки)
- `created_at` - DateTimeField(auto_now_add=True)

**Мета:**
- `verbose_name = "Изображение Hero секции"`
- `verbose_name_plural = "Изображения Hero секции"`
- `ordering = ['hero_section', 'order']`

**Примечание:** Используется только если `display_type` = 'slider' или 'slider_video'

---

### 14. Модель `GalleryImage` (Изображения галереи)
**Назначение:** Фотографии для галереи на главной странице

**Поля:**
- `id` - Primary Key (автоматически)
- `image` - ImageField(upload_to='gallery/') - Изображение (оригинал)
- `image_webp` - ImageField(upload_to='gallery/webp/', blank=True, null=True) - WebP версия изображения (опционально)
- `alt_text` - CharField(max_length=200, blank=True) - Альтернативный текст
- `position` - CharField(max_length=20, choices=[('left', 'Левая колонка'), ('center', 'Центральная колонка'), ('right', 'Правая колонка')], default='center')
- `order` - PositiveIntegerField(default=0) - Порядок сортировки внутри колонки
- `is_active` - BooleanField(default=True) - Отображать ли изображение
- `created_at` - DateTimeField(auto_now_add=True)

**Мета:**
- `verbose_name = "Изображение галереи"`
- `verbose_name_plural = "Изображения галереи"`
- `ordering = ['position', 'order']`

---


---

## API Endpoints (DRF)

### Базовые настройки
- Использовать `rest_framework` для создания API
- Настроить CORS для работы с Vue frontend
- Использовать пагинацию для списков
- Добавить фильтрацию и поиск где необходимо

### Список эндпоинтов:

1. **GET /api/lodge-types/** - Список типов размещения
2. **GET /api/lodge-types/{id}/** - Детали типа размещения (с SEO данными)
3. **GET /api/lodges/** - Список размещений (с фильтрацией по типу)
4. **GET /api/lodges/{id}/** - Детали размещения с изображениями, SEO данными и Schema.org
5. **GET /api/activities/** - Список активностей (с фильтрацией по категории: active/peaceful)
6. **GET /api/activities/{id}/** - Детали активности (с SEO данными)
7. **GET /api/event-types/** - Список типов мероприятий
8. **GET /api/event-types/{id}/** - Детали типа мероприятия (с SEO данными и Schema.org)
9. **GET /api/news/** - Список новостей (только опубликованные)
10. **GET /api/news/{id}/** - Детали новости (с SEO данными и Schema.org)
11. **GET /api/restaurant/** - Информация о ресторане (Singleton, с SEO данными и Schema.org)
12. **GET /api/restaurant/images/** - Изображения ресторана
13. **GET /api/restaurant/meal-types/** - Типы питания
14. **GET /api/restaurant/benefits/** - Преимущества ресторана
15. **GET /api/statistics/** - Статистика базы отдыха
16. **GET /api/gallery/** - Изображения галереи (с фильтрацией по позиции)
17. **GET /api/hero/** - Hero секция для главной страницы (Singleton, с изображениями/видео)
18. **GET /api/site-settings/** - Настройки сайта (Singleton, с SEO данными для главной)
19. **GET /api/sitemap/** - Данные для генерации sitemap.xml
20. **GET /api/robots.txt** - Генерация robots.txt
21. **POST /api/bookings/** - Создание бронирования (если реализовано)

---

## Сериализаторы (DRF Serializers)

### Основные сериализаторы:

1. **LodgeTypeSerializer** - с вложенными размещениями и SEO данными
2. **LodgeSerializer** - с изображениями, SEO данными и Schema.org JSON-LD
3. **LodgeImageSerializer**
4. **ActivitySerializer** - с SEO данными
5. **EventTypeSerializer** - с SEO данными и Schema.org JSON-LD
6. **NewsSerializer** - с краткой и полной версией, SEO данными и Schema.org JSON-LD
7. **RestaurantSerializer** - с изображениями, типами питания, преимуществами и SEO данными
8. **StatisticSerializer**
9. **GalleryImageSerializer**
10. **HeroSectionSerializer** - с изображениями слайдера, видео и SEO данными
11. **HeroImageSerializer**
12. **SiteSettingsSerializer** - с SEO данными для главной страницы
13. **BookingSerializer** (если реализовано)

### SEO поля в сериализаторах:

**Пример для LodgeSerializer:**
```python
class LodgeSerializer(serializers.ModelSerializer):
    # SEO поля
    meta_title = serializers.CharField(required=False, allow_blank=True)
    meta_description = serializers.CharField(required=False, allow_blank=True)
    og_title = serializers.CharField(required=False, allow_blank=True)
    og_description = serializers.CharField(required=False, allow_blank=True)
    og_image_url = serializers.SerializerMethodField()
    canonical_url = serializers.CharField(required=False, allow_blank=True)
    robots_meta = serializers.CharField(required=False)

    # Schema.org JSON-LD
    schema_org = serializers.SerializerMethodField()

    # Breadcrumbs
    breadcrumbs = serializers.SerializerMethodField()

    def get_og_image_url(self, obj):
        if obj.og_image:
            return obj.og_image.url
        if obj.images.first():
            return obj.images.first().image.url
        return None

    def get_schema_org(self, obj):
        return obj.get_schema_org_json()

    def get_breadcrumbs(self, obj):
        return obj.get_breadcrumbs()

    class Meta:
        model = Lodge
        fields = [
            'id', 'name', 'slug', 'description', 'short_description',
            'capacity', 'area', 'price_from', 'images',
            # SEO поля
            'meta_title', 'meta_description', 'meta_keywords',
            'og_title', 'og_description', 'og_image_url',
            'canonical_url', 'robots_meta',
            # Дополнительные SEO данные
            'schema_org', 'breadcrumbs'
        ]
```

**Пример для HeroSectionSerializer:**
```python
class HeroImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    image_webp_url = serializers.SerializerMethodField()

    def get_image_url(self, obj):
        return obj.image.url if obj.image else None

    def get_image_webp_url(self, obj):
        return obj.image_webp.url if obj.image_webp else None

    class Meta:
        model = HeroImage
        fields = ['id', 'image_url', 'image_webp_url', 'alt_text', 'order', 'transition_duration']

class HeroSectionSerializer(serializers.ModelSerializer):
    images = HeroImageSerializer(many=True, read_only=True)
    preview_image_url = serializers.SerializerMethodField()
    preview_image_webp_url = serializers.SerializerMethodField()
    video_poster_url = serializers.SerializerMethodField()
    promo_video_url_field = serializers.SerializerMethodField()

    def get_preview_image_url(self, obj):
        return obj.preview_image.url if obj.preview_image else None

    def get_preview_image_webp_url(self, obj):
        return obj.preview_image_webp.url if obj.preview_image_webp else None

    def get_video_poster_url(self, obj):
        if obj.video_poster:
            return obj.video_poster.url
        if obj.preview_image:
            return obj.preview_image.url
        return None

    def get_promo_video_url_field(self, obj):
        # Возвращаем URL загруженного файла или внешний URL
        if obj.promo_video:
            return obj.promo_video.url
        if obj.promo_video_url:
            return obj.promo_video_url
        return None

    class Meta:
        model = HeroSection
        fields = [
            'id', 'title', 'title_line2', 'subtitle',
            'display_type', 'preview_image_url', 'preview_image_webp_url',
            'promo_video_url_field', 'video_poster_url',
            'autoplay_video', 'loop_video', 'mute_video',
            'images', 'is_active',
            # SEO поля
            'meta_title', 'meta_description',
            'og_title', 'og_description', 'og_image'
        ]
```

**Автозаполнение SEO полей:**
- Если `meta_title` пустое - использовать `name` или `title`
- Если `meta_description` пустое - использовать `description` или `short_description`
- Если `og_title` пустое - использовать `meta_title`
- Если `og_description` пустое - использовать `meta_description`

---

## ViewSets и Views

### Рекомендуемая структура:

- Использовать `ModelViewSet` для CRUD операций (где нужно)
- Использовать `ReadOnlyModelViewSet` для только чтения
- Использовать `GenericAPIView` для кастомных эндпоинтов (например, SiteSettings)
- Добавить фильтры через `django-filter` для:
  - Lodges (по типу, цене, вместимости)
  - Activities (по категории)
  - News (по дате публикации)
  - Gallery (по позиции)

---

## Административная панель (Django Admin)

### Настройка админки:

1. Зарегистрировать все модели
2. Создать `Inline` для:
   - `LodgeImage` в `Lodge`
   - `HeroImage` в `HeroSection`
   - `RestaurantImage`, `MealType`, `RestaurantBenefit` в `Restaurant`
3. Добавить фильтры и поиск
4. Настроить отображение списков с полезными полями
5. Добавить действия (actions) для массовых операций
6. **Для HeroSection:** Настроить валидацию, чтобы была только одна активная запись

---

## Медиа файлы

### Настройки:

- `MEDIA_URL = '/media/'`
- `MEDIA_ROOT = os.path.join(BASE_DIR, 'media')`
- Организовать загрузку по папкам:
  - `lodges/` - изображения размещений
  - `activities/` - изображения и видео активностей
  - `events/` - изображения мероприятий
  - `news/` - изображения новостей
  - `restaurant/` - изображения ресторана
  - `gallery/` - изображения галереи
  - `hero/` - Hero секция:
    - `hero/preview/` - превью изображения
    - `hero/slider/` - изображения для слайдера
    - `hero/videos/` - проморолики
    - `hero/posters/` - постеры для видео
    - `hero/og/` - Open Graph изображения
  - `settings/` - логотипы и общие изображения

---

## Дополнительные требования

### 1. SEO оптимизация

#### 1.1. Базовая модель для SEO мета-данных

Создать абстрактную модель `SEOMixin` для переиспользования:

```python
from django.db import models

class SEOMixin(models.Model):
    """Абстрактная модель для SEO мета-данных"""
    # Основные мета-теги
    meta_title = models.CharField(
        max_length=60,
        blank=True,
        help_text="Title для страницы (до 60 символов, рекомендуется 50-60)"
    )
    meta_description = models.TextField(
        max_length=160,
        blank=True,
        help_text="Meta description (до 160 символов, рекомендуется 150-160)"
    )
    meta_keywords = models.CharField(
        max_length=255,
        blank=True,
        help_text="Ключевые слова через запятую (необязательно, Google не использует)"
    )

    # Open Graph для социальных сетей
    og_title = models.CharField(
        max_length=95,
        blank=True,
        help_text="Open Graph title (до 95 символов)"
    )
    og_description = models.TextField(
        max_length=200,
        blank=True,
        help_text="Open Graph description (до 200 символов)"
    )
    og_image = models.ImageField(
        upload_to='og-images/',
        blank=True,
        null=True,
        help_text="Изображение для Open Graph (рекомендуется 1200x630px)"
    )

    # Дополнительные SEO поля
    canonical_url = models.URLField(
        blank=True,
        help_text="Canonical URL (если отличается от стандартного)"
    )
    robots_meta = models.CharField(
        max_length=50,
        default='index, follow',
        choices=[
            ('index, follow', 'Индексировать, следовать ссылкам'),
            ('noindex, follow', 'Не индексировать, следовать ссылкам'),
            ('index, nofollow', 'Индексировать, не следовать ссылкам'),
            ('noindex, nofollow', 'Не индексировать, не следовать ссылкам'),
        ],
        help_text="Robots meta тег"
    )

    class Meta:
        abstract = True
```

#### 1.2. SEO поля для существующих моделей

Добавить SEO поля в следующие модели (через наследование от `SEOMixin` или напрямую):

**Модели, требующие SEO:**
- `LodgeType` - для страниц типов размещения
- `Lodge` - для страниц конкретных домов
- `Activity` - для страниц активностей
- `EventType` - для страниц типов мероприятий
- `News` - для страниц новостей
- `Restaurant` - для страницы ресторана

**Автогенерация мета-данных:**
- Если `meta_title` пустое - использовать `title` или `name`
- Если `meta_description` пустое - использовать `description` или `short_description`
- Если `og_title` пустое - использовать `meta_title`
- Если `og_description` пустое - использовать `meta_description`
- Если `og_image` пустое - использовать основное `image`

#### 1.3. Структурированные данные (Schema.org / JSON-LD)

Добавить методы для генерации JSON-LD разметки в моделях:

**Для Lodge (Accommodation):**
```python
def get_schema_org_json(self):
    """Генерирует JSON-LD для Schema.org типа LodgingBusiness"""
    return {
        "@context": "https://schema.org",
        "@type": "LodgingBusiness",
        "name": self.name,
        "description": self.description,
        "image": self.image.url if self.image else None,
        "priceRange": f"от {self.price_from} руб.",
        "numberOfRooms": 1,
        "amenityFeature": [
            {"@type": "LocationFeatureSpecification", "name": "Вместимость", "value": self.capacity}
        ]
    }
```

**Для News (Article):**
```python
def get_schema_org_json(self):
    """Генерирует JSON-LD для Schema.org типа NewsArticle"""
    return {
        "@context": "https://schema.org",
        "@type": "NewsArticle",
        "headline": self.title,
        "description": self.short_description or self.content[:200],
        "image": self.image.url if self.image else None,
        "datePublished": self.published_at.isoformat(),
        "author": {
            "@type": "Organization",
            "name": "Строгановские Просторы"
        }
    }
```

**Для EventType (Event):**
```python
def get_schema_org_json(self):
    """Генерирует JSON-LD для Schema.org типа Event"""
    return {
        "@context": "https://schema.org",
        "@type": "Event",
        "name": self.title,
        "description": self.description,
        "image": self.image.url if self.image else None,
        "organizer": {
            "@type": "Organization",
            "name": "Строгановские Просторы"
        }
    }
```

**Для Restaurant (Restaurant):**
```python
def get_schema_org_json(self):
    """Генерирует JSON-LD для Schema.org типа Restaurant"""
    return {
        "@context": "https://schema.org",
        "@type": "Restaurant",
        "name": self.title,
        "description": self.description,
        "servesCuisine": "Русская кухня",
        "address": {
            "@type": "PostalAddress",
            "addressLocality": "Ильинский",
            "addressRegion": "Пермский край"
        }
    }
```

**Для Organization (главная страница):**
Создать отдельную модель или использовать SiteSettings для организации:
```python
{
    "@context": "https://schema.org",
    "@type": "TouristAttraction",
    "name": "Строгановские Просторы",
    "description": "База отдыха на берегу Камского моря",
    "address": {...},
    "telephone": "+7 (902) 643-92-94",
    "priceRange": "$$"
}
```

#### 1.4. Breadcrumbs (Хлебные крошки)

Добавить модель или метод для генерации breadcrumbs:

```python
def get_breadcrumbs(self):
    """Генерирует breadcrumbs для страницы"""
    return [
        {"name": "Главная", "url": "/"},
        {"name": self.lodge_type.name, "url": f"/lodges/{self.lodge_type.slug}/"},
        {"name": self.name, "url": f"/lodges/{self.slug}/"}
    ]
```

Или использовать JSON-LD для breadcrumbs:
```python
def get_breadcrumb_schema(self):
    """JSON-LD для BreadcrumbList"""
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [...]
    }
```

#### 1.5. Рекомендации по текстовой оптимизации

**Для полей описаний:**
- `description` - основное описание (минимум 200-300 символов для SEO)
- `short_description` - краткое описание для карточек (100-150 символов)
- `meta_description` - специально для SEO (150-160 символов)

**Правила заполнения:**
1. **Title (meta_title):**
   - 50-60 символов (оптимально)
   - Включать ключевые слова в начале
   - Уникальный для каждой страницы
   - Формат: "Название | Строгановские Просторы"

2. **Description (meta_description):**
   - 150-160 символов
   - Призыв к действию
   - Включать ключевые слова естественно
   - Уникальный для каждой страницы

3. **Keywords:**
   - Необязательно (Google не использует)
   - Можно оставить для внутренней аналитики
   - 5-10 ключевых фраз через запятую

4. **Alt-тексты для изображений:**
   - Описательные, не просто "фото"
   - Включать контекст (например, "Коттедж Дом Кузнеца на базе отдыха Строгановские Просторы")
   - Максимум 125 символов

#### 1.6. Sitemap.xml

Настроить автоматическую генерацию sitemap.xml:

```python
# Использовать django.contrib.sitemaps
from django.contrib.sitemaps import Sitemap

class LodgeSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Lodge.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at
```

**Приоритеты для разных страниц:**
- Главная: 1.0
- Типы размещения: 0.9
- Конкретные размещения: 0.8
- Новости: 0.7
- Активности: 0.6
- Мероприятия: 0.6

#### 1.7. Robots.txt

Настроить robots.txt:
```
User-agent: *
Allow: /
Disallow: /admin/
Disallow: /api/
Sitemap: https://stroganovprostor.ru/sitemap.xml
```

#### 1.8. Дополнительные SEO поля в моделях

**Для News:**
- `excerpt` - краткое извлечение для превью (200-300 символов)
- `reading_time` - время чтения статьи (автоматический расчет)

**Для Lodge:**
- `features` - список особенностей (ManyToMany или JSONField)
- `location_description` - описание местоположения для SEO

**Для Activity:**
- `duration` - продолжительность активности
- `difficulty_level` - уровень сложности

### 2. Оптимизация изображений

#### Подход 1: Автоматическая генерация WebP (Рекомендуется)
Использовать библиотеку `django-imagekit` для автоматической генерации WebP версий из оригиналов:

**Преимущества:**
- Автоматическая генерация при сохранении
- Не требует ручной загрузки WebP
- Поддержка различных размеров (thumbnails, resizing)
- Кэширование сгенерированных изображений

**Пример использования:**
```python
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, Format

class LodgeImage(models.Model):
    image = models.ImageField(upload_to='lodges/')

    # Автоматическая генерация WebP
    image_webp = ImageSpecField(
        source='image',
        processors=[ResizeToFill(1200, 800), Format('webp')],
        format='WEBP',
        options={'quality': 85}
    )
```

#### Подход 2: Отдельное поле image_webp (Альтернативный)
Использовать опциональное поле `image_webp` для ручной загрузки или кастомной генерации:

**Преимущества:**
- Полный контроль над процессом
- Возможность ручной оптимизации
- Гибкость в выборе качества

**Недостатки:**
- Требует дополнительной логики для генерации
- Больше места в базе данных

**Рекомендация:** Использовать **Подход 1** (django-imagekit) для автоматизации, но оставить поле `image_webp` как опциональное для случаев, когда нужен больший контроль.

#### Генерация WebP через сигналы Django
Альтернативный вариант - использовать Django signals для автоматической генерации:

```python
from django.db.models.signals import post_save
from PIL import Image
import os

def generate_webp(sender, instance, **kwargs):
    if instance.image:
        img = Image.open(instance.image.path)
        webp_path = instance.image.path.rsplit('.', 1)[0] + '.webp'
        img.save(webp_path, 'WEBP', quality=85)
        instance.image_webp = webp_path.replace(settings.MEDIA_ROOT, '')
        instance.save(update_fields=['image_webp'])
```

---

## Зависимости (requirements.txt)

```
Django>=4.2,<5.0
djangorestframework>=3.14.0
django-cors-headers>=4.0.0
Pillow>=10.0.0
django-filter>=23.0
django-solo>=2.0.0  # для Singleton модели SiteSettings
django-redis>=5.0.0  # для кэширования
python-decouple>=3.8  # для настроек
django-imagekit>=5.0.0  # для автоматической генерации WebP и оптимизации изображений
django-meta>=2.0.0  # для генерации мета-тегов (опционально)
```

**Примечание:** `django-imagekit` требует установки `Pillow` и поддерживает автоматическую генерацию WebP, thumbnails и других вариантов изображений.

---

## Структура проекта Django

```
backend/
├── manage.py
├── requirements.txt
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   ├── __init__.py
│   ├── lodges/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── admin.py
│   ├── activities/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── admin.py
│   ├── events/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── admin.py
│   ├── news/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── admin.py
│   ├── restaurant/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── admin.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── models.py  # SiteSettings, Statistic, GalleryImage, HeroSection, HeroImage
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── admin.py
│   └── bookings/  # опционально
│       ├── __init__.py
│       ├── models.py
│       ├── serializers.py
│       ├── views.py
│       ├── urls.py
│       └── admin.py
└── media/
    └── ...
```

---

## Примечания

1. Все текстовые поля должны поддерживать кириллицу
2. **Изображения и WebP:**
   - Рекомендуется использовать `django-imagekit` для автоматической генерации WebP
   - Поля `image_webp` опциональны и могут использоваться для ручной загрузки или кастомной логики
   - В сериализаторах проверять наличие `image_webp`, если нет - возвращать оригинал `image`
   - Frontend должен поддерживать fallback на оригинальное изображение, если WebP недоступен
3. **SEO оптимизация:**
   - Все публичные страницы должны иметь уникальные `meta_title` и `meta_description`
   - Использовать автозаполнение SEO полей из основных полей, если они не заполнены
   - Генерировать Schema.org JSON-LD для всех основных сущностей (Lodge, News, Event, Restaurant)
   - Frontend должен вставлять JSON-LD в `<script type="application/ld+json">` теги
   - Open Graph изображения должны быть минимум 1200x630px для лучшего отображения в соцсетях
   - Регулярно проверять и обновлять SEO данные
4. Для production использовать PostgreSQL вместо SQLite
5. Настроить CORS для работы с Vue frontend
6. Добавить rate limiting для API (защита от спама)
7. Рассмотреть возможность добавления системы уведомлений о новых бронированиях
8. **Сериализаторы изображений:** Добавить методы для возврата WebP версии с fallback на оригинал:
   ```python
   def get_image_webp_url(self, obj):
       if obj.image_webp:
           return obj.image_webp.url
       return obj.image.url if obj.image else None
   ```
9. **Текстовая оптимизация:**
   - Минимальная длина `description` - 200-300 символов для лучшего SEO
   - Использовать ключевые слова естественно, без переспама
   - Структурировать текст с использованием подзаголовков (H2, H3)
   - Добавлять внутренние ссылки между связанными страницами
   - Регулярно обновлять контент для поддержания актуальности

---

## Примеры данных для заполнения (Fixtures)

Создать JSON fixtures для начального заполнения:
- Hero секция (HeroSection) с изображениями/видео
- Типы размещения (Коттеджи, Модульные дома) - LodgeType
- Примеры размещений - Lodge
- Активности (активный и спокойный отдых)
- Типы мероприятий
- Статистика
- Настройки сайта

---

## Использование SEO данных на Frontend (Vue)

### 1. Мета-теги в `<head>`

**Пример для Vue Router:**
```javascript
// В router/index.js или в компоненте страницы
import { useHead } from '@vueuse/head'

// Получаем данные из API
const { data: lodge } = await fetch(`/api/lodges/${id}/`).then(r => r.json())

// Устанавливаем мета-теги
useHead({
  title: lodge.meta_title || lodge.name,
  meta: [
    {
      name: 'description',
      content: lodge.meta_description || lodge.short_description
    },
    {
      name: 'keywords',
      content: lodge.meta_keywords
    },
    {
      name: 'robots',
      content: lodge.robots_meta
    },
    // Open Graph
    {
      property: 'og:title',
      content: lodge.og_title || lodge.meta_title || lodge.name
    },
    {
      property: 'og:description',
      content: lodge.og_description || lodge.meta_description
    },
    {
      property: 'og:image',
      content: lodge.og_image_url || lodge.images[0]?.image
    },
    {
      property: 'og:type',
      content: 'website'
    },
    // Canonical
    {
      rel: 'canonical',
      href: lodge.canonical_url || `${window.location.origin}/lodges/${lodge.slug}/`
    }
  ]
})
```

### 1.1. Использование HeroSection на Frontend

**Пример компонента HeroSection.vue:**
```vue
<template>
  <section class="relative flex min-h-screen items-center justify-center overflow-hidden">
    <!-- Фон: слайдер изображений или видео -->
    <div class="absolute inset-0 z-0">
      <!-- Вариант 1: Слайдер изображений -->
      <div v-if="hero.display_type === 'slider' || hero.display_type === 'slider_video'"
           class="hero-slider">
        <img
          v-for="(img, index) in hero.images"
          :key="img.id"
          :src="img.image_webp_url || img.image_url"
          :alt="img.alt_text"
          class="hero-slide"
          :class="{ 'active': currentSlide === index }"
        />
      </div>

      <!-- Вариант 2: Одно изображение -->
      <img
        v-else-if="hero.display_type === 'image'"
        :src="hero.preview_image_webp_url || hero.preview_image_url"
        alt="Hero image"
        class="h-full w-full object-cover"
      />

      <!-- Вариант 3: Видео с превью -->
      <div v-else-if="hero.display_type === 'video' || hero.display_type === 'slider_video'"
           class="hero-video-container">
        <video
          ref="videoRef"
          :src="hero.promo_video_url_field"
          :poster="hero.video_poster_url || hero.preview_image_url"
          :autoplay="hero.autoplay_video"
          :loop="hero.loop_video"
          :muted="hero.mute_video"
          playsinline
          class="h-full w-full object-cover"
        />
        <button
          v-if="!hero.autoplay_video"
          @click="playVideo"
          class="play-button"
        >
          ▶
        </button>
      </div>

      <!-- Градиент overlay -->
      <div class="absolute inset-0 bg-gradient-to-b from-primary/70 via-primary/50 to-primary/70" />
    </div>

    <!-- Контент -->
    <div class="absolute bottom-0 left-0 right-0 z-10 pb-12 md:pb-16">
      <div class="container mx-auto px-6 md:px-8">
        <div class="grid items-end gap-8 md:grid-cols-2">
          <div class="animate-fade-in">
            <h1 class="text-2xl font-light leading-relaxed text-primary-foreground md:text-3xl">
              {{ hero.title }}
              <br v-if="hero.title_line2" />
              {{ hero.title_line2 }}
            </h1>
          </div>
          <div class="animate-slide-in-right rounded-2xl border border-primary-foreground/20 bg-primary-foreground/10 p-6 backdrop-blur-md">
            <p class="text-base leading-relaxed text-primary-foreground md:text-lg">
              {{ hero.subtitle }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'

const props = defineProps({
  hero: {
    type: Object,
    required: true
  }
})

const videoRef = ref(null)
const currentSlide = ref(0)
let slideInterval = null

const playVideo = () => {
  if (videoRef.value) {
    videoRef.value.play()
  }
}

// Автопрокрутка слайдера
onMounted(() => {
  if ((props.hero.display_type === 'slider' || props.hero.display_type === 'slider_video')
      && props.hero.images?.length > 1) {
    slideInterval = setInterval(() => {
      currentSlide.value = (currentSlide.value + 1) % props.hero.images.length
    }, props.hero.images[currentSlide.value]?.transition_duration || 5000)
  }
})

onBeforeUnmount(() => {
  if (slideInterval) {
    clearInterval(slideInterval)
  }
})
</script>
```

**Получение данных HeroSection:**
```javascript
// В HomeView.vue или главном компоненте
import { ref, onMounted } from 'vue'

const hero = ref(null)

onMounted(async () => {
  const response = await fetch('/api/hero/')
  hero.value = await response.json()
})
```

### 2. Schema.org JSON-LD

**Добавление структурированных данных:**
```vue
<template>
  <div>
    <!-- Контент страницы -->
    <script type="application/ld+json" v-html="schemaJson"></script>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  schemaData: Object
})

const schemaJson = computed(() => {
  return JSON.stringify(props.schemaData, null, 2)
})
</script>
```

### 3. Breadcrumbs

**Отображение хлебных крошек:**
```vue
<template>
  <nav aria-label="breadcrumb">
    <ol>
      <li v-for="(crumb, index) in breadcrumbs" :key="index">
        <router-link v-if="index < breadcrumbs.length - 1" :to="crumb.url">
          {{ crumb.name }}
        </router-link>
        <span v-else>{{ crumb.name }}</span>
      </li>
    </ol>
  </nav>
</template>
```

### 4. Sitemap.xml генерация

**На backend создать view для sitemap:**
```python
from django.contrib.sitemaps import Sitemap
from django.http import HttpResponse
from django.template.loader import render_to_string

def sitemap_xml(request):
    sitemaps = {
        'lodges': LodgeSitemap(),
        'news': NewsSitemap(),
        'activities': ActivitySitemap(),
    }
    xml = render_to_string('sitemap.xml', {'sitemaps': sitemaps})
    return HttpResponse(xml, content_type='application/xml')
```

---

## Дополнительные рекомендации по SEO

### 1. Внутренняя перелинковка
- Добавлять ссылки на связанные страницы в описаниях
- Использовать анкоры с ключевыми словами
- Создавать карту сайта для пользователей

### 2. Контент-стратегия
- Регулярно публиковать новости (минимум 1-2 раза в месяц)
- Обновлять описания размещений и активностей
- Добавлять отзывы и рейтинги (можно добавить модель Review)

### 3. Локализация
- Подготовить структуру для мультиязычности (i18n)
- Добавить поля для перевода мета-данных
- Использовать hreflang теги для разных языков

### 4. Производительность
- Оптимизировать изображения (WebP, lazy loading)
- Минифицировать CSS и JS
- Использовать CDN для статических файлов
- Настроить кэширование

### 5. Мониторинг
- Интегрировать Google Search Console
- Настроить аналитику (Google Analytics, Yandex.Metrica)
- Отслеживать позиции по ключевым запросам
- Регулярно проверять индексацию страниц

---

**Дата создания:** 2025-01-27
**Версия:** 2.0 (добавлен раздел SEO оптимизации)

