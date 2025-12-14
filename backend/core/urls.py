from django.urls import path, include
from .views import (
    StatisticViewSet, GalleryImageViewSet,
    HeroSectionView, SiteSettingsView,
    sitemap_view, robots_txt
)
from .api_views import api_root
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'statistics', StatisticViewSet, basename='statistic')
router.register(r'gallery', GalleryImageViewSet, basename='galleryimage')

urlpatterns = [
    path('', api_root, name='api-root'),
    path('hero/', HeroSectionView.as_view(), name='hero'),
    path('site-settings/', SiteSettingsView.as_view(), name='site-settings'),
    path('sitemap.xml', sitemap_view, name='sitemap'),
    path('robots.txt', robots_txt, name='robots'),
    path('', include(router.urls)),
]

