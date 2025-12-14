<script setup>
// Страница списка домиков
// Каждая страница сама запрашивает свои данные через composables

const config = useRuntimeConfig()
const siteUrl = config.public.siteUrl

// Загружаем данные через composable
const { lodges, lodgesError } = useLodges()
const { types, typesError } = useLodgeTypes()

// Логируем ошибки
if (lodgesError.value) {
  console.error('Error loading lodges:', lodgesError.value)
}
if (typesError.value) {
  console.error('Error loading lodge types:', typesError.value)
}

// SEO мета-теги
useHead({
  title: 'Домики - Строгановские Просторы',
  meta: [
    {
      name: 'description',
      content: 'Выберите уютный домик для отдыха на базе Строгановские Просторы',
    },
  ],
  link: [
    { rel: 'canonical', href: `${siteUrl}/lodge` },
  ],
})
</script>

<template>
  <div class="min-h-screen bg-background text-foreground">
    <div class="container mx-auto px-6 py-12 md:px-8">
      <h1 class="mb-8 text-4xl font-serif text-primary">Наши домики</h1>

      <!-- Фильтры по типам -->
      <div v-if="types && types.length > 0" class="mb-8 flex gap-4">
        <button
          v-for="type in types"
          :key="type.id"
          class="rounded-lg border border-border px-4 py-2 transition-colors hover:bg-primary hover:text-primary-foreground"
        >
          {{ type.name }}
        </button>
      </div>

      <!-- Список домиков -->
      <div v-if="lodges && lodges.length > 0" class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        <div
          v-for="lodge in lodges"
          :key="lodge.id"
          class="rounded-lg border border-border bg-card p-6 shadow-md"
        >
          <h2 class="mb-2 text-2xl font-serif text-primary">{{ lodge.name }}</h2>
          <p class="text-muted-foreground">{{ lodge.description }}</p>
          <!-- Добавьте больше полей по необходимости -->
        </div>
      </div>

      <!-- Состояние загрузки/ошибки -->
      <div v-else-if="lodgesError" class="text-center text-red-500">
        Ошибка загрузки домиков
      </div>
      <div v-else class="text-center text-muted-foreground">
        Загрузка...
      </div>
    </div>
  </div>
</template>

