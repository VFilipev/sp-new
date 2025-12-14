from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventTypeViewSet

router = DefaultRouter()
router.register(r'', EventTypeViewSet, basename='eventtype')

urlpatterns = [
    path('', include(router.urls)),
]

