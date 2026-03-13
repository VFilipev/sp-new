<script setup>
import { computed, defineAsyncComponent, onBeforeUnmount, ref, watch } from 'vue'
import { useLodgeTypes } from '~/composables/useLodges'

// Lazy loading для тяжелого модального компонента
const LodgeModal = defineAsyncComponent(() =>
  import('~/components/lodge/LodgeModal.vue')
)

const { types: lodgeTypes } = useLodgeTypes()

const selectedType = ref(null)
const showContent = ref(false)
const isClosing = ref(false)

// Динамические refs для карточек
const cardRefs = ref({})
const setCardRef = (slug) => (el) => {
  if (el) {
    cardRefs.value[slug] = el
  }
}

// Преобразуем данные с сервера в формат для модального окна
const modalMeta = computed(() => {
  if (!selectedType.value || !lodgeTypes.value) return null

  const type = lodgeTypes.value.find(t => t.slug === selectedType.value || t.id === selectedType.value)
  if (!type) return null

  return {
    title: type.name,
    subtitle: type.subtitle || type.description || '',
    heroImage: type.hero_image_webp_url || type.hero_image_url || type.hero_image_variants?.main,
    heroImageVariants: type.hero_image_variants,
  }
})

// Преобразуем lodges в формат для модального окна
const modalItems = computed(() => {
  if (!selectedType.value || !lodgeTypes.value) return []

  const type = lodgeTypes.value.find(t => t.slug === selectedType.value || t.id === selectedType.value)
  if (!type || !type.lodges) return []

  // Определяем тип домов на основе slug типа
  let houseType = 'wooden' // по умолчанию
  if (type.slug === 'modulnye-doma' || type.name.toLowerCase().includes('модульн')) {
    houseType = 'modular'
  }

  return type.lodges.map(lodge => ({
    id: lodge.id,
    name: lodge.name,
    slug: lodge.slug,
    description: lodge.short_description || '',
    capacityNum: lodge.capacity,
    area: parseFloat(lodge.area) || 0,
    priceFrom: parseFloat(lodge.price_from) || 0,
    houseType: houseType, // добавляем информацию о типе
    images: lodge.images?.map(img =>
      img.image_webp_url || img.image_url || img.image_variants?.card
    ) || [],
    imageVariants: lodge.images?.map(img => img.image_variants) || [],
  }))
})

const isOpen = computed(() => !!selectedType.value)

const setCardVars = (slug) => {
  if (!process.client) return
  const cardEl = cardRefs.value[slug]
  if (!cardEl) return
  const rect = cardEl.getBoundingClientRect()
  if (!rect) return
  document.documentElement.style.setProperty('--card-top', `${rect.top}px`)
  document.documentElement.style.setProperty('--card-left', `${rect.left}px`)
  document.documentElement.style.setProperty('--card-width', `${rect.width}px`)
  document.documentElement.style.setProperty('--card-height', `${rect.height}px`)
}

const handleTypeClick = (slug) => {
  if (selectedType.value) return
  setCardVars(slug)
  selectedType.value = slug
}

const handleClose = () => {
  showContent.value = false
  isClosing.value = true
  setTimeout(() => {
    selectedType.value = null
    isClosing.value = false
  }, 800)
}

watch(selectedType, (value) => {
  if (!process.client) return
  if (value) {
    document.body.style.overflow = 'hidden'
    setTimeout(() => (showContent.value = true), 500)
  } else {
    document.body.style.overflow = ''
    showContent.value = false
  }
})

onBeforeUnmount(() => {
  if (process.client) {
    document.body.style.overflow = ''
  }
})
</script>

<template>
  <section id="lodge" class="bg-background py-20">
    <div class="container mx-auto px-6 md:px-8">
      <div class="animate-fade-in mb-12 text-center">
        <h2 class="mb-4 text-4xl font-serif text-primary md:text-5xl">Проживание</h2>
        <p class="mx-auto max-w-2xl text-lg text-muted-foreground">Выберите подходящий для вас вариант размещения</p>
      </div>

      <div v-if="lodgeTypes && lodgeTypes.length > 0" class="relative mb-8 grid gap-4 md:grid-cols-2">
        <div
          v-for="type in lodgeTypes"
          :key="type.id"
          :ref="setCardRef(type.slug)"
          class="group relative cursor-pointer overflow-hidden rounded-2xl border border-border/60 bg-white/80"
          :class="[
            selectedType === type.slug ? '!invisible !transition-none' : '',
            selectedType && selectedType !== type.slug ? 'pointer-events-none opacity-30 transition-opacity duration-300' : 'hover:scale-[1.02] hover:shadow-2xl transition-all duration-300',
          ]"
          @click="handleTypeClick(type.slug)"
        >
          <div class="relative h-[400px]">
            <NuxtImg
              :src="type.hero_image_webp_url || type.hero_image_url || type.hero_image_variants?.card"
              :alt="type.name"
              :width="626"
              :height="456"
              :quality="75"
              loading="lazy"
              sizes="626px"
              class="h-full w-full object-cover transition-transform duration-700 group-hover:scale-105"
            />
            <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/40 to-transparent" />
            <div class="absolute inset-0 flex flex-col justify-end p-8">
              <h3 class="mb-3 text-3xl font-serif text-white md:text-4xl">{{ type.name }}</h3>
              <p class="mb-4 text-lg text-white/90">{{ type.subtitle || type.description }}</p>
              <div class="text-sm text-white/80">Нажмите, чтобы узнать больше</div>
            </div>
          </div>
        </div>
      </div>
      <div v-else class="relative mb-8 grid gap-4 md:grid-cols-2">
        <div class="h-[400px] animate-pulse rounded-2xl bg-gray-200" />
        <div class="h-[400px] animate-pulse rounded-2xl bg-gray-200" />
      </div>

      <ClientOnly>
        <LodgeModal
          :open="isOpen"
          :is-closing="isClosing"
          :show-content="showContent"
          :meta="modalMeta || {}"
          :items="modalItems"
          @close="handleClose"
        />
        <template #fallback>
          <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-black/70">
            <div class="text-white">Загрузка...</div>
          </div>
        </template>
      </ClientOnly>
    </div>
  </section>
</template>

