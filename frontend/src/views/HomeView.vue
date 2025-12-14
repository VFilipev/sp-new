<script setup>
import LodgeSection from '@/components/sections/LodgeSection.vue'
import ActiveRestSection from '@/components/sections/ActiveRestSection.vue'
import EventsSection from '@/components/sections/EventsSection.vue'
import FooterSection from '@/components/sections/FooterSection.vue'
import GalleryStatsSection from '@/components/sections/GalleryStatsSection.vue'
import HeroSection from '@/components/sections/HeroSection.vue'
import NewsSection from '@/components/sections/NewsSection.vue'
import PeacefulRestSection from '@/components/sections/PeacefulRestSection.vue'
import RestaurantSection from '@/components/sections/RestaurantSection.vue'
</script>

<template>
  <div class="min-h-screen bg-background text-foreground">
    <HeroSection />
    <GalleryStatsSection />
    <LodgeSection />
    <PeacefulRestSection />
    <ActiveRestSection />
    <EventsSection />
    <RestaurantSection />
    <NewsSection />
    <FooterSection />
  </div>
</template>
