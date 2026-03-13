#!/bin/bash

# Скрипт для автоматического обновления проекта на сервере

set -euo pipefail  # Остановка при ошибке и неинициализированных переменных

echo "🔄 Начинаем обновление проекта..."

cd /var/www/sp-new

echo "📥 Получаем последние изменения из Git..."
git pull origin master

echo "🔨 Обновляем Nuxt..."
cd frontend-nuxt/sp-nuxt

# Гарантируем корректную версию Node.js для Nuxt/Vite (crypto.hash и др. API)
export NVM_DIR="${NVM_DIR:-$HOME/.nvm}"
if [ ! -s "$NVM_DIR/nvm.sh" ]; then
  echo "❌ nvm не найден: $NVM_DIR/nvm.sh"
  exit 1
fi

# shellcheck disable=SC1090
source "$NVM_DIR/nvm.sh"
nvm install 22 >/dev/null
nvm use 22 >/dev/null

echo "ℹ️ Node/NPM окружение:"
echo "   PATH=$PATH"
echo "   node: $(which node)"
echo "   npm:  $(which npm)"
echo "   node version: $(node -v)"
echo "   npm version:  $(npm -v)"

if [ "$(node -e "const c=require('node:crypto'); process.stdout.write(typeof c.hash)")" != "function" ]; then
  echo "❌ В текущем Node отсутствует crypto.hash, сборка Nuxt будет падать"
  exit 1
fi

npm ci
npm run build
pm2 restart nuxt-ssr --update-env

echo "🐍 Обновляем Django..."
cd /var/www/sp-new/backend
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart sp-new-django

echo "✅ Обновление завершено успешно!"

