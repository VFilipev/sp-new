<script setup>
import { onBeforeUnmount, onMounted, ref, computed } from "vue";
import basePlanImage from "~/assets/resort/base-plan.webp";

const isVisible = ref(false);
const sectionRef = ref(null);

const {statistics: stats, error: statisticsError} = useStatistics({ordering: 'order'});
const { galleryImages, error: galleryError } = useGallery({ position: 'main', ordering: 'order' });

// Распределяем изображения по колонкам на основе поля column
const leftColumn = computed(() => {
  return galleryImages.value
    .filter(img => img.position === 'main' && img.column === 'left' && img.is_active)
    .sort((a, b) => a.order - b.order);
});

const centerColumn = computed(() => {
  return galleryImages.value
    .filter(img => img.position === 'main' && img.column === 'center' && img.is_active)
    .sort((a, b) => a.order - b.order);
});

const rightColumn = computed(() => {
  return galleryImages.value
    .filter(img => img.position === 'main' && img.column === 'right' && img.is_active)
    .sort((a, b) => a.order - b.order);
});


let observer;

onMounted(() => {
  if (sectionRef.value) {
    observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          isVisible.value = true;
        }
      },
      { threshold: 0.1 }
    );

    observer.observe(sectionRef.value);
  }
});

onBeforeUnmount(() => {
  if (observer) {
    observer.disconnect();
  }
});
</script>

<template>
  <section ref="sectionRef" class="bg-background py-20">
    <div class="container mx-auto px-6 md:px-8">
      <div class="mb-16">
        <div class="grid grid-cols-1 gap-3 md:grid-cols-3">
          <div class="flex flex-col gap-3">
            <div
              v-for="(image, index) in leftColumn"
              :key="`left-${image.id}`"
              class="transform overflow-hidden rounded-sm border border-border/50 transition-all duration-700"
              :class="
                isVisible
                  ? 'opacity-100 translate-y-0'
                  : 'opacity-0 translate-y-10'
              "
              :style="{
                transitionDelay: isVisible ? `${index * 150}ms` : '0ms',
              }"
            >
              <div class="relative h-[450px] overflow-hidden">
                <NuxtImg
                  :src="image.image_webp_url"
                  :alt="image.alt_text || 'Изображение галереи'"
                  :width="414"
                  :height="552"
                  :placeholder="image.image_placeholder_url"
                  loading="lazy"
                  sizes="414px"
                  class="h-full w-full object-cover"
                />
              </div>
            </div>
          </div>

          <div class="flex flex-col gap-3">
            <div
              v-for="(image, index) in centerColumn"
              :key="`center-${image.id}`"
              class="transform overflow-hidden rounded-sm border border-border/50 transition-all duration-700"
              :class="
                isVisible
                  ? 'opacity-100 translate-y-0'
                  : 'opacity-0 translate-y-10'
              "
              :style="{
                transitionDelay: isVisible ? `${(index + 2) * 150}ms` : '0ms',
              }"
            >
              <div class="relative h-[296px] overflow-hidden">
                <NuxtImg
                  :src="image.image_webp_url"
                  :alt="image.alt_text || 'Изображение галереи'"
                  :width="414"
                  :height="296"
                  :placeholder="image.image_placeholder_url"
                  loading="lazy"
                  sizes="414px"
                  class="h-full w-full object-cover"
                />
              </div>
            </div>
          </div>

          <div class="flex flex-col gap-3">
            <div
              v-for="(image, index) in rightColumn"
              :key="`right-${image.id}`"
              class="transform overflow-hidden rounded-sm border border-border/50 transition-all duration-700"
              :class="
                isVisible
                  ? 'opacity-100 translate-y-0'
                  : 'opacity-0 translate-y-10'
              "
              :style="{
                transitionDelay: isVisible ? `${(index + 5) * 150}ms` : '0ms',
              }"
            >
              <div class="relative h-[450px] overflow-hidden">
                <NuxtImg
                  :src="image.image_webp_url"
                  :alt="image.alt_text || 'Изображение галереи'"
                  :width="414"
                  :height="552"
                  :placeholder="image.image_placeholder_url"
                  loading="lazy"
                  sizes="414px"
                  class="h-full w-full object-cover"
                />
              </div>
            </div>
          </div>
        </div>
      </div>

      <div
        class="mb-16 grid items-center gap-10 lg:grid-cols-[1.3fr_1fr]"
        :class="
          isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'
        "
        :style="{ transitionDelay: isVisible ? '400ms' : '0ms' }"
      >
        <div
          class="overflow-hidden rounded-2xl border border-border/50 bg-card/80 shadow-2xl backdrop-blur"
        >
          <div class="relative">
            <NuxtImg
              :src="basePlanImage"
              :width="694"
              :height="486"
              alt="План базы отдыха Строгановские Просторы"
              sizes="694px"
              class="h-auto w-full"
            />
            <div
              class="pointer-events-none absolute inset-0 bg-gradient-to-t from-black/10 to-transparent"
            />
          </div>
        </div>

        <div class="space-y-4">
          <h3 class="text-3xl font-serif text-primary md:text-4xl">
            План базы отдыха
          </h3>
          <p class="text-lg leading-relaxed text-muted-foreground">
            Откройте для себя место, где каждый уголок создан для незабываемых
            моментов.
          </p>
          <p class="text-lg leading-relaxed text-muted-foreground">
            Уютные домики среди вековых сосен, живописная набережная реки Камы,
            зоны для активного отдыха и тихие уголки для уединения — всё
            расположено так, чтобы ваш отдых стал по-настоящему особенным.
          </p>
        </div>
      </div>

      <div>
        <h3
          class="mb-10 text-center text-3xl font-serif text-primary transition-all duration-700 md:text-4xl"
          :class="
            isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'
          "
          :style="{ transitionDelay: isVisible ? '200ms' : '0ms' }"
        >
          Цифры и факты
        </h3>

        <div class="grid grid-cols-2 gap-4 md:grid-cols-3 lg:grid-cols-5">
          <div
            v-for="(stat, index) in stats"
            :key="stat?.id"
            class="group transform bg-[hsl(var(--stats-card))] p-6 text-center transition-all duration-700 rounded-2xl"
            :class="
              isVisible
                ? 'opacity-100 translate-y-0'
                : 'opacity-0 translate-y-10'
            "
            :style="{
              transitionDelay: isVisible ? `${200 + index * 80}ms` : '0ms',
            }"
          >
            <div class="space-y-2">
              <div
                class="text-4xl font-bold text-[hsl(var(--stats-card-foreground))] md:text-5xl"
              >
                {{ stat?.number }}
              </div>
              <div
                class="text-sm font-semibold text-[hsl(var(--stats-card-foreground)/0.9)] md:text-base"
              >
                {{ stat?.label }}
              </div>
              <div
                class="text-xs leading-relaxed text-[hsl(var(--stats-card-foreground)/0.7)]"
              >
                {{ stat?.description }}
              </div>
            </div>
          </div>
        </div>

        <!-- <div class="flex justify-center mt-10">
          <div style="width:360px;height:600px;overflow:hidden;position:relative;">
            <iframe
              style="width:100%;height:100%;border:1px solid #e6e6e6;border-radius:8px;box-sizing:border-box"
              src="https://yandex.ru/maps-reviews-widget/1277179994?comments"
            ></iframe>
            <a
              href="https://yandex.ru/maps/org/stroganovskiye_prostory/1277179994/"
              target="_blank"
              style="box-sizing:border-box;text-decoration:none;color:#b3b3b3;font-size:10px;font-family:YS Text,sans-serif;padding:0 20px;position:absolute;bottom:8px;width:100%;text-align:center;left:0;overflow:hidden;text-overflow:ellipsis;display:block;max-height:14px;white-space:nowrap;padding:0 16px;box-sizing:border-box"
            >Строгановские просторы на карте Пермского края — Яндекс Карты</a>
          </div>
        </div> -->
      </div>
    </div>
  </section>
</template>
