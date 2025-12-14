<script setup>
import { ref, onMounted, onBeforeUnmount } from "vue";
import { Coffee, Sun, Moon } from "lucide-vue-next";

const isVisible = ref(false);
const activeIndex = ref(0);
const activeMeal = ref(null);
const sectionRef = ref(null);
const containerRef = ref(null);

// Placeholder images - можно заменить на реальные изображения
const restaurantImages = [
  "/src/assets/resort/rest1.jpg",
  "/src/assets/resort/rest2.jpg",
  "/src/assets/resort/rest3.jpg",
];

const mealTypes = [
  {
    icon: Coffee,
    title: "Завтрак",
    description: "Плотный завтрак с 8:00",
  },
  {
    icon: Sun,
    title: "Обед",
    description: "Домашние обеды с 12:00",
  },
  {
    icon: Moon,
    title: "Ужин",
    description: "Атмосферные ужины с 18:00",
  },
];

const benefits = [
  "Завтрак, обед и ужин на территории базы",
  "Комбо-предложения для гостей",
  "Меню с основными блюдами, закусками и десертами",
  "Подходит для гостей с детьми и компаний",
];

const handleMouseMove = (e) => {
  if (!containerRef.value || restaurantImages.length <= 1) return;

  const rect = containerRef.value.getBoundingClientRect();
  const x = e.clientX - rect.left;
  const sectionWidth = rect.width / restaurantImages.length;
  const newIndex = Math.min(
    Math.floor(x / sectionWidth),
    restaurantImages.length - 1
  );

  if (newIndex !== activeIndex.value) {
    activeIndex.value = newIndex;
  }
};

const handleMouseLeave = () => {
  activeIndex.value = 0;
};

onMounted(() => {
  const observer = new IntersectionObserver(
    ([entry]) => {
      if (entry.isIntersecting) {
        isVisible.value = true;
      }
    },
    { threshold: 0.1 }
  );

  if (sectionRef.value) {
    observer.observe(sectionRef.value);
  }

  return () => observer.disconnect();
});

onBeforeUnmount(() => {
  // Cleanup если нужно
});
</script>

<template>
  <section ref="sectionRef" class="bg-background py-16 md:py-24">
    <div class="container mx-auto px-4">
      <!-- Main Content -->
      <div
        class="grid items-center gap-8 transition-all duration-700 delay-200 lg:grid-cols-2 lg:gap-12"
        :class="
          isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'
        "
      >
        <!-- Photo Section with Carousel -->
        <div class="relative overflow-hidden rounded-2xl">
          <div class="aspect-[4/3]">
            <div
              ref="containerRef"
              class="relative h-full w-full cursor-pointer"
              @mousemove="handleMouseMove"
              @mouseleave="handleMouseLeave"
            >
              <img
                v-for="(img, index) in restaurantImages"
                :key="index"
                :src="img"
                :alt="`Интерьер ресторана ${index + 1}`"
                class="absolute inset-0 h-full w-full object-cover transition-opacity duration-300"
                :class="index === activeIndex ? 'opacity-100' : 'opacity-0'"
              />

              <!-- Indicators -->
              <div
                v-if="restaurantImages.length > 1"
                class="absolute bottom-3 left-1/2 flex -translate-x-1/2 gap-1.5"
              >
                <div
                  v-for="(_, index) in restaurantImages"
                  :key="index"
                  class="h-1 rounded-full transition-all duration-300"
                  :class="
                    index === activeIndex ? 'w-4 bg-white' : 'w-1.5 bg-white/50'
                  "
                />
              </div>
            </div>
          </div>
        </div>

        <!-- Text Content -->
        <div class="space-y-8">
          <!-- Description -->
          <div>
            <h2
              class="mb-4 font-lato text-3xl font-light text-primary md:text-4xl"
            >
              Ресторан
            </h2>
            <p class="mb-6 text-lg leading-relaxed text-foreground/80">
              На базе работает ресторан: полноценные завтраки, обеды и ужины для
              гостей. Доступны готовые комбо-наборы и блюда из основного меню.
            </p>

            <!-- Benefits List -->
            <ul class="space-y-3">
              <li
                v-for="(benefit, index) in benefits"
                :key="index"
                class="flex items-start gap-3"
              >
                <span
                  class="mt-2.5 h-1.5 w-1.5 flex-shrink-0 rounded-full bg-primary"
                />
                <span class="text-foreground/70">{{ benefit }}</span>
              </li>
            </ul>
          </div>

          <!-- Meal Type Icons -->
          <div class="grid grid-cols-1 gap-3 sm:grid-cols-3">
            <button
              v-for="(meal, index) in mealTypes"
              :key="index"
              @click="activeMeal = activeMeal === index ? null : index"
              class="flex items-center gap-3 rounded-xl border px-5 py-3 transition-all duration-300"
              :class="
                activeMeal === index
                  ? 'border-primary bg-primary text-primary-foreground'
                  : 'border-border bg-card hover:border-primary/50 hover:bg-primary/5'
              "
            >
              <component :is="meal.icon" class="h-5 w-5 flex-shrink-0" />
              <div class="min-w-0 flex-1 text-left">
                <p class="text-sm font-medium">{{ meal.title }}</p>
                <p
                  class="text-xs"
                  :class="
                    activeMeal === index
                      ? 'text-primary-foreground/80'
                      : 'text-muted-foreground'
                  "
                >
                  {{ meal.description }}
                </p>
              </div>
            </button>
          </div>

          <!-- Action Buttons -->
          <div class="flex flex-wrap gap-4">
            <button
              class="rounded-xl bg-primary px-8 py-3 text-primary-foreground transition-colors hover:bg-primary/90"
            >
              Посмотреть меню
            </button>
            <button
              class="rounded-xl border border-primary/30 bg-transparent px-8 py-3 text-primary transition-colors hover:bg-primary/5"
            >
              Комбо-предложения
            </button>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
