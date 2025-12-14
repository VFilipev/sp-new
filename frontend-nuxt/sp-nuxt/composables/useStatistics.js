export const useStatistics = (options = {}) => {
  const config = useRuntimeConfig()
  const apiBase = config.public.apiBase

  // Используем useFetch для SSR поддержки
  // useFetch работает синхронно в контексте setup (Nuxt 3 автоматически обрабатывает await)
  const { data, error } = useFetch(`${apiBase}/statistics/`, {
    key: 'statistics',
    default: () => [],
    server: true, // Выполняется на сервере для SSR
    ...options,
  })

  // Обрабатываем ответ от Django REST Framework (может быть объект с пагинацией)
  const statistics = computed(() => {
    if (!data.value) return []
    // Если это объект с пагинацией Django REST Framework, извлекаем results
    if (typeof data.value === 'object' && 'results' in data.value) {
      return data.value.results
    }
    // Если это уже массив, возвращаем как есть
    if (Array.isArray(data.value)) {
      return data.value
    }
    return []
  })

  return {
    data,
    statistics,
    error,
  }
}

