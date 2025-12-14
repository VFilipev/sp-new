<script setup>
// Компоненты сами запрашивают свои данные через composables
// Это делает архитектуру более модульной и позволяет легко создавать новые роуты

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
    <!-- Компоненты сами запрашивают свои данные -->
    <HeroSection />
    <GalleryStatsSection />
    <LodgeSection />
    <PeacefulRestSection />
    <ActiveRestSection />
    <EventsSection />
    <RestaurantSection />
    <NewsSection />
    <FooterSection />
  </div>
</template>

