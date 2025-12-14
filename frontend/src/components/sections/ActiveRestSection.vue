<script setup>
import { ref } from 'vue'
import snowmobileImage from '@/assets/resort/active-snowmobile.jpg'
import skatingImage from '@/assets/resort/active-skating.jpg'
import skiingImage from '@/assets/resort/active-skiing.jpg'
import skatingVideo from '@/assets/resort/active-skating-video.mp4'
import snowmobileVideo from '@/assets/resort/active-snowmobile-video.mp4'

const hoveredIndex = ref(null)
const videoRefs = ref([])

const setVideoRef = (index) => (el) => {
  if (el) {
    videoRefs.value[index] = el
  }
}

const activities = [
  { image: snowmobileImage, video: snowmobileVideo, title: 'Снегоходы', description: 'Зимние приключения на скоростных снегоходах' },
  { image: skatingImage, video: skatingVideo, title: 'Коньки', description: 'Катание на коньках на открытом катке' },
  { image: skiingImage, title: 'Лыжи', description: 'Лыжные прогулки по живописным трассам' },
]

const handleMouseEnter = (index) => {
  hoveredIndex.value = index
  const video = videoRefs.value[index]
  if (activities[index].video && video) {
    video.currentTime = 0
    video.play().catch(() => {})
  }
}

const handleMouseLeave = (index) => {
  const video = videoRefs.value[index]
  if (video) {
    video.pause()
  }
  hoveredIndex.value = null
}
</script>

<template>
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
</template>




