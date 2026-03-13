<script setup>
// Компоненты сами запрашивают свои данные через composables
// Это делает архитектуру более модульной и позволяет легко создавать новые роуты
const {
  isAdmin,
  adminName,
  isEditMode,
  pending: adminStatusPending,
  toggleEditMode,
} = useAdminEditMode()

const config = useRuntimeConfig()
const siteUrl = config.public.siteUrl
const apiBase = config.public.apiBase

// Prefetch для улучшения производительности
useHead({
  link: [
    // Предзагрузка критических ресурсов
    { rel: 'preconnect', href: apiBase },
    { rel: 'dns-prefetch', href: apiBase },
  ],
})

// SEO мета-теги
useHead({
  title: 'Строгановские Просторы - Коттеджи и глэмпинг',
  meta: [
    {
      name: 'description',
      content: 'Уютные коттеджи и глэмпинг на берегу камского моря. Уединённый отдых в хвойном лесу с европейским уровнем комфорта.',
    },
  ],
  link: [
    { rel: 'canonical', href: siteUrl },
  ],
})

// Open Graph и Twitter Cards
useSeoMeta({
  title: 'Строгановские Просторы - Коттеджи и глэмпинг',
  description: 'Уютные коттеджи и глэмпинг на берегу камского моря. Уединённый отдых в хвойном лесу с европейским уровнем комфорта.',
  ogTitle: 'Строгановские Просторы',
  ogDescription: 'Уютные коттеджи и глэмпинг на берегу камского моря',
  ogImage: `${siteUrl}/images/hero-cottages.jpg`,
  ogUrl: siteUrl,
  ogType: 'website',
  ogLocale: 'ru_RU',
  twitterCard: 'summary_large_image',
  twitterTitle: 'Строгановские Просторы',
  twitterDescription: 'Уютные коттеджи и глэмпинг на берегу камского моря',
  twitterImage: `${siteUrl}/images/hero-cottages.jpg`,
})

// Структурированные данные (JSON-LD)
useStructuredData({
  '@context': 'https://schema.org',
  '@type': 'TouristAttraction',
  name: 'Строгановские Просторы',
  description: 'Уютные коттеджи и глэмпинг на берегу камского моря. Уединённый отдых в хвойном лесу с европейским уровнем комфорта.',
  url: siteUrl,
  image: `${siteUrl}/images/hero-cottages.jpg`,
  address: {
    '@type': 'PostalAddress',
    addressCountry: 'RU',
    addressRegion: 'Пермский край',
  },
  offers: {
    '@type': 'Offer',
    priceCurrency: 'RUB',
  },
})
</script>

<template>
  <div class="min-h-screen bg-background text-foreground">
    <div
      v-if="isAdmin"
      class="fixed right-4 top-4 z-[60] flex items-center gap-2 rounded-full border border-primary/20 bg-background/95 p-1 shadow-lg backdrop-blur"
    >
      <span class="px-2 text-xs text-muted-foreground">
        {{ adminName ? `Админ: ${adminName}` : "Админ" }}
      </span>
      <button
        class="rounded-full px-3 py-2 text-xs font-semibold transition-colors"
        :class="
          isEditMode
            ? 'bg-primary text-primary-foreground'
            : 'bg-muted text-foreground hover:bg-muted/80'
        "
        :disabled="adminStatusPending"
        @click="toggleEditMode"
      >
        {{ isEditMode ? "Режим редактирования: ВКЛ" : "Режим редактирования: ВЫКЛ" }}
      </button>
    </div>

    <!-- Критичные компоненты для первого рендера - загружаются сразу -->
    <HeroSection :edit-mode="isEditMode" />

    <!-- GalleryStatsSection обернут в ClientOnly, так как он использует API gallery,
         который генерирует варианты изображений на лету и блокирует SSR на 4+ секунды -->
    <ClientOnly>
      <GalleryStatsSection :edit-mode="isEditMode" />
    </ClientOnly>

    <!-- Компоненты ниже первого экрана - lazy loading для ускорения SSR -->
    <!-- Используем ClientOnly для компонентов, которые не критичны для SEO -->
    <ClientOnly>
      <LazyLodgeSection />
      <LazyPeacefulRestSection />
      <LazyActiveRestSection />
      <LazyEventsSection />
      <LazyRestaurantSection />
      <LazyNewsSection />
    </ClientOnly>

    <!-- Footer всегда рендерится для SEO -->
    <LazyFooterSection />
  </div>
</template>

