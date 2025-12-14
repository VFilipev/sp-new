#!/bin/bash

# Скрипт для автоматического обновления проекта на сервере

set -e  # Остановка при ошибке

echo "🔄 Начинаем обновление проекта..."

cd /var/www/sp-new

echo "📥 Получаем последние изменения из Git..."
git pull origin master

echo "🔨 Обновляем Nuxt..."
cd frontend-nuxt/sp-nuxt
npm install
npm run build
pm2 restart nuxt-ssr

echo "🐍 Обновляем Django..."
cd /var/www/sp-new/backend
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart sp-new-django

echo "✅ Обновление завершено успешно!"

