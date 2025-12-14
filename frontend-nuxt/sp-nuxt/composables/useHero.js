export const useHero = (options = {}) => {
  const config = useRuntimeConfig()
  const apiBase = config.public.apiBase

  // Используем useFetch для SSR поддержки
  // useFetch работает синхронно в контексте setup (Nuxt 3 автоматически обрабатывает await)
  const { data, error } = useFetch(`${apiBase}/hero/`, {
    key: 'hero',
    default: () => ({ images: [] }), // Безопасное значение по умолчанию с пустым массивом images
    server: true, // Выполняется на сервере для SSR
    ...options,
  })

  return {
    data,
    error,
  }
}

