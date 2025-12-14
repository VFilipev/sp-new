<script setup>
import { Teleport } from 'vue'
import ImageCarousel from './ImageCarousel.vue'

const props = defineProps({
  open: { type: Boolean, default: false },
  isClosing: { type: Boolean, default: false },
  showContent: { type: Boolean, default: false },
  meta: {
    type: Object,
    default: () => ({}),
  },
  items: {
    type: Array,
    default: () => [],
  },
})

const emit = defineEmits(['close'])

const handleClose = () => emit('close')
</script>

<template>
  <Teleport to="body">
    <div v-if="open">
      <div
        class="fixed inset-0 z-40 bg-black/70 transition-opacity duration-700"
        :class="showContent && !isClosing ? 'opacity-100' : 'opacity-0'"
        @click="handleClose"
      />

      <div
        class="fixed z-50 overflow-hidden rounded-2xl bg-background shadow-2xl"
        :class="[
          isClosing ? 'lodge-popup-collapsing' : showContent ? 'lodge-popup-expanded' : 'lodge-popup-expanding',
        ]"
      >
        <div v-if="!showContent || isClosing" class="absolute inset-0">
          <NuxtImg
            :src="meta.heroImage"
            :alt="meta.title"
            :width="1410"
            :height="940"
            :quality="80"
            loading="eager"
            sizes="1410px"
            class="h-full w-full object-cover"
          />
          <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/40 to-transparent" />
          <div class="absolute inset-0 flex flex-col justify-end p-8">
            <h3 class="mb-3 text-3xl font-serif text-white md:text-4xl">
              {{ meta.title }}
            </h3>
            <p class="text-lg text-white/90">
              {{ meta.subtitle }}
            </p>
          </div>
        </div>
        <div v-else class="absolute inset-0 bg-background" />

        <div v-if="showContent && !isClosing" class="relative flex h-full w-full flex-col">
          <div class="flex items-center justify-between border-b border-border/50 bg-background/95 p-4 backdrop-blur">
            <h3 class="text-2xl font-serif text-primary md:text-3xl">
              {{ meta.title }}
            </h3>
            <button class="rounded-full p-2 transition-colors hover:bg-secondary/80" @click="handleClose">
              <span class="sr-only">Закрыть</span>
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M6 6l12 12M18 6L6 18" />
              </svg>
            </button>
          </div>

          <div class="flex-1 overflow-y-auto">
            <div class="p-6">
              <div class="grid gap-6 md:grid-cols-3">
                <article
                  v-for="item in items"
                  :key="item.name"
                  class="overflow-hidden rounded-2xl border-0 bg-[#f5f2ed] shadow-sm transition-all duration-300 hover:shadow-xl"
                >
                  <ImageCarousel :images="item.images" />

                  <div class="px-4 pb-4">
                    <div class="mb-3 flex items-center justify-between gap-2">
                      <h4 class="text-lg font-semibold text-foreground">{{ item.name }}</h4>
                      <div class="flex items-center gap-3 text-sm">
                        <span class="font-medium text-foreground">₽ {{ item.priceFrom.toLocaleString('ru-RU') }}</span>
                        <div class="flex items-center gap-1 text-muted-foreground">
                          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 12c2.485 0 4.5-2.015 4.5-4.5S14.485 3 12 3 7.5 5.015 7.5 7.5 9.515 12 12 12zM5.25 20.25a6.75 6.75 0 1 1 13.5 0" />
                          </svg>
                          <span>до {{ item.capacityNum }} чел</span>
                        </div>
                      </div>
                    </div>

                    <p class="mb-4 text-sm leading-relaxed text-muted-foreground">
                      {{ item.description }}
                    </p>

                    <div class="flex justify-end">
                      <button
                        class="rounded-full border border-primary px-5 py-2 text-sm font-medium text-primary transition-colors hover:bg-primary hover:text-primary-foreground"
                      >
                        подробнее
                      </button>
                    </div>
                  </div>
                </article>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>

