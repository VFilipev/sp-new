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

  return {
    types,
    typesError,
  }
}

