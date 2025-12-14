// nuxt.config.js
export default defineNuxtConfig({
  // Режим рендеринга - SSR (Server-Side Rendering)
  ssr: true, // Включен SSR

  // Отключаем экспериментальные функции, которые могут вызывать проблемы с hot reload
  experimental: {
    payloadExtraction: false,
    viewTransition: true,
    watcher: 'chokidar-granular', // Более стабильный watcher
  },

  // Модули
  modules: [
    '@nuxtjs/tailwindcss',
    '@nuxt/image',
    '@pinia/nuxt',
    '@nuxtjs/seo',
    '@nuxtjs/critters',
  ],

  // Критический CSS и preload
  critters: {
    preload: 'swap',
    pruneSource: true,
    compress: true,
  },

  // CSS
  css: ['~/assets/css/main.css'],

  // Алиасы (автоматически настроены, но можно расширить)
  alias: {
    '@': '.',
  },

  // Настройка компонентов (автоимпорт включен по умолчанию)
  components: [
    {
      path: '~/components',
      pathPrefix: false,
    },
  ],

  // Переменные окружения
  runtimeConfig: {
    // Приватные ключи (только на сервере)
    apiSecret: process.env.API_SECRET || '',

    // Публичные ключи (доступны и на клиенте)
    public: {
      apiBase: process.env.API_BASE_URL || 'http://localhost:8000/api',
      siteUrl: process.env.SITE_URL || 'http://localhost:3000',
    },
  },

  // Оптимизация изображений
  image: {
    domains: ['localhost', '45.153.69.10'],
    provider: 'ipx', // Встроенный провайдер
    quality: 100, // Качество по умолчанию (снижено с 80 для лучшего сжатия)
    format: ['webp', 'avif'], // Поддержка современных форматов
  },

  // SEO настройки
  site: {
    // Очищаем URL от символа §, если он там есть
    url: (process.env.SITE_URL || 'http://localhost:3000').replace(/[§]/g, ''),
    name: 'Строгановские Просторы',
    description: 'Уютные коттеджи и глэмпинг на берегу камского моря',
    defaultLocale: 'ru',
  },

  // Настройки sitemap
  sitemap: {
    // Настраиваем hostname, очищая от символа §
    hostname: (process.env.SITE_URL || 'http://localhost:3000').replace(/[§]/g, '').replace(/\/$/, ''),
  },

  // Настройки robots.txt
  robots: {
    allow: ['/'],
    disallow: ['/admin/', '/api/'],
    // Указываем только наш sitemap URL от Django API
    // Файл server/routes/sitemap.xml.js переименован, чтобы модуль не находил его автоматически
    sitemap: (() => {
      const siteUrl = (process.env.SITE_URL || 'http://localhost:3000').replace(/[§]/g, '');
      // Убеждаемся, что URL заканчивается правильно
      return siteUrl.replace(/\/$/, '') + '/api/sitemap.xml';
    })(),
  },


  // Настройки сборки
  nitro: {
    compressPublicAssets: {
      gzip: true,
      brotli: true,
    },
    prerender: {
      crawlLinks: false, // Отключаем автоматический обход ссылок
      failOnError: false, // Не прерывать сборку при ошибках пререндеринга
    },
  },

  // Vite настройки (для совместимости и оптимизации)
  vite: {
    css: {
      preprocessorOptions: {
        scss: {
          additionalData: '@use "@/assets/scss/variables.scss" as *;',
        },
      },
    },
  },

  // App конфигурация
  app: {
    head: {
      charset: 'utf-8',
      viewport: 'width=device-width, initial-scale=1',
      title: 'Строгановские Просторы',
      titleTemplate: '%s - Строгановские Просторы',
      meta: [
        { name: 'description', content: 'Уютные коттеджи и глэмпинг на берегу камского моря. Уединённый отдых в хвойном лесу с европейским уровнем комфорта.' },
        { name: 'keywords', content: 'коттеджи, глэмпинг, отдых, Пермский край, база отдыха, Камское море, активный отдых, спокойный отдых' },
        { name: 'author', content: 'Строгановские Просторы' },
        { name: 'language', content: 'ru' },
        { property: 'og:type', content: 'website' },
        { property: 'og:locale', content: 'ru_RU' },
        { property: 'og:site_name', content: 'Строгановские Просторы' },
        { name: 'twitter:card', content: 'summary_large_image' },
      ],
      link: [
        { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
        { rel: 'canonical', href: process.env.SITE_URL || 'http://localhost:3000' },
        // Preload шрифтов Lato для ускорения отрисовки текста
        { rel: 'preload', as: 'font', type: 'font/ttf', href: '/fonts/Lato-Light.ttf', crossorigin: 'anonymous' },
        { rel: 'preload', as: 'font', type: 'font/ttf', href: '/fonts/Lato-Regular.ttf', crossorigin: 'anonymous' },
        { rel: 'preload', as: 'font', type: 'font/ttf', href: '/fonts/Lato-Medium.ttf', crossorigin: 'anonymous' },
        { rel: 'preload', as: 'font', type: 'font/ttf', href: '/fonts/Lato-SemiBold.ttf', crossorigin: 'anonymous' },
        { rel: 'preload', as: 'font', type: 'font/ttf', href: '/fonts/Lato-Bold.ttf', crossorigin: 'anonymous' },
      ],
    },
  },

  // Совместимость
  compatibilityDate: '2025-07-15',

  // Devtools
  devtools: { enabled: true },
})

