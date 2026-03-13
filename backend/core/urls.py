from django.urls import path, include
from .views import (
    StatisticViewSet, GalleryImageViewSet,
    HeroSectionView, SiteSettingsView, AdminStatusView,
    CsrfTokenView, HeroSectionPatchView, StatisticPatchView,
    GalleryImageAdminListView, GalleryImageUploadView, GalleryLayoutApplyView,
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
    path('auth/admin-status/', AdminStatusView.as_view(), name='admin-status'),
    path('auth/csrf/', CsrfTokenView.as_view(), name='csrf-token'),
    path('auth/edit/hero/active/', HeroSectionPatchView.as_view(), name='hero-edit-active'),
    path('auth/edit/statistics/<int:pk>/', StatisticPatchView.as_view(), name='statistic-edit'),
    path('auth/edit/gallery/all/', GalleryImageAdminListView.as_view(), name='gallery-admin-all'),
    path('auth/edit/gallery/upload/', GalleryImageUploadView.as_view(), name='gallery-upload'),
    path('auth/edit/gallery/apply/', GalleryLayoutApplyView.as_view(), name='gallery-apply'),
    path('sitemap.xml', sitemap_view, name='sitemap'),
    path('robots.txt', robots_txt, name='robots'),
    path('', include(router.urls)),
]

