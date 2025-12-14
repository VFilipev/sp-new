<script setup>
import { storeToRefs } from 'pinia'
import { RouterLink } from 'vue-router'
import { useCounterStore } from '../stores/counter'

const counter = useCounterStore()
const { count, doubleCount } = storeToRefs(counter)
</script>

<template>
  <section class="space-y-6">
    <div class="space-y-2">
      <p class="text-sm font-medium text-blue-700">Pinia</p>
      <h1 class="text-3xl font-bold text-slate-900">Счётчик состояния</h1>
      <p class="text-slate-600">
        Простая демонстрация глобального состояния через Pinia. Значения доступны из любого места
        приложения.
      </p>
    </div>

    <div class="card space-y-4">
      <div class="flex flex-wrap items-end justify-between gap-4">
        <div class="flex items-center gap-4">
          <span class="text-5xl font-bold tracking-tight">{{ count }}</span>
          <div class="text-sm text-slate-500">
            <p>Удвоенное значение:</p>
            <p class="text-lg font-semibold text-slate-800">{{ doubleCount }}</p>
          </div>
        </div>
      </div>

      <div class="flex flex-wrap gap-3">
        <button type="button" class="btn-primary" @click="counter.increment()">+1</button>
        <button type="button" class="btn-secondary" @click="counter.decrement()">-1</button>
        <button type="button" class="btn-secondary" @click="counter.reset()">Сброс</button>
      </div>
    </div>

    <RouterLink class="text-sm font-semibold text-blue-700 hover:text-blue-800" to="/">
      ← Вернуться на главную
    </RouterLink>
  </section>
</template>




