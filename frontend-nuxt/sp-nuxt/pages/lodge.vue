<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import WoodenHousesSection from '~/components/lodge/WoodenHousesSection.vue'
import ModularHousesSection from '~/components/lodge/ModularHousesSection.vue'

// Импортируем изображения
import cottageExterior from '~/assets/resort/cottage-exterior.webp'
import cottageInterior from '~/assets/resort/cottage-interior.webp'
import banyaExterior from '~/assets/resort/banya-exterior.webp'
import modularHouse from '~/assets/resort/modular-house.webp'
import galleryForestWalk from '~/assets/resort/gallery-forest-walk.webp'
import galleryWindowView from '~/assets/resort/gallery-window-view.webp'
import peacefulForestWalk from '~/assets/resort/peaceful-forest-walk.webp'
import galleryPierWinter from '~/assets/resort/gallery-pier-winter.webp'

// Моковые данные для houseList
const mockHouseList = [
  {
    id: 1,
    name: 'Дом Кузнеца',
    slug: 'dom-kuznetsa',
    img: cottageExterior,
    description: '2 смежные и 2 изолированные спальни, просторная кухня-гостиная, санузел. Уютный дом для большой компании.',
    conveniences: 'Wi-Fi, отопление, кухня, санузел, терраса',
    include: 'Постельное белье, полотенца, посуда, бытовая химия',
    travelLineId: '1',
    photo_gallery_set: [
      {
        img: cottageExterior,
        name: 'Внешний вид',
      },
      {
        img: cottageInterior,
        name: 'Интерьер',
      },
      {
        img: banyaExterior,
        name: 'Баня',
      },
      {
        img: galleryForestWalk,
        name: 'Окрестности',
      },
    ],
    price_set: [
      { name: 'Будни (1-2 чел.)', cost: 5000 },
      { name: 'Будни (3-4 чел.)', cost: 8000 },
      { name: 'Выходные (1-2 чел.)', cost: 7000 },
      { name: 'Выходные (3-4 чел.)', cost: 10000 },
    ],
    special_price_set: [
      { name: 'Новогодние праздники', cost: 15000 },
    ],
    availability_set: [
      { name: 'Доступен для бронирования' },
      { name: 'Минимум 2 ночи' },
    ],
  },
  {
    id: 2,
    name: 'Дом Лесника',
    slug: 'dom-lesnika',
    img: modularHouse,
    description: '3 изолированные спальни, большая терраса с видом на лес, камин. Идеально для семейного отдыха.',
    conveniences: 'Wi-Fi, отопление, кухня, санузел, терраса, камин',
    include: 'Постельное белье, полотенца, посуда, дрова для камина',
    travelLineId: '2',
    photo_gallery_set: [
      {
        img: modularHouse,
        name: 'Внешний вид',
      },
      {
        img: cottageInterior,
        name: 'Гостиная',
      },
      {
        img: galleryWindowView,
        name: 'Вид из окна',
      },
      {
        img: peacefulForestWalk,
        name: 'Терраса',
      },
    ],
    price_set: [
      { name: 'Будни (1-2 чел.)', cost: 4500 },
      { name: 'Будни (3-4 чел.)', cost: 7500 },
      { name: 'Выходные (1-2 чел.)', cost: 6500 },
      { name: 'Выходные (3-4 чел.)', cost: 9500 },
    ],
    special_price_set: [
      { name: 'Новогодние праздники', cost: 14000 },
    ],
    availability_set: [
      { name: 'Доступен для бронирования' },
      { name: 'Минимум 2 ночи' },
    ],
  },
  {
    id: 3,
    name: 'Дом Охотника',
    slug: 'dom-ohotnika',
    img: banyaExterior,
    description: '2 спальни, уютная гостиная с камином, мангальная зона. Компактный и уютный дом для небольшой компании.',
    conveniences: 'Wi-Fi, отопление, кухня, санузел, мангальная зона',
    include: 'Постельное белье, полотенца, посуда, уголь для мангала',
    travelLineId: '3',
    photo_gallery_set: [
      {
        img: banyaExterior,
        name: 'Внешний вид',
      },
      {
        img: cottageInterior,
        name: 'Интерьер',
      },
      {
        img: galleryPierWinter,
        name: 'Мангальная зона',
      },
    ],
    price_set: [
      { name: 'Будни (1-2 чел.)', cost: 3500 },
      { name: 'Будни (3-4 чел.)', cost: 6000 },
      { name: 'Выходные (1-2 чел.)', cost: 5500 },
      { name: 'Выходные (3-4 чел.)', cost: 8500 },
    ],
    special_price_set: [
      { name: 'Новогодние праздники', cost: 12000 },
    ],
    availability_set: [
      { name: 'Доступен для бронирования' },
      { name: 'Минимум 1 ночь' },
    ],
  },
]

// Моковые данные для модульных домов
const mockModularHouseList = [
  {
    id: 4,
    name: 'Премиум',
    slug: 'modular-premium',
    img: modularHouse,
    description: 'Современный модульный дом с панорамными окнами, просторная гостиная, 2 спальни, полностью оборудованная кухня.',
    conveniences: 'Wi-Fi, отопление, кондиционер, кухня, санузел, терраса, панорамные окна',
    include: 'Постельное белье, полотенца, посуда, бытовая техника',
    travelLineId: '4',
    photo_gallery_set: [
      {
        img: modularHouse,
        name: 'Внешний вид',
      },
      {
        img: cottageInterior,
        name: 'Гостиная',
      },
      {
        img: galleryWindowView,
        name: 'Панорамные окна',
      },
      {
        img: peacefulForestWalk,
        name: 'Терраса',
      },
    ],
    price_set: [
      { name: 'Будни (1-2 чел.)', cost: 6000 },
      { name: 'Будни (3-4 чел.)', cost: 9000 },
      { name: 'Выходные (1-2 чел.)', cost: 8000 },
      { name: 'Выходные (3-4 чел.)', cost: 12000 },
    ],
    special_price_set: [
      { name: 'Новогодние праздники', cost: 18000 },
    ],
    availability_set: [
      { name: 'Доступен для бронирования' },
      { name: 'Минимум 2 ночи' },
    ],
  },
  {
    id: 5,
    name: 'Комфорт',
    slug: 'modular-comfort',
    img: cottageExterior,
    description: 'Уютный модульный дом для небольшой компании. 1 спальня, компактная кухня, уютная гостиная.',
    conveniences: 'Wi-Fi, отопление, кухня, санузел, терраса',
    include: 'Постельное белье, полотенца, посуда',
    travelLineId: '5',
    photo_gallery_set: [
      {
        img: cottageExterior,
        name: 'Внешний вид',
      },
      {
        img: cottageInterior,
        name: 'Интерьер',
      },
      {
        img: galleryForestWalk,
        name: 'Окрестности',
      },
    ],
    price_set: [
      { name: 'Будни (1-2 чел.)', cost: 4000 },
      { name: 'Будни (3-4 чел.)', cost: 7000 },
      { name: 'Выходные (1-2 чел.)', cost: 6000 },
      { name: 'Выходные (3-4 чел.)', cost: 10000 },
    ],
    special_price_set: [
      { name: 'Новогодние праздники', cost: 15000 },
    ],
    availability_set: [
      { name: 'Доступен для бронирования' },
      { name: 'Минимум 1 ночь' },
    ],
  },
]

// Реактивные данные
const houseList = ref(mockHouseList)
const modularHouseList = ref(mockModularHouseList)
const isShowModalHouse = ref(false)
const selectLodge = ref({})

// Рефы для секций (для скролла)
const woodenSectionRef = ref(null)
const modularSectionRef = ref(null)

const route = useRoute()

const closeModal = () => {
  if (import.meta.client) {
    document.body.classList.remove('modal-open')
  }
  isShowModalHouse.value = false
}

const selLodge = (lodge) => {
  selectLodge.value = lodge
  isShowModalHouse.value = true
}

// Функция для установки активного дома
const setActiveHouse = async (houseId, houseType) => {
  if (!import.meta.client) return

  await nextTick()

  if (houseType === 'wooden') {
    const index = houseList.value.findIndex((house) => house.id === houseId)
    if (index !== -1) {
      // Используем метод из компонента WoodenHousesSection
      // Для этого нужно передать ref или использовать событие
      // Пока используем простой способ через query параметры
      // Компонент сам обработает это через prop
    }
  } else if (houseType === 'modular') {
    const index = modularHouseList.value.findIndex((house) => house.id === houseId)
    if (index !== -1) {
      // Аналогично для модульных домов
    }
  }
}

// Инициализация
onMounted(async () => {
  if (import.meta.client) {
    // Проверяем query параметры
    const houseId = route.query.houseId
    const houseType = route.query.houseType

    if (houseId && houseType) {
      // Ждем рендеринга компонентов
      await nextTick()

      // Если модульный дом, скроллим к секции модульных домов
      if (houseType === 'modular') {
        // Даем время компонентам установить правильный индекс
        setTimeout(() => {
          const modularSection = document.querySelector('[data-section="modular"]')
          if (modularSection) {
            // Вычисляем позицию с учетом отступа
            const yOffset = -80 // Отступ сверху
            const y = modularSection.getBoundingClientRect().top + window.pageYOffset + yOffset
            window.scrollTo({ top: y, behavior: 'smooth' })
          }
        }, 500)
      } else {
        // Для деревянных домов скроллим в начало
        window.scrollTo({ top: 0, behavior: 'smooth' })
      }
    } else {
      window.scrollTo({ top: 0, behavior: 'smooth' })
    }
  }
})
</script>

<template>
  <div>
    <!-- Временно закомментированы компоненты, которые нужно будет добавить позже -->
    <!-- <header-main /> -->

    <WoodenHousesSection
      ref="woodenSectionRef"
      :houses="houseList"
      title="Деревянные дома"
      :initial-house-id="route.query.houseType === 'wooden' ? parseInt(route.query.houseId) : undefined"
    />
    <ModularHousesSection
      ref="modularSectionRef"
      :houses="modularHouseList"
      title="Модульные дома"
      :initial-house-id="route.query.houseType === 'modular' ? parseInt(route.query.houseId) : undefined"
    />

  </div>
</template>

<style scoped>
.modal-mask {
  position: fixed;
  top: 0;
  height: 100vh;
  width: 100%;
  background-color: #ece8e3;
  z-index: 200;
}

/* HOUSE DETAIL */
.modalBottom-enter-active {
  animation: animatebottom 1s;
}

.modalBottom-leave-active {
  animation: animatebottom 1s reverse;
}

@keyframes animatebottom {
  from {
    top: 100%;
    opacity: 0;
  }

  to {
    top: 0%;
    opacity: 1;
  }
}
</style>
