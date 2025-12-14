<script setup>
import { computed, ref } from 'vue'

const props = defineProps({
  images: {
    type: Array,
    default: () => [],
  },
  heightClass: {
    type: String,
    default: 'h-52',
  },
})

const activeIndex = ref(0)

const hasMultiple = computed(() => (props.images?.length || 0) > 1)

const handleMouseMove = (e) => {
  if (!hasMultiple.value) return
  const rect = e.currentTarget.getBoundingClientRect()
  const x = e.clientX - rect.left
  const sectionWidth = rect.width / props.images.length
  const newIndex = Math.min(Math.floor(x / sectionWidth), props.images.length - 1)
  if (newIndex !== activeIndex.value) {
    activeIndex.value = newIndex
  }
}

const handleMouseLeave = () => {
  activeIndex.value = 0
}
</script>

<template>
  <div
    class="relative m-3 overflow-hidden rounded-xl"
    :class="heightClass"
    @mousemove="handleMouseMove"
    @mouseleave="handleMouseLeave"
  >
    <NuxtImg
      v-for="(img, index) in images"
      :key="img + index"
      :src="img"
      :alt="`Фото ${index + 1}`"
      :width="626"
      :height="456"
      :quality="75"
      :loading="index === 0 ? 'eager' : 'lazy'"
      sizes="626px"
      class="absolute inset-0 h-full w-full object-cover transition-opacity duration-300"
      :class="index === activeIndex ? 'opacity-100' : 'opacity-0'"
    />

    <div v-if="hasMultiple" class="absolute bottom-3 left-1/2 flex -translate-x-1/2 gap-1.5">
      <div
        v-for="(_, index) in images"
        :key="'dot' + index"
        class="h-1 rounded-full transition-all duration-300"
        :class="index === activeIndex ? 'w-4 bg-white' : 'w-1.5 bg-white/50'"
      />
    </div>
  </div>
</template>

