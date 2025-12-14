<script setup>
import { computed, defineAsyncComponent, onBeforeUnmount, ref, watch } from 'vue'
import cottageImage from '~/assets/resort/cottage-exterior.jpg'
import cottageInterior from '~/assets/resort/cottage-interior.jpg'
import modularImage from '~/assets/resort/modular-house.jpg'
import banyaImage from '~/assets/resort/banya-exterior.jpg'

// Lazy loading для тяжелого модального компонента
const LodgeModal = defineAsyncComponent(() =>
  import('~/components/lodge/LodgeModal.vue')
)

const selectedType = ref(null)
const showContent = ref(false)
const isClosing = ref(false)

const cardRefs = {
  cottages: ref(null),
  modular: ref(null),
}
const setCardRef = (type) => (el) => {
  cardRefs[type].value = el
}

const typeMeta = {
  cottages: {
    title: 'Коттеджи',
    subtitle: 'Традиционные деревянные дома с террасами и мангальными зонами',
    heroImage: cottageImage,
    items: [
      {
        name: 'Дом Кузнеца',
        description: '2 смежные и 2 изолированные спальни, просторная кухня-гостиная, санузел',
        capacityNum: 11,
        area: 120,
        priceFrom: 10000,
        images: [cottageImage, cottageInterior, banyaImage],
      },
      {
        name: 'Дом Лесника',
        description: '3 изолированные спальни, большая терраса с видом на лес, камин',
        capacityNum: 8,
        area: 95,
        priceFrom: 8500,
        images: [cottageImage, cottageInterior, banyaImage],
      },
      {
        name: 'Дом Охотника',
        description: '2 спальни, уютная гостиная с камином, мангальная зона',
        capacityNum: 6,
        area: 75,
        priceFrom: 6500,
        images: [cottageImage, cottageInterior, banyaImage],
      },
    ],
  },
  modular: {
    title: 'Модульные дома',
    subtitle: 'Современные дома с панорамными окнами и стильным интерьером',
    heroImage: modularImage,
    items: [
      {
        name: 'Модуль Панорама',
        description: 'Панорамные окна с видом на реку, современный минималистичный интерьер',
        capacityNum: 2,
        area: 25,
        priceFrom: 4500,
        images: [modularImage, cottageInterior, banyaImage],
      },
      {
        name: 'Модуль Комфорт',
        description: 'Увеличенная площадь, дополнительная спальная зона, терраса',
        capacityNum: 4,
        area: 35,
        priceFrom: 5500,
        images: [modularImage, cottageInterior, banyaImage],
      },
      {
        name: 'Модуль Премиум',
        description: 'Максимальный комфорт, джакузи, камин, панорамный вид на лес',
        capacityNum: 4,
        area: 40,
        priceFrom: 7500,
        images: [modularImage, cottageInterior, banyaImage],
      },
    ],
  },
}

const modalMeta = computed(() => (selectedType.value ? typeMeta[selectedType.value] : null))
const modalItems = computed(() => modalMeta.value?.items || [])
const isOpen = computed(() => !!selectedType.value)

const setCardVars = (type) => {
  if (!process.client) return
  const rect = cardRefs[type].value?.getBoundingClientRect()
  if (!rect) return
  document.documentElement.style.setProperty('--card-top', `${rect.top}px`)
  document.documentElement.style.setProperty('--card-left', `${rect.left}px`)
  document.documentElement.style.setProperty('--card-width', `${rect.width}px`)
  document.documentElement.style.setProperty('--card-height', `${rect.height}px`)
}

const handleTypeClick = (type) => {
  if (selectedType.value) return
  setCardVars(type)
  selectedType.value = type
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

      <div class="relative mb-8 grid gap-4 md:grid-cols-2">
        <div
          :ref="setCardRef('cottages')"
          class="group relative cursor-pointer overflow-hidden rounded-2xl border border-border/60 bg-white/80"
          :class="[
            selectedType === 'cottages' ? '!invisible !transition-none' : '',
            selectedType && selectedType !== 'cottages' ? 'pointer-events-none opacity-30 transition-opacity duration-300' : 'hover:scale-[1.02] hover:shadow-2xl transition-all duration-300',
          ]"
          @click="handleTypeClick('cottages')"
        >
          <div class="relative h-[400px]">
            <img :src="cottageImage" alt="Коттеджи" class="h-full w-full object-cover transition-transform duration-700 group-hover:scale-105" />
            <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/40 to-transparent" />
            <div class="absolute inset-0 flex flex-col justify-end p-8">
              <h3 class="mb-3 text-3xl font-serif text-white md:text-4xl">Коттеджи</h3>
              <p class="mb-4 text-lg text-white/90">Традиционные деревянные дома с террасами и мангальными зонами</p>
              <div class="text-sm text-white/80">Нажмите, чтобы узнать больше</div>
            </div>
          </div>
        </div>

        <div
          :ref="setCardRef('modular')"
          class="group relative cursor-pointer overflow-hidden rounded-2xl border border-border/60 bg-white/80"
          :class="[
            selectedType === 'modular' ? '!invisible !transition-none' : '',
            selectedType && selectedType !== 'modular' ? 'pointer-events-none opacity-30 transition-opacity duration-300' : 'hover:scale-[1.02] hover:shadow-2xl transition-all duration-300',
          ]"
          @click="handleTypeClick('modular')"
        >
          <div class="relative h-[400px]">
            <img :src="modularImage" alt="Модульные дома" class="h-full w-full object-cover transition-transform duration-700 group-hover:scale-105" />
            <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/40 to-transparent" />
            <div class="absolute inset-0 flex flex-col justify-end p-8">
              <h3 class="mb-3 text-3xl font-serif text-white md:text-4xl">Модульные дома</h3>
              <p class="mb-4 text-lg text-white/90">Современные дома с панорамными окнами и стильным интерьером</p>
              <div class="text-sm text-white/80">Нажмите, чтобы узнать больше</div>
            </div>
          </div>
        </div>
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

