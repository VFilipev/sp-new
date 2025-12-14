export const useGallery = () => {
  const { fetch } = useApi()

  const getGalleryImages = async (position) => {
    const endpoint = position ? `/gallery/?position=${position}` : '/gallery/'
    return await fetch(endpoint, {
      key: `gallery-${position || 'all'}`,
      default: () => [],
    })
  }

  return {
    getGalleryImages,
  }
}

