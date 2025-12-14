export const useNews = (options = {}) => {
  const config = useRuntimeConfig()
  const apiBase = config.public.apiBase

  // Загрузка списка новостей
  const { data: news, error: newsError } = useFetch(`${apiBase}/news/`, {
    key: 'news',
    default: () => [],
    server: true,
    ...options,
  })

  // Обрабатываем ответ от Django REST Framework (может быть объект с пагинацией)
  const newsList = computed(() => {
    if (!news.value) return []
    if (typeof news.value === 'object' && 'results' in news.value) {
      return news.value.results
    }
    if (Array.isArray(news.value)) {
      return news.value
    }
    return []
  })

  return {
    news,
    newsList,
    newsError,
  }
}

export const useNewsItem = (id, options = {}) => {
  const config = useRuntimeConfig()
  const apiBase = config.public.apiBase

  // Загрузка конкретной новости
  const { data: newsItem, error: newsItemError } = useFetch(`${apiBase}/news/${id}/`, {
    key: `news-${id}`,
    default: () => null,
    server: true,
    ...options,
  })

  return {
    newsItem,
    newsItemError,
  }
}

