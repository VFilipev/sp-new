<script setup>
// Страница конкретной новости
// Используем динамический роут [id].vue

const route = useRoute()
const config = useRuntimeConfig()
const siteUrl = config.public.siteUrl

// Получаем ID из параметров роута
const newsId = route.params.id

// Загружаем данные конкретной новости
const { newsItem, newsItemError } = useNewsItem(newsId)

// Логируем ошибки
if (newsItemError.value) {
  console.error('Error loading news item:', newsItemError.value)
}

// SEO мета-теги
useHead({
  title: computed(() => newsItem.value ? `${newsItem.value.title} - Строгановские Просторы` : 'Новость - Строгановские Просторы'),
  meta: [
    {
      name: 'description',
      content: computed(() => newsItem.value?.excerpt || newsItem.value?.description || 'Новость'),
    },
  ],
  link: [
    { rel: 'canonical', href: `${siteUrl}/news/${newsId}` },
  ],
})
</script>

<template>
  <div class="min-h-screen bg-background text-foreground">
    <div v-if="newsItem" class="container mx-auto px-6 py-12 md:px-8">
      <NuxtLink to="/news" class="mb-4 inline-block text-primary hover:underline">
        ← Назад к новостям
      </NuxtLink>

      <article>
        <h1 class="mb-4 text-4xl font-serif text-primary">{{ newsItem.title }}</h1>
        <div v-if="newsItem.published_at" class="mb-4 text-sm text-muted-foreground">
          {{ new Date(newsItem.published_at).toLocaleDateString('ru-RU') }}
        </div>
        <div class="prose prose-lg max-w-none">
          <p class="text-lg leading-relaxed">{{ newsItem.content || newsItem.description }}</p>
          <!-- Добавьте больше полей по необходимости -->
        </div>
      </article>
    </div>

    <!-- Состояние загрузки/ошибки -->
    <div v-else-if="newsItemError" class="container mx-auto px-6 py-12 text-center text-red-500">
      Ошибка загрузки новости
    </div>
    <div v-else class="container mx-auto px-6 py-12 text-center text-muted-foreground">
      Загрузка...
    </div>
  </div>
</template>

