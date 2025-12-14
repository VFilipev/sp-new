<script setup>
// Страница конкретного домика
// Используем динамический роут [id].vue

const route = useRoute()
const config = useRuntimeConfig()
const siteUrl = config.public.siteUrl

// Получаем ID из параметров роута
const lodgeId = route.params.id

// Загружаем данные конкретного домика
const { lodge, lodgeError } = useLodge(lodgeId)

// Логируем ошибки
if (lodgeError.value) {
  console.error('Error loading lodge:', lodgeError.value)
}

// SEO мета-теги
useHead({
  title: computed(() => lodge.value ? `${lodge.value.name} - Строгановские Просторы` : 'Домик - Строгановские Просторы'),
  meta: [
    {
      name: 'description',
      content: computed(() => lodge.value?.description || 'Информация о домике'),
    },
  ],
  link: [
    { rel: 'canonical', href: `${siteUrl}/lodge/${lodgeId}` },
  ],
})
</script>

<template>
  <div class="min-h-screen bg-background text-foreground">
    <div v-if="lodge" class="container mx-auto px-6 py-12 md:px-8">
      <h1 class="mb-4 text-4xl font-serif text-primary">{{ lodge.name }}</h1>
      <p class="mb-8 text-lg text-muted-foreground">{{ lodge.description }}</p>

      <!-- Добавьте больше информации о домике -->
      <div class="grid gap-6 md:grid-cols-2">
        <!-- Изображения, характеристики и т.д. -->
      </div>
    </div>

    <!-- Состояние загрузки/ошибки -->
    <div v-else-if="lodgeError" class="container mx-auto px-6 py-12 text-center text-red-500">
      Ошибка загрузки домика
    </div>
    <div v-else class="container mx-auto px-6 py-12 text-center text-muted-foreground">
      Загрузка...
    </div>
  </div>
</template>

