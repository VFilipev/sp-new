from rest_framework import viewsets, generics, filters
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from django.contrib.sitemaps import Sitemap
from django.contrib.sitemaps.views import sitemap
from django_filters.rest_framework import DjangoFilterBackend
from .models import Statistic, GalleryImage, HeroSection, SiteSettings
from .serializers import (
    StatisticSerializer, GalleryImageSerializer,
    HeroSectionSerializer, SiteSettingsSerializer
)
from .sitemaps import (
    LodgeTypeSitemap, LodgeSitemap, NewsSitemap,
    ActivitySitemap, EventTypeSitemap
)


class StatisticViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для статистики"""
    queryset = Statistic.objects.filter(is_active=True)
    serializer_class = StatisticSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['is_active']
    ordering_fields = ['order']
    ordering = ['order', 'id']

    def get_serializer_context(self):
        """Передаем request в контекст сериализатора"""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class GalleryImageViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для изображений галереи"""
    queryset = GalleryImage.objects.filter(is_active=True)
    serializer_class = GalleryImageSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['position', 'is_active']
    ordering_fields = ['order']
    ordering = ['position', 'order', 'id']

    def get_serializer_context(self):
        """Передаем request в контекст сериализатора"""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class HeroSectionView(generics.RetrieveAPIView):
    """View для Hero секции (активная запись)"""
    queryset = HeroSection.objects.filter(is_active=True)
    serializer_class = HeroSectionSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        """Возвращает активную Hero секцию"""
        return HeroSection.get_active_hero()

    def get_serializer_context(self):
        """Передаем request в контекст сериализатора"""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class SiteSettingsView(generics.RetrieveAPIView):
    """View для настроек сайта (Singleton)"""
    queryset = SiteSettings.objects.all()
    serializer_class = SiteSettingsSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        """Возвращает единственную запись настроек сайта"""
        return SiteSettings.objects.get()

    def get_serializer_context(self):
        """Передаем request в контекст сериализатора"""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


# Sitemap
sitemaps = {
    'lodgetypes': LodgeTypeSitemap,
    'lodges': LodgeSitemap,
    'news': NewsSitemap,
    'activities': ActivitySitemap,
    'eventtypes': EventTypeSitemap,
}

sitemap_view = lambda request: sitemap(request, sitemaps)


# Robots.txt
@api_view(['GET'])
def robots_txt(request):
    """Генерирует robots.txt"""
    content = """User-agent: *
Allow: /
Disallow: /admin/
Disallow: /api/

Sitemap: http://localhost:8000/api/sitemap.xml
"""
    return HttpResponse(content, content_type='text/plain')
