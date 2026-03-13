export const useLodges = (type = null, options = {}) => {
  const config = useRuntimeConfig()
  const apiBase = config.public.apiBase

  // Загрузка списка домиков
  const endpoint = type ? `${apiBase}/lodges/?type=${type}` : `${apiBase}/lodges/`
  const { data: lodges, error: lodgesError } = useFetch(endpoint, {
    key: `lodges-${type || 'all'}`,
    default: () => [],
    server: true,
    ...options,
  })

  return {
    lodges,
    lodgesError,
  }
}

export const useLodge = (id, options = {}) => {
  const config = useRuntimeConfig()
  const apiBase = config.public.apiBase

  // Загрузка конкретного домика
  const { data: lodge, error: lodgeError } = useFetch(`${apiBase}/lodges/${id}/`, {
    key: `lodge-${id}`,
    default: () => null,
    server: true,
    ...options,
  })

  return {
    lodge,
    lodgeError,
  }
}

export const useLodgeTypes = (options = {}) => {
  const config = useRuntimeConfig()
  const apiBase = config.public.apiBase

  // Загрузка типов домиков
  const { data: types, error: typesError } = useFetch(`${apiBase}/lodges/types/`, {
    key: 'lodge-types',
    default: () => [],
    server: true,
    ...options,
  })

  // Обрабатываем ответ от Django REST Framework (может быть объект с пагинацией)
  const typesResults = computed(() => {
    if (!types.value) return []
    // Если это объект с пагинацией Django REST Framework, извлекаем results
    if (typeof types.value === 'object' && 'results' in types.value) {
      return types.value.results
    }
    // Если это уже массив, возвращаем как есть
    if (Array.isArray(types.value)) {
      return types.value
    }
    return []
  })

  return {
    types: typesResults,
    typesError,
  }
}

