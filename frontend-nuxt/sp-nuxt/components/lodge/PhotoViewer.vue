<script setup>
import { ref, computed, watch, onMounted, onUnmounted, Teleport } from 'vue'
import { Swiper, SwiperSlide } from 'swiper/vue'
import { Navigation, Keyboard } from 'swiper/modules'
import 'swiper/css'
import 'swiper/css/navigation'

const props = defineProps({
  images: {
    type: Array,
    required: true,
  },
  initialIndex: {
    type: Number,
    default: 0,
  },
  open: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['close'])

const currentIndex = ref(props.initialIndex)
const swiperRef = ref(null)

const imageList = computed(() => {
  return props.images.map((img) => (typeof img === 'string' ? img : img.img || img.url))
})

const handleClose = () => {
  emit('close')
}

const handleBackdropClick = (e) => {
  if (e.target === e.currentTarget) {
    handleClose()
  }
}

const goToSlide = (index) => {
  if (swiperRef.value) {
    swiperRef.value.slideTo(index)
  }
}

const onSwiper = (swiper) => {
  swiperRef.value = swiper
  if (props.initialIndex !== undefined) {
    swiper.slideTo(props.initialIndex)
  }
}

const onSlideChange = (swiper) => {
  currentIndex.value = swiper.activeIndex
}

watch(
  () => props.initialIndex,
  (newIndex) => {
    if (swiperRef.value && newIndex !== undefined) {
      swiperRef.value.slideTo(newIndex)
    }
  }
)

watch(
  () => props.open,
  (isOpen) => {
    if (isOpen) {
      document.body.style.overflow = 'hidden'
      if (swiperRef.value && props.initialIndex !== undefined) {
        swiperRef.value.slideTo(props.initialIndex)
      }
    } else {
      document.body.style.overflow = ''
    }
  }
)

const handleKeydown = (e) => {
  if (!props.open) return

  if (e.key === 'Escape') {
    handleClose()
  } else if (e.key === 'ArrowLeft' && swiperRef.value) {
    swiperRef.value.slidePrev()
  } else if (e.key === 'ArrowRight' && swiperRef.value) {
    swiperRef.value.slideNext()
  }
}

onMounted(() => {
  window.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeydown)
  document.body.style.overflow = ''
})
</script>

<template>
  <Teleport to="body">
    <Transition name="photo-viewer">
      <div v-if="open" class="photo-viewer" @click="handleBackdropClick">
        <div class="photo-viewer__close" @click="handleClose">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </div>

        <div class="photo-viewer__container" @click.stop>
          <Swiper
            :modules="[Navigation, Keyboard]"
            :slides-per-view="1"
            :space-between="0"
            :navigation="true"
            :keyboard="{ enabled: true }"
            :initial-slide="initialIndex"
            class="photo-viewer__swiper"
            @swiper="onSwiper"
            @slideChange="onSlideChange"
          >
            <SwiperSlide v-for="(image, index) in imageList" :key="index" class="photo-viewer__slide">
              <div class="photo-viewer__image-wrapper">
                <img :src="image" :alt="`Фото ${index + 1}`" class="photo-viewer__image" />
              </div>
            </SwiperSlide>
          </Swiper>

          <div class="photo-viewer__counter">
            {{ currentIndex + 1 }} / {{ imageList.length }}
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.photo-viewer {
  position: fixed;
  inset: 0;
  z-index: 9999;
  background-color: rgba(0, 0, 0, 0.95);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.photo-viewer__container {
  position: relative;
  width: 100%;
  max-width: 1400px;
  height: 100%;
  max-height: 90vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.photo-viewer__swiper {
  width: 100%;
  height: 100%;
}

.photo-viewer__slide {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
}

.photo-viewer__image-wrapper {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.photo-viewer__image {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  border-radius: 8px;
  user-select: none;
}

.photo-viewer__close {
  position: absolute;
  top: 20px;
  right: 20px;
  z-index: 10000;
  width: 48px;
  height: 48px;
  background-color: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  color: white;
}

.photo-viewer__close:hover {
  background-color: rgba(255, 255, 255, 0.2);
  transform: scale(1.1);
}

.photo-viewer__close svg {
  width: 24px;
  height: 24px;
}

.photo-viewer__counter {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  background-color: rgba(0, 0, 0, 0.6);
  color: white;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 14px;
  font-family: 'Lato', sans-serif;
  font-weight: 400;
  z-index: 10000;
}

/* Навигация Swiper */
:global(.photo-viewer__swiper .swiper-button-next),
:global(.photo-viewer__swiper .swiper-button-prev) {
  color: white;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(10px);
  width: 56px;
  height: 56px;
  border-radius: 50%;
  border: 1px solid rgba(255, 255, 255, 0.15);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  margin-top: 0;
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  align-items: center;
  justify-content: center;
}

:global(.photo-viewer__swiper .swiper-button-next) {
  right: 24px;
}

:global(.photo-viewer__swiper .swiper-button-prev) {
  left: 24px;
}

:global(.photo-viewer__swiper .swiper-button-next:hover),
:global(.photo-viewer__swiper .swiper-button-prev:hover) {
  background: rgba(0, 0, 0, 0.7);
  border-color: rgba(255, 255, 255, 0.3);
  transform: translateY(-50%) scale(1.05);
}

:global(.photo-viewer__swiper .swiper-button-next:active),
:global(.photo-viewer__swiper .swiper-button-prev:active) {
  transform: translateY(-50%) scale(0.95);
}

:global(.photo-viewer__swiper .swiper-button-next::after),
:global(.photo-viewer__swiper .swiper-button-prev::after) {
  font-size: 9px;
  font-weight: 600;
  letter-spacing: -0.5px;
}

/* Масштабирование SVG иконок в кнопках навигации */
:global(.photo-viewer__swiper .swiper-button-next svg),
:global(.photo-viewer__swiper .swiper-button-prev svg) {
  width: 11px !important;
  height: 11px !important;
}

:global(.photo-viewer__swiper .swiper-button-next .swiper-navigation-icon),
:global(.photo-viewer__swiper .swiper-button-prev .swiper-navigation-icon) {
  width: 11px !important;
  height: 11px !important;
}

:global(.photo-viewer__swiper .swiper-button-disabled) {
  opacity: 0.3;
  cursor: not-allowed;
}

/* Анимации */
.photo-viewer-enter-active,
.photo-viewer-leave-active {
  transition: opacity 0.3s ease;
}

.photo-viewer-enter-from,
.photo-viewer-leave-to {
  opacity: 0;
}

.photo-viewer-enter-active .photo-viewer__container,
.photo-viewer-leave-active .photo-viewer__container {
  transition: transform 0.3s ease, opacity 0.3s ease;
}

.photo-viewer-enter-from .photo-viewer__container,
.photo-viewer-leave-to .photo-viewer__container {
  transform: scale(0.9);
  opacity: 0;
}

@media (max-width: 768px) {
  .photo-viewer__close {
    width: 40px;
    height: 40px;
    top: 10px;
    right: 10px;
  }

  .photo-viewer__close svg {
    width: 20px;
    height: 20px;
  }

  .photo-viewer__counter {
    bottom: 10px;
    font-size: 12px;
    padding: 6px 12px;
  }

  :global(.photo-viewer__swiper .swiper-button-next),
  :global(.photo-viewer__swiper .swiper-button-prev) {
    width: 44px;
    height: 44px;
  }

  :global(.photo-viewer__swiper .swiper-button-next) {
    right: 12px;
  }

  :global(.photo-viewer__swiper .swiper-button-prev) {
    left: 12px;
  }

  :global(.photo-viewer__swiper .swiper-button-next::after),
  :global(.photo-viewer__swiper .swiper-button-prev::after) {
    font-size: 7px;
  }

  :global(.photo-viewer__swiper .swiper-button-next svg),
  :global(.photo-viewer__swiper .swiper-button-prev svg) {
    width: 8px !important;
    height: 8px !important;
  }

  :global(.photo-viewer__swiper .swiper-button-next .swiper-navigation-icon),
  :global(.photo-viewer__swiper .swiper-button-prev .swiper-navigation-icon) {
    width: 8px !important;
    height: 8px !important;
  }
}
</style>

