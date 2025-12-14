# Backend для сайта "Строгановские Просторы"

Django + DRF проект для управления контентом базы отдыха.

## Установка и запуск

### 1. Создание виртуального окружения

```bash
python3 -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate
```

### 2. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 3. Применение миграций

```bash
python manage.py migrate
```

### 4. Создание суперпользователя (опционально)

```bash
python manage.py createsuperuser
```

### 5. Запуск сервера разработки

```bash
python manage.py runserver
```

Сервер будет доступен по адресу: http://127.0.0.1:8000/

Админ-панель: http://127.0.0.1:8000/admin/

## Структура проекта

- `config/` - основные настройки проекта
- `core/` - базовые модели и утилиты
- `lodges/` - модели размещения
- `activities/` - модели активностей
- `events/` - модели мероприятий
- `news/` - модели новостей
- `restaurant/` - модели ресторана

## Этапы разработки

См. `BACKEND_IMPLEMENTATION_PLAN.md` для детального плана реализации.

