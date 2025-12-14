export const useApi = () => {
  const config = useRuntimeConfig()
  const baseURL = config.public.apiBase

  // Используем $fetch для простых запросов (без реактивности)
  const fetch = async (endpoint, options = {}) => {
    try {
      const response = await $fetch(`${baseURL}${endpoint}`, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
      })
      return response
    } catch (error) {
      console.error(`API Error [${endpoint}]:`, error)
      throw createError({
        statusCode: error.statusCode || 500,
        message: error.message || 'Ошибка при загрузке данных',
      })
    }
  }

  return { fetch }
}

