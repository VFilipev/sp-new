<script setup>
// Страница новостей
// Каждая страница сама запрашивает свои данные через composables

const config = useRuntimeConfig()
const siteUrl = config.public.siteUrl

// Загружаем данные через composable
const { newsList, newsError } = useNews()

// Логируем ошибки
if (newsError.value) {
  console.error('Error loading news:', newsError.value)
}

// SEO мета-теги
useHead({
  title: 'Новости - Строгановские Просторы',
  meta: [
    {
      name: 'description',
      content: 'Новости и события базы отдыха Строгановские Просторы',
    },
  ],
  link: [
    { rel: 'canonical', href: `${siteUrl}/news` },
  ],
})
</script>

<template>
  <div class="min-h-screen bg-background text-foreground">
    <div class="container mx-auto px-6 py-12 md:px-8">
      <h1 class="mb-8 text-4xl font-serif text-primary">Новости</h1>

      <!-- Список новостей -->
      <div v-if="newsList && newsList.length > 0" class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        <article
          v-for="item in newsList"
          :key="item.id"
          class="rounded-lg border border-border bg-card p-6 shadow-md"
        >
          <h2 class="mb-2 text-2xl font-serif text-primary">{{ item.title }}</h2>
          <p class="mb-4 text-muted-foreground">{{ item.excerpt || item.description }}</p>
          <NuxtLink
            :to="`/news/${item.id}`"
            class="text-primary hover:underline"
          >
            Читать далее →
          </NuxtLink>
        </article>
      </div>

      <!-- Состояние загрузки/ошибки -->
      <div v-else-if="newsError" class="text-center text-red-500">
        Ошибка загрузки новостей
      </div>
      <div v-else class="text-center text-muted-foreground">
        Загрузка...
      </div>
    </div>
  </div>
</template>

