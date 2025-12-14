<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from "vue";
import { useHead } from "#imports";
import heroImage from "~/assets/resort/hero-cottages.webp";
import heroPlaceholder from "~/assets/resort/hero-cottages-plc.webp";
import { Phone } from "lucide-vue-next";
import logo from "~/assets/resort/logo.webp";
import nac from "~/assets/resort/nac.webp";

// Компонент использует window API для parallax эффекта, поэтому рендерится только на клиенте


// Компонент сам запрашивает свои данные через composable
const { data: heroData, error: heroError } = useHero()

// Логируем ошибки, но не прерываем рендеринг
if (heroError.value) {
  console.error('Error loading hero:', heroError.value)
}

// Используем данные из API или fallback
const heroImageSrc = computed(() => {
  if (heroData.value?.images && Array.isArray(heroData.value.images) && heroData.value.images.length > 0) {
    return heroData.value.images[0]?.image_webp_url || heroImage
  }
  return heroImage
})

useHead(() => ({
  link: [
    {
      rel: "preload",
      as: "image",
      href: logo,
    },
    {
      rel: "preload",
      as: "image",
      href: nac,
    },
  ],
}))

const scrollY = ref(0);
const parallaxEnabled = ref(false);

const parallaxStyle = computed(() => {
  if (!parallaxEnabled.value) {
    return {
      transform: "translateY(0px) scale(1.05)",
    };
  }
  return {
    transform: `translateY(${scrollY.value * 0.5}px) scale(1.1)`,
  };
});

const handleScroll = () => {
  if (!parallaxEnabled.value) return;
  scrollY.value = window.scrollY;
};

onMounted(() => {
  if (!import.meta.client) return;

  const prefersReducedMotion = window.matchMedia?.(
    "(prefers-reduced-motion: reduce)"
  ).matches;
  const isDesktop = window.matchMedia?.("(min-width: 768px)").matches;

  parallaxEnabled.value = !prefersReducedMotion && isDesktop;

  if (parallaxEnabled.value) {
    window.addEventListener("scroll", handleScroll, { passive: true });
  }
});

onBeforeUnmount(() => {
  if (parallaxEnabled.value && import.meta.client) {
    window.removeEventListener("scroll", handleScroll);
  }
});
</script>

<template>
  <section
    class="relative flex min-h-screen items-center justify-center overflow-hidden"
  >
  <div class="absolute inset-0 z-0">
    <NuxtImg
      :src="heroImageSrc"
      alt="Коттеджи базы отдыха Строгановские Просторы зимой"
      :width="1410"
      :height="940"
      :quality="80"
      class="h-full w-full object-cover transition-transform duration-200 ease-out"
      :style="parallaxStyle"
      loading="eager"
      decoding="async"
      fetchpriority="high"
      sizes="100vw"
      :preload="true"
      format="webp"
      :placeholder="heroPlaceholder"
    />
    <div
      class="absolute inset-0 bg-gradient-to-b from-primary/70 via-primary/50 to-primary/70"
    />
  </div>

  <nav class="animate-fade-in absolute left-0 right-0 top-0 z-20 p-6 md:p-8">
    <div class="container mx-auto flex items-center justify-between">
      <div class="flex items-center gap-8">
        <div class="flex items-center">
          <NuxtImg
            :src="logo"
            alt="Строгановские Просторы"
            class="h-12 transition-transform duration-300 hover:scale-105 md:h-16"
            loading="lazy"
            decoding="async"
            sizes="140px"
            :preload="true"
          />
          <div class="h-24 w-px bg-white mx-[0.8rem]"></div>
          <NuxtImg
            :src="nac"
            alt="национальные проекты"
            class="h-24"
            loading="lazy"
            decoding="async"
            sizes="150px"
            :preload="true"
          />
        </div>
        <a
          class="transition-all duration-300 text-primary-foreground hover:translate-y-[-2px] hover:text-primary-foreground/80"
          href="#lodge"
          >о клубе</a
        >
        <a
          class="transition-all duration-300 text-primary-foreground hover:translate-y-[-2px] hover:text-primary-foreground/80"
          href="#lodge"
          >дома</a
        >
        <a
          class="transition-all duration-300 text-primary-foreground hover:translate-y-[-2px] hover:text-primary-foreground/80"
          href="#active"
          >услуги</a
        >
        <a
          class="transition-all duration-300 text-primary-foreground hover:translate-y-[-2px] hover:text-primary-foreground/80"
          href="#active"
          >туры</a
        >
        <a
          class="transition-all duration-300 text-primary-foreground hover:translate-y-[-2px] hover:text-primary-foreground/80"
          href="#contacts"
          >как добраться</a
        >
      </div>
      <div class="flex items-center gap-4">
        <a
          href="tel:+79991234567"
          class="transition-transform duration-300 text-primary-foreground hover:scale-110 hover:text-primary-foreground/80"
        >
          <Phone class="w-5 h-5" />
        </a>
        <button
          class="rounded-full border border-primary-foreground bg-transparent px-6 py-2 text-sm font-semibold uppercase tracking-wide text-primary-foreground transition-all duration-300 hover:scale-105 hover:bg-primary-foreground hover:text-primary"
        >
          забронировать
        </button>
      </div>
    </div>
  </nav>

  <div class="absolute bottom-0 left-0 right-0 z-10 pb-12 md:pb-16">
    <div class="container mx-auto px-6 md:px-8">
      <div class="grid items-end gap-8 md:grid-cols-2">
        <div
          class="animate-fade-in"
          style="
            animation-delay: 0.3s;
            opacity: 0;
            animation-fill-mode: forwards;
          "
        >
          <p
            class="text-2xl font-light leading-relaxed text-primary-foreground md:text-3xl"
          >
            {{ heroData?.title || 'уютные коттеджи и глэмпинг'}}
          </p>
        </div>

        <div
          class="animate-slide-in-right rounded-2xl border border-primary-foreground/20 bg-primary-foreground/10 p-6 backdrop-blur-md transition-all duration-500 hover:bg-primary-foreground/15 md:p-8"
          style="
            animation-delay: 0.6s;
            opacity: 0;
            animation-fill-mode: forwards;
          "
        >
          <p
            class="text-base leading-relaxed text-primary-foreground md:text-lg"
          >
            {{ heroData?.subtitle || 'Уединённый отдых в хвойном лесу с европейским уровнем комфорта. Квадроциклы, традиционная баня и первозданная природа Пермского края.' }}
          </p>
        </div>
      </div>
    </div>
  </div>
</section>
</template>
