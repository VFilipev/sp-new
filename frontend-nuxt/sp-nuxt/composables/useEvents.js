export const useEvents = (options = {}) => {
  const config = useRuntimeConfig()
  const apiBase = config.public.apiBase

  // Загрузка типов мероприятий
  const { data: eventTypes, error: eventTypesError } = useFetch(`${apiBase}/events/types/`, {
    key: 'event-types',
    default: () => [],
    server: true,
    ...options,
  })

  return {
    eventTypes,
    eventTypesError,
  }
}

export const useEventType = (id, options = {}) => {
  const config = useRuntimeConfig()
  const apiBase = config.public.apiBase

  // Загрузка конкретного типа мероприятия
  const { data: eventType, error: eventTypeError } = useFetch(`${apiBase}/events/types/${id}/`, {
    key: `event-type-${id}`,
    default: () => null,
    server: true,
    ...options,
  })

  return {
    eventType,
    eventTypeError,
  }
}

