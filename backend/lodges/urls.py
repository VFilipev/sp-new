from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LodgeTypeViewSet, LodgeViewSet

router = DefaultRouter()
router.register(r'types', LodgeTypeViewSet, basename='lodgetype')
router.register(r'', LodgeViewSet, basename='lodge')

urlpatterns = [
    path('', include(router.urls)),
]

