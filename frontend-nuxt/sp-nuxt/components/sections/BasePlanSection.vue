<script setup>
import basePlanImage from '~/assets/resort/base-plan.webp'
</script>

<template>
  <section class="bg-background py-20">
    <div class="container mx-auto px-6 md:px-8">
      <div class="animate-fade-in mb-12 text-center">
        <h2 class="mb-4 text-4xl font-serif text-primary md:text-5xl">План базы отдыха</h2>
        <p class="mx-auto max-w-2xl text-lg text-muted-foreground">
          Ознакомьтесь с расположением всех объектов и инфраструктуры на территории "Строгановских Просторов"
        </p>
      </div>

      <div class="animate-fade-in w-[70%] max-w-6xl mx-auto overflow-hidden rounded-2xl border border-border/50 bg-card/80 shadow-2xl backdrop-blur">
        <div class="relative">
          <img
            :src="basePlanImage"
            alt="План базы отдыха Строгановские Просторы"
            class="w-full h-auto"
          />
          <div class="pointer-events-none absolute inset-0 bg-gradient-to-t from-black/10 to-transparent" />
        </div>
      </div>

      <div class="animate-fade-in mt-8 text-center" style="animation-delay: 200ms">
        <p class="mx-auto max-w-3xl text-muted-foreground">
          На территории базы расположены домики для проживания, развлекательные и спортивные объекты, зоны отдыха у воды,
          бани и многое другое для вашего комфортного отдыха
        </p>
      </div>
    </div>
  </section>
</template>

