<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import event1Image from '~/assets/resort/event1.webp'
import event2Image from '~/assets/resort/event2.webp'
import event3Image from '~/assets/resort/event3.webp'
import event5Image from '~/assets/resort/event5.webp'

const isVisible = ref(false)
const sectionRef = ref(null)

const events = [
  {
    id: 1,
    title: 'Свадьбы',
    description: 'Загородная церемония, банкетный зал, фотозоны и размещение гостей на базе отдыха.',
    image: event1Image,
  },
  {
    id: 2,
    title: 'Юбилеи',
    description: 'Уютный банкетный зал, украшение под ваш сценарий и программы с ведущими.',
    image: event2Image,
  },
  {
    id: 3,
    title: 'Корпоративы',
    description: 'Тимбилдинг на природе, конференц-зона, банкет и активный отдых круглый год.',
    image: event3Image,
  },
  {
    id: 4,
    title: 'Выпускные вечера',
    description: 'Безопасная закрытая территория, зал для выпускного вечера и программы для школьников и студентов.',
    image: event5Image,
  },
]

onMounted(() => {
  const observer = new IntersectionObserver(
    ([entry]) => {
      if (entry.isIntersecting) {
        isVisible.value = true
      }
    },
    { threshold: 0.1 }
  )

  if (sectionRef.value) {
    observer.observe(sectionRef.value)
  }

  return () => observer.disconnect()
})

onBeforeUnmount(() => {
  // Cleanup если нужно
})
</script>

<template>
  <section ref="sectionRef" class="bg-background ">
    <div class="container mx-auto px-6 md:px-8 py-20">
      <!-- Header -->
      <div class="mb-12 text-center">
        <h3
          class="mb-4 font-serif text-3xl text-primary transition-all duration-1000 md:text-4xl"
          :class="isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'"
        >
            Ваш идеальный праздник среди природы
        </h3>
        <p
          class="mx-auto max-w-2xl text-lg text-muted-foreground transition-all duration-1000 delay-200"
          :class="isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'"
        >
          Проведите свадьбу, юбилей, корпоратив или выпускной с проживанием и питанием на нашей базе отдыха
        </p>
      </div>

      <!-- Cards Grid -->
      <div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        <div
          v-for="(event, index) in events"
          :key="event.id"
          class="group relative h-80 cursor-pointer overflow-hidden rounded-2xl transition-all duration-700"
          :class="isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'"
          :style="{
            transitionDelay: isVisible ? `${300 + index * 100}ms` : '0ms',
          }"
        >
          <!-- Background Image -->
          <img
            :src="event.image"
            :alt="event.title"
            class="absolute inset-0 h-full w-full object-cover transition-transform duration-700 group-hover:scale-110"
          />

          <!-- Dark Gradient Overlay -->
          <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/30 to-transparent" />

          <!-- Content Container -->
          <div class="absolute inset-0 flex flex-col justify-end p-6">
            <!-- Title - moves up on hover -->
            <h4 class="text-xl font-semibold text-white transition-all duration-500 ease-out md:text-2xl group-hover:-translate-y-24">
              {{ event.title }}
            </h4>

            <!-- Description & Button - appears on hover -->
            <div class="absolute bottom-6 left-6 right-6 translate-y-4 opacity-0 transition-all duration-500 ease-out group-hover:translate-y-0 group-hover:opacity-100">
              <p class="mb-4 line-clamp-2 text-sm text-white/90">
                {{ event.description }}
              </p>
              <button
                class="rounded-md border border-white bg-transparent px-4 py-2 text-sm text-white transition-colors hover:bg-white hover:text-primary"
              >
                Узнать условия
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

