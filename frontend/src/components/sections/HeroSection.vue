<script setup>
import { onBeforeUnmount, onMounted, ref } from "vue";
import heroImage from "@/assets/resort/hero-cottages.jpg";
import { Phone } from "lucide-vue-next";
import logo from "@/assets/resort/logo.png";

const scrollY = ref(0);

const handleScroll = () => {
  scrollY.value = window.scrollY;
};

onMounted(() => {
  window.addEventListener("scroll", handleScroll, { passive: true });
});

onBeforeUnmount(() => {
  window.removeEventListener("scroll", handleScroll);
});
</script>

<template>
  <section
    class="relative flex min-h-screen items-center justify-center overflow-hidden"
  >
    <div class="absolute inset-0 z-0">
      <img
        :src="heroImage"
        alt="Коттеджи базы отдыха Строгановские Просторы зимой"
        class="h-full w-full object-cover transition-transform duration-100 ease-out"
        :style="{ transform: `translateY(${scrollY * 0.5}px) scale(1.1)` }"
      />
      <div
        class="absolute inset-0 bg-gradient-to-b from-primary/70 via-primary/50 to-primary/70"
      />
    </div>

    <nav class="animate-fade-in absolute left-0 right-0 top-0 z-20 p-6 md:p-8">
      <div class="container mx-auto flex items-center justify-between">
        <div class="flex items-center gap-8">
          <div class="flex items-center">
            <img
              :src="logo"
              alt="Строгановские Просторы"
              class="h-12 transition-transform duration-300 hover:scale-105 md:h-16"
            />
            <div class="h-24 w-px bg-white mx-[0.8rem]"></div>
            <img
              src="@/assets/resort/nac.png"
              alt="национальные проекты"
              class="h-24"
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
              уютные коттеджи и глэмпинг
              <br />
              на берегу камского моря
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
              Уединённый отдых в хвойном лесу с европейским уровнем комфорта.
              Квадроциклы, традиционная баня и первозданная природа Пермского
              края.
            </p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
