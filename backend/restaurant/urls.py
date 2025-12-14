from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RestaurantView, RestaurantImageViewSet,
    MealTypeViewSet, RestaurantBenefitViewSet
)

router = DefaultRouter()
router.register(r'images', RestaurantImageViewSet, basename='restaurantimage')
router.register(r'meal-types', MealTypeViewSet, basename='mealtype')
router.register(r'benefits', RestaurantBenefitViewSet, basename='restaurantbenefit')

urlpatterns = [
    path('', RestaurantView.as_view(), name='restaurant'),
    path('', include(router.urls)),
]

