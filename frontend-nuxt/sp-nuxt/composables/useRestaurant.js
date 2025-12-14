export const useRestaurant = () => {
  const { fetch } = useApi()

  const getRestaurant = async () => {
    return await fetch('/restaurant/', {
      key: 'restaurant',
      default: () => null,
    })
  }

  const getRestaurantImages = async () => {
    return await fetch('/restaurant/images/', {
      key: 'restaurant-images',
      default: () => [],
    })
  }

  const getMealTypes = async () => {
    return await fetch('/restaurant/meal-types/', {
      key: 'meal-types',
      default: () => [],
    })
  }

  const getBenefits = async () => {
    return await fetch('/restaurant/benefits/', {
      key: 'restaurant-benefits',
      default: () => [],
    })
  }

  return {
    getRestaurant,
    getRestaurantImages,
    getMealTypes,
    getBenefits,
  }
}

