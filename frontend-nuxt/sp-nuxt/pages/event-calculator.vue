<script setup lang="js">
import { ref, computed, onMounted, onBeforeUnmount, watch } from 'vue'
import { useHead } from '#imports'
import { NuxtLink } from '#components'
import FooterSection from '~/components/sections/FooterSection.vue'
import {
  ArrowLeft,
  Calendar as CalendarIcon,
  Home,
  MapPin,
  Music,
  Phone,
  Send,
  Sparkles,
  Users,
  Utensils,
  X,
  RotateCcw,
  ChevronLeft,
  ChevronRight,
} from 'lucide-vue-next'

import logo from '~/assets/resort/logo.png'
import cottageImage from '~/assets/resort/cottage-exterior.jpg'
import cottageInterior from '~/assets/resort/cottage-interior.jpg'
import modularImage from '~/assets/resort/modular-house.jpg'
import banyaImage from '~/assets/resort/banya-exterior.jpg'
import event1Image from '~/assets/resort/event1.webp'
import event2Image from '~/assets/resort/event2.webp'
import event3Image from '~/assets/resort/event3.webp'
import event5Image from '~/assets/resort/event5.webp'

const eventTypes = [
  {
    id: 'wedding',
    title: 'Свадьба',
    description:
      'Романтическая церемония и банкет в живописном месте на берегу Камского моря',
    image: event1Image,
  },
  {
    id: 'anniversary',
    title: 'Юбилей',
    description:
      'Уютный банкетный зал, украшение под ваш сценарий и программы с ведущими',
    image: event2Image,
  },
  {
    id: 'corporate',
    title: 'Корпоратив',
    description:
      'Тимбилдинг на природе, конференц-зона, банкет и активный отдых круглый год',
    image: event3Image,
  },
  {
    id: 'graduation',
    title: 'Выпускной',
    description:
      'Безопасная закрытая территория и программы для школьников и студентов',
    image: event5Image,
  },
]

const cottages = [
  {
    id: 'cottage-1',
    name: 'Дом Кузнеца',
    description: '2 смежные и 2 изолированные спальни, просторная кухня-гостиная',
    capacityNum: 11,
    area: 120,
    pricePerNight: 10000,
    images: [cottageImage, cottageInterior, banyaImage],
  },
  {
    id: 'cottage-2',
    name: 'Дом Лесника',
    description: '3 изолированные спальни, большая терраса с видом на лес',
    capacityNum: 8,
    area: 95,
    pricePerNight: 8500,
    images: [cottageImage, cottageInterior, banyaImage],
  },
  {
    id: 'cottage-3',
    name: 'Дом Охотника',
    description: '2 спальни, уютная гостиная с камином, мангальная зона',
    capacityNum: 6,
    area: 75,
    pricePerNight: 6500,
    images: [cottageImage, cottageInterior, banyaImage],
  },
]

const modularHouses = [
  {
    id: 'modular-1',
    name: 'Модуль Панорама',
    description: 'Панорамные окна с видом на реку, современный интерьер',
    capacityNum: 2,
    area: 25,
    pricePerNight: 4500,
    images: [modularImage, cottageInterior, banyaImage],
  },
  {
    id: 'modular-2',
    name: 'Модуль Комфорт',
    description: 'Увеличенная площадь, дополнительная спальная зона',
    capacityNum: 4,
    area: 35,
    pricePerNight: 5500,
    images: [modularImage, cottageInterior, banyaImage],
  },
  {
    id: 'modular-3',
    name: 'Модуль Премиум',
    description: 'Максимальный комфорт, джакузи, камин',
    capacityNum: 4,
    area: 40,
    pricePerNight: 7500,
    images: [modularImage, cottageInterior, banyaImage],
  },
]

const pricing = {
  venueBase: 25000,
  guestPrice: 3500,
  cateringOptions: {
    basic: { name: 'Базовое меню', price: 2500 },
    premium: { name: 'Премиум меню', price: 4500 },
    luxury: { name: 'Люкс меню', price: 7000 },
  },
  entertainment: {
    dj: { name: 'DJ и звук', price: 15000 },
    band: { name: 'Живая музыка', price: 35000 },
    host: { name: 'Ведущий', price: 20000 },
    photo: { name: 'Фотограф', price: 25000 },
    video: { name: 'Видеограф', price: 30000 },
  },
  additional: {
    decoration: { name: 'Декор и оформление', price: 15000 },
    flowers: { name: 'Цветочные композиции', price: 12000 },
    fireworks: { name: 'Салют и пиротехника', price: 25000 },
    transfer: { name: 'Трансфер гостей', price: 8000 },
  },
}

const selectedEvent = ref(null)
const flippedCard = ref(null)
const isMobile = ref(false)
const isVisible = ref(false)

const guestCount = ref(50)
const eventDate = ref('')
const catering = ref('premium')
const entertainment = ref([])
const additional = ref([])
const contactName = ref('')
const contactPhone = ref('')
const contactEmail = ref('')

const checkInDate = ref('')
const checkOutDate = ref('')
const selectedHouses = ref([])
const accommodationType = ref('cottages') // 'cottages' или 'modular'
const photoModalOpen = ref(false)
const activeHousePhotos = ref(null)
const currentPhotoIndex = ref(0)

const nightsCount = computed(() => {
  if (!checkInDate.value || !checkOutDate.value) return 0
  const start = new Date(checkInDate.value).getTime()
  const end = new Date(checkOutDate.value).getTime()
  const diff = Math.max(0, end - start)
  return Math.floor(diff / 86_400_000)
})

const allHouses = [...cottages, ...modularHouses]

const displayedHouses = computed(() => {
  return accommodationType.value === 'cottages' ? cottages : modularHouses
})

const selectedCottagesCount = computed(() => {
  return selectedHouses.value.filter(id => cottages.some(c => c.id === id)).length
})

const selectedModularCount = computed(() => {
  return selectedHouses.value.filter(id => modularHouses.some(m => m.id === id)).length
})

const accommodationTotal = computed(() =>
  selectedHouses.value.reduce((sum, houseId) => {
    const house = allHouses.find((h) => h.id === houseId)
    return sum + (house ? house.pricePerNight * nightsCount.value : 0)
  }, 0),
)

const total = computed(() => {
  let totalValue = pricing.venueBase
  totalValue += guestCount.value * pricing.guestPrice

  if (catering.value && pricing.cateringOptions[catering.value]) {
    totalValue += guestCount.value * pricing.cateringOptions[catering.value].price
  }

  entertainment.value.forEach((id) => {
    if (pricing.entertainment[id]) {
      totalValue += pricing.entertainment[id].price
    }
  })

  additional.value.forEach((id) => {
    if (pricing.additional[id]) {
      totalValue += pricing.additional[id].price
    }
  })

  totalValue += accommodationTotal.value
  return totalValue
})

const formatPrice = (price) => new Intl.NumberFormat('ru-RU').format(price)

const handleEventSelect = (id) => {
  selectedEvent.value = id
  flippedCard.value = null
  const section = document.getElementById('calculator')
  if (section) {
    setTimeout(() => section.scrollIntoView({ behavior: 'smooth', block: 'start' }), 200)
  }
}

const toggleEntertainment = (id) => {
  entertainment.value = entertainment.value.includes(id)
    ? entertainment.value.filter((e) => e !== id)
    : [...entertainment.value, id]
}

const toggleAdditional = (id) => {
  additional.value = additional.value.includes(id)
    ? additional.value.filter((e) => e !== id)
    : [...additional.value, id]
}

const toggleHouse = (id) => {
  selectedHouses.value = selectedHouses.value.includes(id)
    ? selectedHouses.value.filter((h) => h !== id)
    : [...selectedHouses.value, id]
}

const openPhotoModal = (house) => {
  activeHousePhotos.value = { images: house.images, name: house.name }
  currentPhotoIndex.value = 0
  photoModalOpen.value = true
}

const closeModal = () => {
  photoModalOpen.value = false
  activeHousePhotos.value = null
}

const nextPhoto = () => {
  if (!activeHousePhotos.value) return
  currentPhotoIndex.value = (currentPhotoIndex.value + 1) % activeHousePhotos.value.images.length
}

const prevPhoto = () => {
  if (!activeHousePhotos.value) return
  const totalPhotos = activeHousePhotos.value.images.length
  currentPhotoIndex.value = (currentPhotoIndex.value - 1 + totalPhotos) % totalPhotos
}

const handleResize = () => {
  isMobile.value = window.innerWidth < 768
}

onMounted(() => {
  handleResize()
  window.addEventListener('resize', handleResize)
  setTimeout(() => (isVisible.value = true), 100)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize)
})

watch(photoModalOpen, (open) => {
  document.body.style.overflow = open ? 'hidden' : ''
})

useHead({
  title: 'Калькулятор мероприятия - Строгановские Просторы',
  meta: [
    {
      name: 'description',
      content: 'Рассчитайте предварительную стоимость мероприятия на базе отдыха Строгановские Просторы',
    },
  ],
  link: [{ rel: 'canonical', href: '/event-calculator' }],
})
</script>

<template>
  <div class="min-h-screen bg-background text-foreground">
    <!-- Навигация -->
    <nav class="fixed left-0 right-0 top-0 z-50 bg-primary/95 shadow backdrop-blur">
      <div class="container mx-auto flex items-center justify-between px-6 py-4">
        <div class="flex items-center gap-6">
          <NuxtLink to="/">
            <img :src="logo" alt="Строгановские Просторы" class="h-10 md:h-12 transition-transform duration-300 hover:scale-105" />
          </NuxtLink>
          <NuxtLink
            to="/"
            class="hidden items-center gap-2 text-primary-foreground/80 transition-colors hover:text-primary-foreground md:flex"
          >
            <ArrowLeft class="h-4 w-4" />
            На главную
          </NuxtLink>
        </div>
        <a
          href="tel:+73422333332"
          class="flex items-center gap-2 text-primary-foreground transition-colors hover:text-primary-foreground/80"
        >
          <Phone class="h-5 w-5" />
          <span class="hidden md:inline">+7 (342) 2-33-33-32</span>
        </a>
      </div>
    </nav>

    <!-- Херо -->
    <section class="bg-gradient-to-b from-primary/10 to-background px-6 pb-20 pt-32">
      <div class="container mx-auto">
        <div
          class="mb-12 text-center transition-all duration-700"
          :class="isVisible ? 'translate-y-0 opacity-100' : 'translate-y-10 opacity-0'"
        >
          <h1 class="mb-4 text-3xl font-light text-foreground md:text-5xl">
            Проведите незабываемое мероприятие на природе
          </h1>
          <p class="mx-auto max-w-2xl text-lg text-muted-foreground md:text-xl">
            Свадьбы, юбилеи, корпоративы и выпускные на базе отдыха с проживанием и питанием
          </p>
        </div>

        <!-- Карточки событий -->
        <div
          class="grid grid-cols-1 gap-6 transition-all duration-700 delay-200 md:grid-cols-2 lg:grid-cols-4"
          :class="isVisible ? 'translate-y-0 opacity-100' : 'translate-y-10 opacity-0'"
        >
          <div
            v-for="event in eventTypes"
            :key="event.id"
            class="group h-80 md:h-96 cursor-pointer perspective-1000"
            @mouseenter="!isMobile && (flippedCard = event.id)"
            @mouseleave="!isMobile && (flippedCard = null)"
            @click="handleEventSelect(event.id)"
          >
            <div
              class="relative h-full w-full transition-transform duration-700 transform-style-3d"
              :class="flippedCard === event.id ? 'rotate-y-180' : ''"
            >
              <!-- Front Side -->
              <div class="absolute inset-0 backface-hidden rounded-2xl overflow-hidden shadow-lg">
                <img :src="event.image" :alt="event.title" class="h-full w-full object-cover" />
                <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/30 to-transparent" />
                <div class="absolute bottom-0 left-0 right-0 p-6 text-center">
                  <h3 class="text-2xl font-light text-white md:text-3xl">{{ event.title }}</h3>
                </div>
                <div v-if="isMobile" class="absolute right-4 top-4">
                  <RotateCcw class="h-5 w-5 text-white/70" />
                </div>
              </div>

              <!-- Back Side -->
              <div class="absolute inset-0 backface-hidden rotate-y-180 rounded-2xl overflow-hidden bg-primary shadow-lg">
                <div class="absolute inset-0 flex flex-col items-center justify-center p-6 text-center">
                  <h3 class="mb-4 text-2xl font-light text-primary-foreground md:text-3xl">{{ event.title }}</h3>
                  <p class="mb-6 text-sm leading-relaxed text-primary-foreground/80 md:text-base">
                    {{ event.description }}
                  </p>
                  <button
                    class="rounded-lg border border-primary-foreground bg-transparent px-4 py-2 text-sm font-medium text-primary-foreground transition-all duration-300 hover:bg-primary-foreground hover:text-primary"
                    @click.stop="handleEventSelect(event.id)"
                  >
                    Рассчитать стоимость
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Калькулятор -->
    <section id="calculator" class="px-6 py-20">
      <div class="container mx-auto max-w-5xl">
        <div
          class="mb-12 text-center transition-all duration-700"
          :class="selectedEvent ? 'translate-y-0 opacity-100' : 'opacity-50'"
        >
          <h2 class="mb-4 text-2xl font-light text-foreground md:text-4xl">Рассчитайте стоимость вашего мероприятия</h2>
          <p class="text-muted-foreground">Выберите опции и получите предварительный расчёт</p>
        </div>

        <div class="space-y-8 rounded-3xl bg-card p-6 shadow-lg md:p-10">
          <!-- 1 Основные параметры -->
          <div class="space-y-6">
            <div class="flex items-center gap-3 text-primary">
              <div class="flex h-10 w-10 items-center justify-center rounded-full bg-primary/10">
                <span class="font-medium">1</span>
              </div>
              <h3 class="text-xl font-light">Основные параметры</h3>
            </div>

            <div class="grid grid-cols-1 gap-6 md:grid-cols-3">
              <div class="space-y-2">
                <label class="flex items-center gap-2 text-sm font-medium">
                  <Sparkles class="h-4 w-4 text-primary" />
                  Тип мероприятия
                </label>
                <select
                  v-model="selectedEvent"
                  class="w-full rounded-lg border border-border bg-background px-3 py-2 text-sm focus:border-primary focus:outline-none"
                >
                  <option disabled value="">Выберите тип</option>
                  <option v-for="event in eventTypes" :key="event.id" :value="event.id">{{ event.title }}</option>
                </select>
              </div>

              <div class="space-y-2">
                <label class="flex items-center gap-2 text-sm font-medium">
                  <Users class="h-4 w-4 text-primary" />
                  Количество гостей
                </label>
                <input
                  v-model.number="guestCount"
                  type="number"
                  min="10"
                  max="200"
                  class="w-full rounded-lg border border-border bg-background px-3 py-2 text-sm focus:border-primary focus:outline-none"
                />
              </div>

              <div class="space-y-2">
                <label class="flex items-center gap-2 text-sm font-medium">
                  <CalendarIcon class="h-4 w-4 text-primary" />
                  Дата мероприятия
                </label>
                <input
                  v-model="eventDate"
                  type="date"
                  class="w-full rounded-lg border border-border bg-background px-3 py-2 text-sm focus:border-primary focus:outline-none"
                />
              </div>
            </div>
          </div>

          <!-- 2 Локация -->
          <div class="space-y-6 border-t border-border pt-6">
            <div class="flex items-center gap-3 text-primary">
              <div class="flex h-10 w-10 items-center justify-center rounded-full bg-primary/10">
                <span class="font-medium">2</span>
              </div>
              <h3 class="text-xl font-light">Локация</h3>
            </div>

            <div class="rounded-xl bg-muted/50 p-6">
              <div class="flex items-start gap-4">
                <MapPin class="mt-1 h-6 w-6 text-primary" />
                <div>
                  <h4 class="mb-2 font-medium text-foreground">База отдыха «Строгановские Просторы»</h4>
                  <p class="mb-2 text-sm text-muted-foreground">
                    Живописная территория на берегу Камского моря, банкетный зал до 100 человек, открытая площадка для
                    церемоний, комфортное размещение гостей.
                  </p>
                  <p class="font-medium text-primary">Аренда площадки: {{ formatPrice(pricing.venueBase) }} ₽</p>
                </div>
              </div>
            </div>
          </div>

          <!-- 3 Размещение -->
          <div class="space-y-6 border-t border-border pt-6">
            <div class="flex items-center gap-3 text-primary">
              <div class="flex h-10 w-10 items-center justify-center rounded-full bg-primary/10">
                <span class="font-medium">3</span>
              </div>
              <h3 class="text-xl font-light">Размещение гостей</h3>
            </div>

            <div class="grid grid-cols-1 gap-4 md:grid-cols-2">
              <div class="space-y-2">
                <label class="flex items-center gap-2 text-sm font-medium">
                  <CalendarIcon class="h-4 w-4 text-primary" />
                  Дата заезда
                </label>
                <input
                  v-model="checkInDate"
                  type="date"
                  class="w-full rounded-lg border border-border bg-background px-3 py-2 text-sm focus:border-primary focus:outline-none"
                />
              </div>
              <div class="space-y-2">
                <label class="flex items-center gap-2 text-sm font-medium">
                  <CalendarIcon class="h-4 w-4 text-primary" />
                  Дата выезда
                </label>
                <input
                  v-model="checkOutDate"
                  type="date"
                  class="w-full rounded-lg border border-border bg-background px-3 py-2 text-sm focus:border-primary focus:outline-none"
                />
              </div>
            </div>

            <div v-if="nightsCount > 0" class="rounded-lg bg-primary/10 px-4 py-2 text-center">
              <span class="font-medium text-primary">Количество ночей: {{ nightsCount }}</span>
            </div>

            <div>
              <div
                class="grid w-full grid-cols-2 divide-x divide-border overflow-hidden rounded-xl border border-border text-sm font-medium"
              >
                <button
                  class="relative flex items-center justify-center gap-2 px-3 py-3 transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary/40 focus-visible:ring-offset-0"
                  :class="accommodationType === 'cottages' ? 'bg-primary text-primary-foreground' : 'bg-background text-foreground hover:bg-muted/40'"
                  @click="accommodationType = 'cottages'"
                >
                  <Home class="h-4 w-4" />
                  <span>Коттеджи</span>
                  <span
                    v-if="selectedCottagesCount > 0"
                    class="absolute right-2 top-2 flex h-5 min-w-[1.25rem] items-center justify-center rounded-full bg-primary-foreground px-1 text-xs font-bold text-primary"
                  >
                    {{ selectedCottagesCount }}
                  </span>
                </button>
                <button
                  class="relative flex items-center justify-center gap-2 px-3 py-3 transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary/40 focus-visible:ring-offset-0"
                  :class="accommodationType === 'modular' ? 'bg-primary text-primary-foreground' : 'bg-background text-foreground hover:bg-muted/40'"
                  @click="accommodationType = 'modular'"
                >
                  <Home class="h-4 w-4" />
                  <span>Модульные</span>
                  <span
                    v-if="selectedModularCount > 0"
                    class="absolute right-2 top-2 flex h-5 min-w-[1.25rem] items-center justify-center rounded-full bg-primary-foreground px-1 text-xs font-bold text-primary"
                  >
                    {{ selectedModularCount }}
                  </span>
                </button>
              </div>

              <div class="mt-4 space-y-3">
                <div
                  v-for="house in displayedHouses"
                  :key="house.id"
                  class="flex cursor-pointer gap-4 rounded-xl border-2 p-3 transition-all duration-300"
                  :class="selectedHouses.includes(house.id) ? 'border-primary bg-primary/5' : 'border-border hover:border-primary/50'"
                  @click="toggleHouse(house.id)"
                >
                  <div
                    class="relative h-24 w-24 shrink-0 cursor-zoom-in overflow-hidden rounded-lg"
                    @click.stop="openPhotoModal(house)"
                  >
                    <img :src="house.images[0]" :alt="house.name" class="h-full w-full object-cover transition-transform duration-300 hover:scale-110" />
                    <div v-if="house.images.length > 1" class="absolute bottom-1 right-1 rounded bg-background/80 px-1.5 py-0.5 text-xs">
                      +{{ house.images.length - 1 }}
                    </div>
                  </div>

                  <div class="min-w-0 flex-1">
                    <div class="flex items-start justify-between gap-2">
                      <h4 class="truncate font-medium text-foreground">{{ house.name }}</h4>
                      <input type="checkbox" class="h-4 w-4" :checked="selectedHouses.includes(house.id)" @click.stop="toggleHouse(house.id)" />
                    </div>
                    <div class="mt-1 flex items-center gap-1.5 text-primary font-medium">
                      <Users class="h-4 w-4" />
                      <span>до {{ house.capacityNum }} чел</span>
                    </div>
                    <p class="mt-1 line-clamp-2 text-xs text-muted-foreground">{{ house.description }}</p>
                    <div class="mt-2 flex items-center justify-between">
                      <span class="text-sm font-medium text-foreground">{{ house.pricePerNight.toLocaleString() }} ₽/сутки</span>
                      <span class="text-xs text-muted-foreground">{{ house.area }} м²</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div v-if="selectedHouses.length > 0 && nightsCount > 0" class="space-y-2 rounded-xl bg-primary/5 p-4">
              <div class="flex items-center justify-between">
                <span class="text-sm text-muted-foreground">Выбрано домов:</span>
                <span class="font-medium text-foreground">{{ selectedHouses.length }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-sm text-muted-foreground">Стоимость размещения:</span>
                <span class="font-medium text-primary">{{ formatPrice(accommodationTotal) }} ₽</span>
              </div>
            </div>
          </div>

          <!-- 4 Кейтеринг -->
          <div class="space-y-6 border-t border-border pt-6">
            <div class="flex items-center gap-3 text-primary">
              <div class="flex h-10 w-10 items-center justify-center rounded-full bg-primary/10">
                <span class="font-medium">4</span>
              </div>
              <h3 class="text-xl font-light">Кейтеринг и развлечения</h3>
            </div>

            <div class="space-y-4">
              <label class="flex items-center gap-2 text-sm font-medium">
                <Utensils class="h-4 w-4 text-primary" />
                Меню
              </label>
              <div class="grid grid-cols-1 gap-4 md:grid-cols-3">
                <div
                  v-for="(option, key) in pricing.cateringOptions"
                  :key="key"
                  class="cursor-pointer rounded-xl border-2 p-4 transition-all duration-300"
                  :class="catering === key ? 'border-primary bg-primary/5' : 'border-border hover:border-primary/50'"
                  @click="catering = key"
                >
                  <h4 class="font-medium text-foreground">{{ option.name }}</h4>
                  <p class="text-sm text-primary">{{ formatPrice(option.price) }} ₽/чел</p>
                </div>
              </div>
            </div>

            <div class="space-y-4">
              <label class="flex items-center gap-2 text-sm font-medium">
                <Music class="h-4 w-4 text-primary" />
                Развлечения и персонал
              </label>
              <div class="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
                <div
                  v-for="(option, key) in pricing.entertainment"
                  :key="key"
                  class="flex items-center space-x-3 rounded-xl border border-border p-4 transition-all hover:border-primary/50"
                >
                  <input type="checkbox" :id="key" :checked="entertainment.includes(key)" @change="toggleEntertainment(key)" />
                  <label :for="key" class="flex-1 cursor-pointer">
                    <span class="block text-foreground">{{ option.name }}</span>
                    <span class="text-sm text-primary">{{ formatPrice(option.price) }} ₽</span>
                  </label>
                </div>
              </div>
            </div>
          </div>

          <!-- 5 Дополнительные -->
          <div class="space-y-6 border-t border-border pt-6">
            <div class="flex items-center gap-3 text-primary">
              <div class="flex h-10 w-10 items-center justify-center rounded-full bg-primary/10">
                <span class="font-medium">5</span>
              </div>
              <h3 class="text-xl font-light">Дополнительные услуги</h3>
            </div>

            <div class="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
              <div
                v-for="(option, key) in pricing.additional"
                :key="key"
                class="flex items-center space-x-3 rounded-xl border border-border p-4 transition-all hover:border-primary/50"
              >
                <input
                  :id="`add-${key}`"
                  type="checkbox"
                  :checked="additional.includes(key)"
                  @change="toggleAdditional(key)"
                />
                <label :for="`add-${key}`" class="flex-1 cursor-pointer">
                  <span class="block text-foreground">{{ option.name }}</span>
                  <span class="text-sm text-primary">{{ formatPrice(option.price) }} ₽</span>
                </label>
              </div>
            </div>
          </div>

          <!-- 6 Итог -->
          <div class="space-y-6 border-t border-border pt-6">
            <div class="flex items-center gap-3 text-primary">
              <div class="flex h-10 w-10 items-center justify-center rounded-full bg-primary/10">
                <span class="font-medium">6</span>
              </div>
              <h3 class="text-xl font-light">Итог и заявка</h3>
            </div>

            <div class="rounded-2xl bg-primary p-6 text-center md:p-8">
              <p class="mb-2 text-primary-foreground/80">Предварительная стоимость</p>
              <p class="mb-4 text-4xl font-light text-primary-foreground md:text-5xl">{{ formatPrice(total) }} ₽</p>
              <p class="text-sm text-primary-foreground/60">
                Окончательная стоимость будет рассчитана менеджером с учётом всех деталей
              </p>
            </div>

            <div class="space-y-4">
              <p class="text-center text-muted-foreground">
                Оставьте контакты, и мы свяжемся с вами для уточнения деталей
              </p>
              <div class="grid grid-cols-1 gap-4 md:grid-cols-3">
                <div class="space-y-2">
                  <label for="name" class="text-sm font-medium">Ваше имя</label>
                  <input
                    id="name"
                    v-model="contactName"
                    type="text"
                    placeholder="Иван Иванов"
                    class="w-full rounded-lg border border-border bg-background px-3 py-2 text-sm focus:border-primary focus:outline-none"
                  />
                </div>
                <div class="space-y-2">
                  <label for="phone" class="text-sm font-medium">Телефон</label>
                  <input
                    id="phone"
                    v-model="contactPhone"
                    type="tel"
                    placeholder="+7 (999) 123-45-67"
                    class="w-full rounded-lg border border-border bg-background px-3 py-2 text-sm focus:border-primary focus:outline-none"
                  />
                </div>
                <div class="space-y-2">
                  <label for="email" class="text-sm font-medium">Email</label>
                  <input
                    id="email"
                    v-model="contactEmail"
                    type="email"
                    placeholder="email@example.com"
                    class="w-full rounded-lg border border-border bg-background px-3 py-2 text-sm focus:border-primary focus:outline-none"
                  />
                </div>
              </div>

              <button
                class="mx-auto flex w-full items-center justify-center gap-2 rounded-lg bg-primary px-8 py-3 text-center text-base font-medium text-primary-foreground transition hover:bg-primary/90 md:w-auto"
              >
                <Send class="h-4 w-4" />
                Отправить заявку
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Модалка фото -->
    <transition name="fade">
      <div
        v-if="photoModalOpen && activeHousePhotos"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black/70 px-4"
        role="dialog"
        aria-modal="true"
      >
        <div class="relative w-full max-w-4xl overflow-hidden rounded-2xl bg-background shadow-2xl">
          <button
            class="absolute right-4 top-4 z-10 rounded-full bg-background/80 p-2 text-foreground shadow hover:bg-background"
            @click="closeModal"
            aria-label="Закрыть"
          >
            <X class="h-5 w-5" />
          </button>

          <div class="relative">
            <img
              :src="activeHousePhotos.images[currentPhotoIndex]"
              :alt="`${activeHousePhotos.name} - фото ${currentPhotoIndex + 1}`"
              class="h-[60vh] w-full object-cover"
            />

            <button
              v-if="activeHousePhotos.images.length > 1"
              class="absolute left-4 top-1/2 flex h-10 w-10 -translate-y-1/2 items-center justify-center rounded-full bg-background/80 hover:bg-background"
              @click="prevPhoto"
              aria-label="Предыдущее фото"
            >
              <ChevronLeft class="h-5 w-5" />
            </button>
            <button
              v-if="activeHousePhotos.images.length > 1"
              class="absolute right-4 top-1/2 flex h-10 w-10 -translate-y-1/2 items-center justify-center rounded-full bg-background/80 hover:bg-background"
              @click="nextPhoto"
              aria-label="Следующее фото"
            >
              <ChevronRight class="h-5 w-5" />
            </button>

            <div class="absolute bottom-4 left-1/2 flex -translate-x-1/2 gap-2">
              <button
                v-for="(_, index) in activeHousePhotos.images"
                :key="index"
                class="h-2 rounded-full transition-all"
                :class="index === currentPhotoIndex ? 'w-6 bg-primary' : 'w-2 bg-primary/40'"
                @click="currentPhotoIndex = index"
              />
            </div>
          </div>

          <div class="p-4 text-center">
            <h3 class="font-medium text-foreground">{{ activeHousePhotos.name }}</h3>
            <p class="text-sm text-muted-foreground">
              Фото {{ currentPhotoIndex + 1 }} из {{ activeHousePhotos.images.length }}
            </p>
          </div>
        </div>
      </div>
    </transition>

    <!-- Футер -->
    <FooterSection />
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>

