<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch } from "vue";
import { useHead } from "#imports";
import { Menu, Phone, X } from "lucide-vue-next";
import logo from "~/assets/resort/logo.webp";
import nac from "~/assets/resort/nac.webp";

const props = defineProps({
  editMode: {
    type: Boolean,
    default: false,
  },
});

// Компонент сам запрашивает свои данные через composable
const { data: heroData, error: heroError, refresh: refreshHero } = useHero();
const { patch: patchAdminContent, patchForm: patchAdminContentForm } = useAdminContentApi();

// Логируем ошибки, но не прерываем рендеринг
if (heroError.value) {
  console.error("Error loading hero:", heroError.value);
}

// Используем данные из API или fallback
const localHeroPreviewUrl = ref("");

const releaseHeroPreviewUrl = (url) => {
  if (!url || !import.meta.client) return;
  URL.revokeObjectURL(url);
};

const heroImageSrc = computed(() => {
  if (localHeroPreviewUrl.value) return localHeroPreviewUrl.value;

  if (heroData.value?.preview_image_webp_url || heroData.value?.preview_image_url) {
    return heroData.value?.preview_image_webp_url || heroData.value?.preview_image_url;
  }

  if (
    heroData.value?.images &&
    Array.isArray(heroData.value.images) &&
    heroData.value.images.length > 0
  ) {
    return heroData.value.images[0]?.image_webp_url || heroData.value.images[0]?.image_url;
  }
  return "";
});
const heroPlaceholder = computed(() => {
  if (localHeroPreviewUrl.value) return null;

  if (heroData.value?.preview_image_placeholder_url) {
    return heroData.value.preview_image_placeholder_url;
  }

  if (
    heroData.value?.images &&
    Array.isArray(heroData.value.images) &&
    heroData.value.images.length > 0
  ) {
    return heroData.value.images[0]?.image_placeholder_url;
  }
});

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
}));

const scrollY = ref(0);
const parallaxEnabled = ref(false);
const editableTitle = ref("");
const editableSubtitle = ref("");
const editableHeroFile = ref(null);
const editableHeroFileName = ref("");
const isSaving = ref(false);
const saveError = ref("");
const saveSuccess = ref("");
const mobileMenuOpen = ref(false);

watch(
  heroData,
  (value) => {
    editableTitle.value = value?.title || "";
    editableSubtitle.value = value?.subtitle || "";
  },
  { immediate: true }
);

const displayedTitle = computed(() =>
  props.editMode ? editableTitle.value : (heroData.value?.title || "")
);
const displayedSubtitle = computed(() =>
  props.editMode ? editableSubtitle.value : (heroData.value?.subtitle || "")
);

const resetEditableHero = () => {
  editableTitle.value = heroData.value?.title || "";
  editableSubtitle.value = heroData.value?.subtitle || "";
  editableHeroFile.value = null;
  editableHeroFileName.value = "";
  releaseHeroPreviewUrl(localHeroPreviewUrl.value);
  localHeroPreviewUrl.value = "";
};

const hasHeroChanges = computed(() => {
  return (
    editableTitle.value !== (heroData.value?.title || "") ||
    editableSubtitle.value !== (heroData.value?.subtitle || "") ||
    Boolean(editableHeroFile.value)
  );
});

const selectLocalHeroImage = (event) => {
  const target = event?.target;
  const file = target?.files?.[0];
  if (!file || !import.meta.client) return;

  releaseHeroPreviewUrl(localHeroPreviewUrl.value);
  localHeroPreviewUrl.value = URL.createObjectURL(file);
  editableHeroFile.value = file;
  editableHeroFileName.value = file.name;
  target.value = "";
};

const saveHero = async () => {
  if (!hasHeroChanges.value || isSaving.value) return;

  isSaving.value = true;
  saveError.value = "";
  saveSuccess.value = "";

  try {
    if (editableHeroFile.value) {
      const formData = new FormData();
      formData.append("title", editableTitle.value);
      formData.append("subtitle", editableSubtitle.value);
      formData.append("preview_image", editableHeroFile.value);
      await patchAdminContentForm("/auth/edit/hero/active/", formData);
    } else {
      await patchAdminContent("/auth/edit/hero/active/", {
        title: editableTitle.value,
        subtitle: editableSubtitle.value,
      });
    }

    await refreshHero();
    resetEditableHero();
    saveSuccess.value = "Hero секция сохранена";
  } catch (error) {
    saveError.value = error?.data?.detail || "Не удалось сохранить Hero секцию";
  } finally {
    isSaving.value = false;
  }
};

const parallaxStyle = computed(() => {
  if (!parallaxEnabled.value) {
    return {
      transform: "translate3d(0, 0, 0) scale(1.05)",
    };
  }
  const y = scrollY.value * 0.5;
  return {
    transform: `translate3d(0, ${y}px, 0) scale(1.1)`,
    willChange: "transform",
  };
});

/** Один апдейт на кадр: без rAF каждый scroll + Vue-реактивность дают фризы на тяжёлой странице */
let parallaxRafId = null;
const handleScroll = () => {
  if (!parallaxEnabled.value) return;
  if (parallaxRafId != null) return;
  parallaxRafId = requestAnimationFrame(() => {
    parallaxRafId = null;
    scrollY.value = window.scrollY;
  });
};

const closeMobileMenu = () => {
  mobileMenuOpen.value = false;
};

const handleWindowKeydown = (event) => {
  if (event.key === "Escape") {
    closeMobileMenu();
  }
};

watch(mobileMenuOpen, (isOpen) => {
  if (!import.meta.client) return;
  document.body.style.overflow = isOpen ? "hidden" : "";
});

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
  window.addEventListener("keydown", handleWindowKeydown);
});

onBeforeUnmount(() => {
  closeMobileMenu();
  if (import.meta.client) {
    document.body.style.overflow = "";
    window.removeEventListener("keydown", handleWindowKeydown);
    if (parallaxRafId != null) {
      cancelAnimationFrame(parallaxRafId);
      parallaxRafId = null;
    }
  }
  releaseHeroPreviewUrl(localHeroPreviewUrl.value);
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
      <img
        v-if="localHeroPreviewUrl"
        :src="heroImageSrc"
        alt="Коттеджи базы отдыха Строгановские Просторы зимой"
        class="h-full w-full object-cover [backface-visibility:hidden]"
        :style="parallaxStyle"
      />
      <NuxtImg
        v-else
        :src="heroImageSrc"
        alt="Коттеджи базы отдыха Строгановские Просторы зимой"
        :width="1410"
        :height="940"
        :quality="80"
        class="h-full w-full object-cover [backface-visibility:hidden]"
        :style="parallaxStyle"
        loading="eager"
        decoding="async"
        fetchpriority="high"
        sizes="1410px"
        :preload="true"
        format="webp"
        :placeholder="heroPlaceholder"
      />
      <div
        class="absolute inset-0 bg-gradient-to-b from-primary/70 via-primary/50 to-primary/70"
      />
    </div>

    <nav class="animate-fade-in absolute left-0 right-0 top-0 z-20 p-4 md:p-8">
      <div class="container mx-auto flex items-center justify-between">
        <div class="flex items-center gap-4 md:gap-8">
          <div class="flex items-center">
            <NuxtImg
              :src="logo"
              alt="Строгановские Просторы"
              class="h-10 transition-transform duration-300 hover:scale-105 md:h-16"
              fetchpriority="high"
              decoding="async"
              sizes="140px"
              :preload="true"
            />
            <div class="mx-[0.6rem] h-16 w-px bg-white md:mx-[0.8rem] md:h-24"></div>
            <NuxtImg
              :src="nac"
              fetchpriority="high"
              alt="национальные проекты"
              class="h-16 md:h-24"
              decoding="async"
              sizes="150px"
              :preload="true"
            />
          </div>
          <div class="hidden items-center gap-8 md:flex">
            <a
              class="transition-all duration-300 text-primary-foreground hover:translate-y-[-2px] hover:text-primary-foreground/80"
              href="#lodge"
              >о клубе</a
            >
            <a
              class="transition-all duration-300 text-primary-foreground hover:translate-y-[-2px] hover:text-primary-foreground/80"
              href="/lodge"
              >дома</a
            >
            <a
              class="transition-all duration-300 text-primary-foreground hover:translate-y-[-2px] hover:text-primary-foreground/80"
              href="#active"
              >услуги</a
            >
            <a
              class="transition-all duration-300 text-primary-foreground hover:translate-y-[-2px] hover:text-primary-foreground/80"
              href="/event-calculator"
              >мероприятия</a
            >
            <a
              class="transition-all duration-300 text-primary-foreground hover:translate-y-[-2px] hover:text-primary-foreground/80"
              href="#contacts"
              >как добраться</a
            >
          </div>
        </div>
        <div class="hidden items-center gap-4 md:flex">
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
        <div class="flex items-center gap-2 md:hidden">
          <button
            class="flex h-10 w-10 items-center justify-center rounded-full border border-primary-foreground/70 bg-black/20 text-primary-foreground backdrop-blur-sm transition-colors hover:bg-primary-foreground/15"
            :aria-label="mobileMenuOpen ? 'Закрыть меню' : 'Открыть меню'"
            :aria-expanded="mobileMenuOpen"
            @click="mobileMenuOpen = !mobileMenuOpen"
          >
            <X v-if="mobileMenuOpen" class="h-5 w-5" />
            <Menu v-else class="h-5 w-5" />
          </button>
        </div>
      </div>
      <div
        v-if="mobileMenuOpen"
        class="mt-3 ml-auto w-full max-w-[360px] rounded-2xl border border-white/20 bg-primary/85 p-4 shadow-xl backdrop-blur-md md:hidden"
      >
        <div class="flex flex-col gap-3 text-primary-foreground">
          <a
            class="transition-all duration-300 text-primary-foreground hover:translate-y-[-2px] hover:text-primary-foreground/80"
            href="#lodge"
            @click="closeMobileMenu"
            >о клубе</a
          >
          <a
            class="transition-all duration-300 text-primary-foreground hover:translate-y-[-2px] hover:text-primary-foreground/80"
            href="/lodge"
            @click="closeMobileMenu"
            >дома</a
          >
          <a
            class="transition-all duration-300 text-primary-foreground hover:translate-y-[-2px] hover:text-primary-foreground/80"
            href="#active"
            @click="closeMobileMenu"
            >услуги</a
          >
          <a
            class="transition-all duration-300 text-primary-foreground hover:translate-y-[-2px] hover:text-primary-foreground/80"
            href="/event-calculator"
            @click="closeMobileMenu"
            >мероприятия</a
          >
          <a
            class="transition-all duration-300 text-primary-foreground hover:translate-y-[-2px] hover:text-primary-foreground/80"
            href="#contacts"
            @click="closeMobileMenu"
            >как добраться</a
          >
          <a
            href="tel:+79991234567"
            class="mt-2 inline-flex w-fit items-center gap-2 transition-transform duration-300 text-primary-foreground hover:scale-105 hover:text-primary-foreground/80"
            @click="closeMobileMenu"
          >
            <Phone class="w-5 h-5" />
            <span>+7 (999) 123-45-67</span>
          </a>
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
              {{ displayedTitle }}
            </p>
            <div v-if="editMode" class="mt-3">
              <textarea
                v-model="editableTitle"
                rows="3"
                class="w-full rounded-xl border border-white/30 bg-black/35 p-3 text-sm text-white outline-none ring-0 placeholder:text-white/70"
                placeholder="Заголовок первого экрана"
              />
            </div>
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
              {{ displayedSubtitle }}
            </p>
            <div v-if="editMode" class="mt-3 space-y-2">
              <label
                class="flex cursor-pointer items-center justify-center rounded-lg border border-white/30 bg-black/35 px-3 py-2 text-xs font-semibold text-white transition-colors hover:bg-white/10"
              >
                Выбрать фото для hero
                <input
                  type="file"
                  accept="image/*"
                  class="hidden"
                  @change="selectLocalHeroImage"
                />
              </label>
              <p v-if="editableHeroFileName" class="text-xs text-white/80">
                Локальный файл: {{ editableHeroFileName }}
              </p>
              <textarea
                v-model="editableSubtitle"
                rows="4"
                class="w-full rounded-xl border border-white/30 bg-black/35 p-3 text-sm text-white outline-none ring-0 placeholder:text-white/70"
                placeholder="Подзаголовок первого экрана"
              />
              <div class="flex flex-wrap items-center gap-2">
                <button
                  class="rounded-lg border border-white/30 px-3 py-1 text-xs font-semibold text-white transition-colors hover:bg-white/10"
                  @click="resetEditableHero"
                >
                  Сбросить превью
                </button>
                <button
                  class="rounded-lg px-3 py-1 text-xs font-semibold transition-colors"
                  :class="
                    hasHeroChanges
                      ? 'bg-white text-primary hover:bg-white/90'
                      : 'bg-white/30 text-white/70'
                  "
                  :disabled="!hasHeroChanges || isSaving"
                  @click="saveHero"
                >
                  {{ isSaving ? "Сохранение..." : "Сохранить Hero" }}
                </button>
                <span v-if="saveSuccess" class="text-xs text-green-200">{{ saveSuccess }}</span>
                <span v-if="saveError" class="text-xs text-red-200">{{ saveError }}</span>
              </div>
            </div>
          </div>
        </div>
        <div class="mt-6 flex justify-center md:hidden">
          <button
            class="rounded-full border border-primary-foreground bg-primary-foreground/10 px-8 py-3 text-sm font-semibold uppercase tracking-wide text-primary-foreground backdrop-blur-sm transition-all duration-300 hover:bg-primary-foreground hover:text-primary"
          >
            забронировать
          </button>
        </div>
      </div>
    </div>
  </section>
</template>
