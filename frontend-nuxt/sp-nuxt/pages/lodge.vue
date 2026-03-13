<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import WoodenHousesSection from '~/components/lodge/WoodenHousesSection.vue'
import ModularHousesSection from '~/components/lodge/ModularHousesSection.vue'
import { useLodgeTypes } from '~/composables/useLodges'
// import HeaderNavigation from '../components/sections/HeaderNavigation.vue'

// Загружаем типы размещения с сервера
const { types: lodgeTypes } = useLodgeTypes()

// Функция для преобразования данных с сервера в формат для компонентов
const transformLodgeData = (lodge) => {
  // Преобразуем изображения из сервера в формат для галереи
  let photoGallery = []
  if (lodge.images && lodge.images.length > 0) {
    // Используем реальные изображения с сервера
    photoGallery = lodge.images.map((img, index) => ({
      img: img.image_webp_url || img.image_url || img.image_variants?.main || img.image_variants?.card,
      name: img.alt_text || `Фото ${index + 1}`,
    }))
  }

  // Используем данные с сервера для главного изображения
  const mainImage = photoGallery.length > 0
    ? photoGallery[0].img
    : ''

  return {
    id: lodge.id,
    name: lodge.name,
    slug: lodge.slug,
    img: mainImage,
    description: lodge.short_description || lodge.description || '',
    conveniences: lodge.conveniences || '',
    include: lodge.include || '',
    photo_gallery_set: photoGallery,
    price_set: lodge.price_set || [],
    special_price_set: lodge.special_price_set || [],
    availability_set: lodge.availability_set || [],
  }
}

// Преобразуем данные с сервера в формат для компонентов
const houseList = computed(() => {
  if (!lodgeTypes.value || lodgeTypes.value.length === 0) {
    return []
  }

  // Находим тип "Коттеджи" (деревянные дома)
  const cottagesType = lodgeTypes.value.find(type =>
    type.slug === 'kottedzhi' ||
    type.name.toLowerCase().includes('коттедж') ||
    type.name.toLowerCase().includes('деревянн')
  )

  if (cottagesType && cottagesType.lodges && cottagesType.lodges.length > 0) {
    return cottagesType.lodges.map((lodge) => transformLodgeData(lodge))
  }

  return []
})

const modularHouseList = computed(() => {
  if (!lodgeTypes.value || lodgeTypes.value.length === 0) {
    return []
  }

  // Находим тип "Модульные дома"
  const modularType = lodgeTypes.value.find(type =>
    type.slug === 'modulnye-doma' ||
    type.name.toLowerCase().includes('модульн')
  )

  if (modularType && modularType.lodges && modularType.lodges.length > 0) {
    return modularType.lodges.map((lodge) => transformLodgeData(lodge))
  }

  return []
})

// Реактивные данные
const isShowModalHouse = ref(false)
const selectLodge = ref({})

// Рефы для секций (для скролла)
const woodenSectionRef = ref(null)
const modularSectionRef = ref(null)

const route = useRoute()

// Computed свойства для начальных ID домов
const initialWoodenHouseId = computed(() => {
  if (route.query.houseType === 'wooden' && route.query.houseId) {
    const id = parseInt(route.query.houseId)
    return isNaN(id) ? undefined : id
  }
  return undefined
})

const initialModularHouseId = computed(() => {
  if (route.query.houseType === 'modular' && route.query.houseId) {
    const id = parseInt(route.query.houseId)
    return isNaN(id) ? undefined : id
  }
  return undefined
})

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
    <HeaderNavigation :stick="false" />
    <WoodenHousesSection
      ref="woodenSectionRef"
      :houses="houseList"
      title="Деревянные дома"
      :initial-house-id="initialWoodenHouseId"
    />
    <ModularHousesSection
      ref="modularSectionRef"
      :houses="modularHouseList"
      title="Модульные дома"
      :initial-house-id="initialModularHouseId"
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
