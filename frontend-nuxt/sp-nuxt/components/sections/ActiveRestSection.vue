<script setup>
import { ref, onMounted } from 'vue'
import snowmobileImage from '~/assets/resort/active-snowmobile.jpg'
import skatingImage from '~/assets/resort/active-skating.jpg'
import skiingImage from '~/assets/resort/active-skiing.jpg'
import skatingVideo from '~/assets/resort/active-skating-video.mp4'
import snowmobileVideo from '~/assets/resort/active-snowmobile-video.mp4'

// Компонент использует video API для hover эффектов, поэтому рендерится только на клиенте

const hoveredIndex = ref(null)
const videoRefs = ref([])
const videoUnlocked = ref(false)

const setVideoRef = (index) => (el) => {
  if (el && process.client) {
    videoRefs.value[index] = el
  }
}

const activities = [
  { image: snowmobileImage, video: snowmobileVideo, title: 'Снегоходы', description: 'Зимние приключения на скоростных снегоходах' },
  { image: skatingImage, video: skatingVideo, title: 'Коньки', description: 'Катание на коньках на открытом катке' },
  { image: skiingImage, title: 'Лыжи', description: 'Лыжные прогулки по живописным трассам' },
]

const unlockVideo = () => {
  if (!process.client) return
  videoUnlocked.value = true
}

const handleMouseEnter = (index) => {
  if (!process.client) return

  // Разблокируем видео при первом взаимодействии
  if (!videoUnlocked.value) {
    unlockVideo()
  }

  hoveredIndex.value = index
  const video = videoRefs.value[index]

  if (activities[index].video && video && videoUnlocked.value) {
    // Если видео уже воспроизводится, просто продолжаем
    if (!video.paused) {
      return
    }

    // Сбрасываем время только если видео не воспроизводится
    if (video.readyState >= 2) {
      // HAVE_CURRENT_DATA или выше - можно воспроизводить
      video.currentTime = 0
      const playPromise = video.play()
      if (playPromise !== undefined) {
        playPromise
          .then(() => {
            // Воспроизведение успешно началось
          })
          .catch((error) => {
            // Игнорируем ошибки AbortError - они возникают при быстрых переключениях
            if (error.name !== 'AbortError') {
              // Тихо игнорируем другие ошибки
            }
          })
      }
    } else {
      // Если видео еще не загружено, ждем события loadeddata
      const onLoadedData = () => {
        // Проверяем, что мы все еще на hover (не ушли)
        if (hoveredIndex.value === index && video) {
          video.currentTime = 0
          const playPromise = video.play()
          if (playPromise !== undefined) {
            playPromise.catch(() => {
              // Игнорируем все ошибки
            })
          }
        }
        video.removeEventListener('loadeddata', onLoadedData)
      }

      // Добавляем обработчик только если его еще нет
      if (!video.hasAttribute('data-listener-added')) {
        video.addEventListener('loadeddata', onLoadedData)
        video.setAttribute('data-listener-added', 'true')
      }
    }
  }
}

const handleMouseLeave = (index) => {
  if (!process.client) return

  const video = videoRefs.value[index]
  if (video) {
    video.pause()
    video.currentTime = 0 // Сбрасываем на начало
  }
  hoveredIndex.value = null
}

onMounted(() => {
  if (process.client) {
    // Попытка автоматически разблокировать видео при монтировании
    // Некоторые браузеры позволяют autoplay после загрузки страницы
    const testVideo = document.createElement('video')
    testVideo.muted = true
    testVideo.playsInline = true
    const testPromise = testVideo.play()
    if (testPromise !== undefined) {
      testPromise
        .then(() => {
          videoUnlocked.value = true
        })
        .catch(() => {
          // Автоматическая разблокировка не удалась, потребуется пользовательское взаимодействие
        })
    }
  }
})
</script>

<template>
  <ClientOnly>
    <section id="active" class="bg-background py-20">
    <div class="container mx-auto px-6 md:px-8">
      <div class="animate-fade-in mb-12 text-center">
        <h2 class="mb-4 text-4xl font-serif text-primary md:text-5xl">Активный отдых</h2>
        <p class="mx-auto max-w-2xl text-lg text-muted-foreground">
          Почувствуйте прилив адреналина и испытайте незабываемые эмоции среди уральской природы
        </p>
      </div>

      <div class="grid gap-6 md:grid-cols-3">
        <div
          v-for="(activity, index) in activities"
          :key="activity.title"
          class="group relative overflow-hidden rounded-2xl border border-border/50 bg-white/70 transition-all duration-500 hover:scale-105 hover:shadow-2xl animate-fade-in"
          :style="{ animationDelay: `${index * 150}ms` }"
          @click="unlockVideo"
          @mouseenter="handleMouseEnter(index)"
          @mouseleave="handleMouseLeave(index)"
        >
          <div class="relative h-[400px] overflow-hidden">
            <img :src="activity.image" :alt="activity.title" class="h-full w-full object-cover transition-transform duration-700 group-hover:scale-105" />
            <video
              v-if="activity.video"
              :ref="setVideoRef(index)"
              :src="activity.video"
              muted
              loop
              playsinline
              preload="metadata"
              class="absolute inset-0 h-full w-full object-cover transition-all duration-1000 ease-out"
              :class="hoveredIndex === index ? 'opacity-100 scale-100' : 'opacity-0 scale-105'"
            />
            <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/40 to-transparent" />
            <div class="absolute inset-0 flex flex-col justify-end p-6 text-white">
              <h3 class="mb-2 text-2xl font-semibold transition-transform duration-300 group-hover:-translate-y-1">{{ activity.title }}</h3>
              <p class="text-white/90 transition-all duration-300 group-hover:-translate-y-1">{{ activity.description }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
  </ClientOnly>
</template>




