<script setup>
// Страница мероприятий
// Каждая страница сама запрашивает свои данные через composables

const config = useRuntimeConfig()
const siteUrl = config.public.siteUrl

// Загружаем данные через composable
const { eventTypes, eventTypesError } = useEvents()

// Логируем ошибки
if (eventTypesError.value) {
  console.error('Error loading events:', eventTypesError.value)
}

// SEO мета-теги
useHead({
  title: 'Мероприятия - Строгановские Просторы',
  meta: [
    {
      name: 'description',
      content: 'Организация мероприятий на базе отдыха Строгановские Просторы',
    },
  ],
  link: [
    { rel: 'canonical', href: `${siteUrl}/events` },
  ],
})
</script>

<template>
  <div class="min-h-screen bg-background text-foreground">
    <div class="container mx-auto px-6 py-12 md:px-8">
      <h1 class="mb-8 text-4xl font-serif text-primary">Мероприятия</h1>

      <!-- Список типов мероприятий -->
      <div v-if="eventTypes && eventTypes.length > 0" class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        <div
          v-for="eventType in eventTypes"
          :key="eventType.id"
          class="rounded-lg border border-border bg-card p-6 shadow-md"
        >
          <h2 class="mb-2 text-2xl font-serif text-primary">{{ eventType.name }}</h2>
          <p class="text-muted-foreground">{{ eventType.description }}</p>
          <!-- Добавьте больше полей по необходимости -->
        </div>
      </div>

      <!-- Состояние загрузки/ошибки -->
      <div v-else-if="eventTypesError" class="text-center text-red-500">
        Ошибка загрузки мероприятий
      </div>
      <div v-else class="text-center text-muted-foreground">
        Загрузка...
      </div>
    </div>
  </div>
</template>

