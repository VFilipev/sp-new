# Пошаговое руководство по деплою в продакшн

## Архитектура

```
Интернет (45.153.69.10:8009)
    ↓
Nginx (слушает порт 8009)
    ↓
    ├─→ Nuxt SSR (localhost:3000) - для фронтенда
    └─→ Django API (localhost:8000) - для /api/ и /admin/
```

## Шаг 1: Подготовка сервера

### 1.1. Подключение к серверу
```bash
ssh user@45.153.69.10
```

### 1.2. Установка зависимостей (если не установлены)

```bash
# Python и pip
sudo apt update
sudo apt install python3 python3-pip python3-venv -y

# Node.js и npm (для Nuxt)
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

# PM2 для управления Node.js процессами
sudo npm install -g pm2

# Nginx (если не установлен)
sudo apt install nginx -y

# Gunicorn для Django
pip3 install gunicorn
```

## Шаг 2: Клонирование проекта

```bash
cd /var/www
sudo git clone https://github.com/VFilipev/sp-new.git
sudo chown -R $USER:$USER /var/www/sp-new
cd /var/www/sp-new
```

## Шаг 3: Настройка Django

### 3.1. Создание виртуального окружения

```bash
cd /var/www/sp-new/backend
python3 -m venv venv
source venv/bin/activate
```

### 3.2. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 3.3. Настройка переменных окружения

Создайте файл `.env` в директории `backend/`:

```bash
cd /var/www/sp-new/backend
nano .env
```

Добавьте (если нужно):
```
SECRET_KEY=ваш-секретный-ключ-здесь
DEBUG=False
ALLOWED_HOSTS=45.153.69.10,localhost,127.0.0.1
```

### 3.4. Применение миграций

```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

### 3.5. Создание суперпользователя (если нужно)

```bash
python manage.py createsuperuser
```

## Шаг 4: Настройка Nuxt SSR

### 4.1. Установка зависимостей

```bash
cd /var/www/sp-new/frontend-nuxt/sp-nuxt
npm install
```

### 4.2. Создание переменных окружения

Создайте файл `.env` в директории `frontend-nuxt/sp-nuxt/`:

```bash
cd /var/www/sp-new/frontend-nuxt/sp-nuxt
nano .env
```

Добавьте:
```
NODE_ENV=production
PORT=3000
API_BASE_URL=http://localhost:8000/api
SITE_URL=http://45.153.69.10:8009
```

### 4.3. Сборка проекта

```bash
npm run build
```

### 4.4. Создание директории для логов

```bash
cd /var/www/sp-new
mkdir -p logs
```

## Шаг 5: Настройка PM2 для Nuxt

### 5.1. Обновление конфигурации PM2

Файл `ecosystem.config.js` уже настроен. Проверьте пути:

```bash
cd /var/www/sp-new
cat ecosystem.config.js
```

### 5.2. Запуск Nuxt через PM2

```bash
cd /var/www/sp-new
pm2 start ecosystem.config.js
pm2 save
pm2 startup  # Следуйте инструкциям для автозапуска
```

### 5.3. Проверка статуса

```bash
pm2 status
pm2 logs nuxt-ssr
```

## Шаг 6: Настройка Gunicorn для Django

### 6.1. Создание systemd сервиса

Создайте файл `/etc/systemd/system/sp-new-django.service`:

```bash
sudo nano /etc/systemd/system/sp-new-django.service
```

Вставьте следующее содержимое:

```ini
[Unit]
Description=SP New Django Gunicorn daemon
After=network.target

[Service]
User=ваш-пользователь
Group=www-data
WorkingDirectory=/var/www/sp-new/backend
Environment="PATH=/var/www/sp-new/backend/venv/bin"
ExecStart=/var/www/sp-new/backend/venv/bin/gunicorn \
    --workers 3 \
    --bind 127.0.0.1:8000 \
    --access-logfile /var/www/sp-new/logs/gunicorn-access.log \
    --error-logfile /var/www/sp-new/logs/gunicorn-error.log \
    config.wsgi:application

[Install]
WantedBy=multi-user.target
```

**Важно:** Замените `ваш-пользователь` на ваше имя пользователя (можно узнать командой `whoami`).

### 6.2. Запуск сервиса

```bash
sudo systemctl daemon-reload
sudo systemctl enable sp-new-django
sudo systemctl start sp-new-django
sudo systemctl status sp-new-django
```

### 6.3. Проверка логов

```bash
sudo journalctl -u sp-new-django -f
```

## Шаг 7: Настройка Nginx

### 7.1. Создание конфигурации

Создайте файл `/etc/nginx/sites-available/sp-new`:

```bash
sudo nano /etc/nginx/sites-available/sp-new
```

Вставьте следующую конфигурацию:

```nginx
# Upstream для Nuxt SSR
upstream nuxt_backend {
    server 127.0.0.1:3000;
    keepalive 64;
}

# Upstream для Django API
upstream django_backend {
    server 127.0.0.1:8000;
    keepalive 64;
}

server {
    listen 8009;
    server_name 45.153.69.10;

    # Увеличение размера загружаемых файлов
    client_max_body_size 20M;

    # Логирование
    access_log /var/log/nginx/sp-new-access.log;
    error_log /var/log/nginx/sp-new-error.log;

    # Nuxt SSR - все запросы кроме /api/ и /admin/
    location / {
        proxy_pass http://nuxt_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        proxy_read_timeout 300s;
        proxy_connect_timeout 75s;
    }

    # Django API
    location /api/ {
        proxy_pass http://django_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 300s;
        proxy_connect_timeout 75s;
    }

    # Django Admin
    location /admin/ {
        proxy_pass http://django_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Статические файлы Django
    location /static/ {
        alias /var/www/sp-new/backend/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Медиа файлы Django
    location /media/ {
        alias /var/www/sp-new/backend/media/;
        expires 30d;
        add_header Cache-Control "public";
    }
}
```

### 7.2. Активация конфигурации

```bash
sudo ln -s /etc/nginx/sites-available/sp-new /etc/nginx/sites-enabled/
sudo nginx -t
```

Если тест прошел успешно:

```bash
sudo systemctl reload nginx
```

### 7.3. Проверка статуса Nginx

```bash
sudo systemctl status nginx
```

## Шаг 8: Настройка файрвола (если используется)

```bash
# Разрешить порт 8009
sudo ufw allow 8009/tcp
sudo ufw reload
```

## Шаг 9: Проверка работы

### 9.1. Проверка сервисов

```bash
# Проверка PM2
pm2 status

# Проверка Django
sudo systemctl status sp-new-django

# Проверка Nginx
sudo systemctl status nginx

# Проверка портов
sudo ss -tulpn | grep -E ':(3000|8000|8009)'
```

### 9.2. Проверка в браузере

Откройте в браузере:
- Главная страница: `http://45.153.69.10:8009`
- API: `http://45.153.69.10:8009/api/`
- Admin: `http://45.153.69.10:8009/admin/`

## Шаг 10: Полезные команды для управления

### Перезапуск сервисов

```bash
# Перезапуск Django
sudo systemctl restart sp-new-django

# Перезапуск Nuxt
pm2 restart nuxt-ssr

# Перезапуск Nginx
sudo systemctl reload nginx
```

### Просмотр логов

```bash
# Логи Django
sudo journalctl -u sp-new-django -f
tail -f /var/www/sp-new/logs/gunicorn-error.log

# Логи Nuxt
pm2 logs nuxt-ssr

# Логи Nginx
sudo tail -f /var/log/nginx/sp-new-error.log
```

### Обновление кода

```bash
cd /var/www/sp-new
git pull origin master

# Пересборка Nuxt
cd frontend-nuxt/sp-nuxt
npm install
npm run build
pm2 restart nuxt-ssr

# Перезапуск Django (если были изменения в коде)
cd /var/www/sp-new/backend
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart sp-new-django
```

## Troubleshooting

### Проблема: Сайт не открывается

1. Проверьте, что все сервисы запущены:
   ```bash
   pm2 status
   sudo systemctl status sp-new-django
   sudo systemctl status nginx
   ```

2. Проверьте логи:
   ```bash
   pm2 logs nuxt-ssr
   sudo journalctl -u sp-new-django -n 50
   sudo tail -n 50 /var/log/nginx/sp-new-error.log
   ```

3. Проверьте порты:
   ```bash
   sudo ss -tulpn | grep -E ':(3000|8000|8009)'
   ```

### Проблема: CORS ошибки

Проверьте настройки CORS в `backend/config/settings.py` - должны быть добавлены `http://45.153.69.10:8009`

### Проблема: 502 Bad Gateway

1. Проверьте, что Django и Nuxt запущены:
   ```bash
   sudo systemctl status sp-new-django
   pm2 status
   ```

2. Проверьте, что они слушают правильные порты:
   ```bash
   sudo ss -tulpn | grep -E ':(3000|8000)'
   ```

### Проблема: Статические файлы не загружаются

1. Убедитесь, что выполнили `collectstatic`:
   ```bash
   cd /var/www/sp-new/backend
   source venv/bin/activate
   python manage.py collectstatic --noinput
   ```

2. Проверьте права доступа:
   ```bash
   sudo chown -R www-data:www-data /var/www/sp-new/backend/staticfiles
   sudo chmod -R 755 /var/www/sp-new/backend/staticfiles
   ```

## Безопасность

⚠️ **Важно для продакшена:**

1. Измените `SECRET_KEY` в Django settings
2. Установите `DEBUG = False`
3. Настройте `ALLOWED_HOSTS`
4. Рассмотрите возможность использования HTTPS (Let's Encrypt)
5. Настройте регулярные бэкапы базы данных

## Автоматизация обновлений

Можно создать скрипт для автоматического обновления:

```bash
#!/bin/bash
# /var/www/sp-new/update.sh

cd /var/www/sp-new
git pull origin master

# Обновление Nuxt
cd frontend-nuxt/sp-nuxt
npm install
npm run build
pm2 restart nuxt-ssr

# Обновление Django
cd /var/www/sp-new/backend
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart sp-new-django

echo "Обновление завершено!"
```

Сделайте скрипт исполняемым:
```bash
chmod +x /var/www/sp-new/update.sh
```

