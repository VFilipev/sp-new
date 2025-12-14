<script setup>
import forestWalkImage from '~/assets/resort/peaceful-forest-walk.jpg'
import windowViewImage from '~/assets/resort/peaceful-window-view.jpg'
import banyaImage from '~/assets/resort/peaceful-banya.jpg'

const activities = [
  { image: forestWalkImage, title: 'Прогулки по лесу', description: 'Хвойный лес и живописные тропы' },
  { image: windowViewImage, title: 'Тишина и уединение', description: 'Отключитесь от городской суеты' },
  { image: banyaImage, title: 'Традиционная баня', description: 'Русская баня с чаном' },
]
</script>

<template>
  <section class="bg-background py-20">
    <div class="container mx-auto px-6 md:px-8">
      <div class="animate-fade-in mb-12 text-center">
        <h2 class="mb-4 text-4xl font-serif text-primary md:text-5xl">Спокойный отдых</h2>
        <p class="mx-auto max-w-2xl text-lg text-muted-foreground">
          Здесь время течет медленнее, даря вам возможность восстановить силы и обрести гармонию с природой
        </p>
      </div>

      <div class="grid gap-6 md:grid-cols-3">
        <div
          v-for="(activity, index) in activities"
          :key="activity.title"
          class="group relative overflow-hidden rounded-2xl border border-border/50 bg-white/70 transition-all duration-500 hover:scale-105 hover:shadow-2xl animate-fade-in"
          :style="{ animationDelay: `${index * 150}ms` }"
        >
          <div class="relative h-[400px] overflow-hidden">
            <img :src="activity.image" :alt="activity.title" class="h-full w-full object-cover transition-transform duration-700 group-hover:scale-110" />
            <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/40 to-transparent" />
            <div class="absolute inset-0 flex flex-col justify-end p-6 text-white">
              <h3 class="mb-2 text-2xl font-semibold transition-transform duration-300 group-hover:-translate-y-1">
                {{ activity.title }}
              </h3>
              <p class="text-white/90 transition-all duration-300 group-hover:-translate-y-1">
                {{ activity.description }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>




