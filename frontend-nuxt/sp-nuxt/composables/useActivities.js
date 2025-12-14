export const useActivities = () => {
  const { fetch } = useApi()

  const getActivities = async (category) => {
    const endpoint = category ? `/activities/?category=${category}` : '/activities/'
    return await fetch(endpoint, {
      key: `activities-${category || 'all'}`,
      default: () => [],
    })
  }

  const getActivity = async (id) => {
    return await fetch(`/activities/${id}/`, {
      key: `activity-${id}`,
      default: () => null,
    })
  }

  return {
    getActivities,
    getActivity,
  }
}

