// PM2 конфигурация для Nuxt SSR
module.exports = {
  apps: [{
    name: 'nuxt-ssr',
    script: './frontend-nuxt/sp-nuxt/.output/server/index.mjs',
    instances: 2, // Количество процессов (рекомендуется: количество CPU ядер)
    exec_mode: 'cluster', // Кластерный режим для лучшей производительности
    env: {
      NODE_ENV: 'production',
      PORT: 3000,
      API_BASE_URL: process.env.API_BASE_URL || 'http://localhost:8000/api',
      SITE_URL: process.env.SITE_URL || 'http://45.153.69.10:8009',
    },
    // Автоперезапуск при ошибках
    autorestart: true,
    // Максимальное использование памяти (MB)
    max_memory_restart: '1G',
    // Логирование
    error_file: './logs/nuxt-error.log',
    out_file: './logs/nuxt-out.log',
    log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
    // Перезапуск при изменении файлов (только для разработки)
    watch: false,
  }]
}

