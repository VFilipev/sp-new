<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import news1Image from '~/assets/resort/news1.jpg'
import news2Image from '~/assets/resort/news2.jpg'
import news3Image from '~/assets/resort/news3.jpg'
import news4Image from '~/assets/resort/news4.jpg'

const isVisible = ref(false)
const sectionRef = ref(null)

const news = [
  {
    id: 1,
    title: 'Афиша на ноябрь',
    date: '01 ноября 2025',
    image: news1Image,
  },
  {
    id: 2,
    title: 'Открыта бронь на квадротур до Чермоза',
    date: '07 сентября 2025',
    image: news2Image,
  },
  {
    id: 3,
    title: 'Открыта вакансия',
    date: '12 июля 2025',
    image: news3Image,
  },
  {
    id: 4,
    title: 'Акция 1 + 1',
    date: '7 мая 2025',
    image: news4Image,
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
  <section ref="sectionRef" class="bg-background py-20">
    <div class="container mx-auto px-6 md:px-8">
      <div class="mb-10 flex items-center justify-between">
        <h3
          class="font-serif text-3xl text-primary transition-all duration-1000 md:text-4xl"
          :class="isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'"
        >
          Новости
        </h3>
        <button
          class="rounded-md border border-primary bg-transparent px-4 py-2 text-primary transition-all duration-1000 hover:bg-primary hover:text-primary-foreground"
          :class="isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'"
        >
          Все новости
        </button>
      </div>

      <div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        <div
          v-for="(item, index) in news"
          :key="item.id"
          class="group cursor-pointer overflow-hidden rounded-lg border-none bg-card transition-all duration-700 hover:scale-105 hover:shadow-xl"
          :class="isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'"
          :style="{
            transitionDelay: isVisible ? `${200 + index * 100}ms` : '0ms',
          }"
        >
          <div class="aspect-[4/3] overflow-hidden">
            <img
              :src="item.image"
              :alt="item.title"
              class="h-full w-full object-cover transition-transform duration-500 group-hover:scale-110"
            />
          </div>
          <div class="space-y-2 p-4">
            <p class="text-sm text-muted-foreground">{{ item.date }}</p>
            <h4 class="line-clamp-2 text-base font-medium leading-tight text-primary">
              {{ item.title }}
            </h4>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

