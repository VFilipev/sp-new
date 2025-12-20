export const useGallery = (options = {}) => {
  const config = useRuntimeConfig()
  const apiBase = config.public.apiBase

  // Формируем URL с query параметрами
  const position = options.position || null
  const ordering = options.ordering || 'order'
  let url = `${apiBase}/gallery/`

  // Добавляем query параметры
  const queryParams = []
  if (position) {
    queryParams.push(`position=${position}`)
  }
  if (ordering) {
    queryParams.push(`ordering=${ordering}`)
  }
  if (queryParams.length > 0) {
    url += `?${queryParams.join('&')}`
  }

  // Используем useFetch для SSR поддержки
  const { data, error } = useFetch(url, {
    key: `gallery-${position || 'all'}-${ordering}`,
    default: () => [],
    server: true, // Выполняется на сервере для SSR
  })

  // Обрабатываем ответ от Django REST Framework (может быть объект с пагинацией)
  const galleryImages = computed(() => {
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

  // Фильтруем изображения по позиции
  const getImagesByPosition = (position) => {
    return computed(() => {
      return galleryImages.value.filter(img => img.position === position)
    })
  }

  // Фильтруем изображения по колонке
  const getImagesByColumn = (column) => {
    return computed(() => {
      return galleryImages.value.filter(img => img.column === column && img.position === 'main')
    })
  }

  return {
    data,
    galleryImages,
    error,
    getImagesByPosition,
    getImagesByColumn,
  }
}

