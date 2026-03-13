from rest_framework import viewsets, generics, filters
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.http import HttpResponse
from django.middleware.csrf import get_token
from django.contrib.sitemaps import Sitemap
from django.contrib.sitemaps.views import sitemap
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction
from .models import Statistic, GalleryImage, HeroSection, SiteSettings
from .serializers import (
    StatisticSerializer, GalleryImageSerializer,
    HeroSectionSerializer, SiteSettingsSerializer,
    HeroSectionPatchSerializer, StatisticPatchSerializer,
    GalleryImageUploadSerializer, GalleryLayoutApplySerializer
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


class IsSiteEditor(BasePermission):
    """Доступ только для редакторов сайта (staff/superuser)."""
    def has_permission(self, request, view):
        user = request.user
        return bool(
            user and user.is_authenticated and (user.is_staff or user.is_superuser)
        )


class AdminStatusView(APIView):
    """Проверка прав администратора для frontend edit-mode."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        can_edit = bool(user.is_staff or user.is_superuser)
        return Response({
            'is_authenticated': True,
            'is_staff': bool(user.is_staff),
            'is_superuser': bool(user.is_superuser),
            'can_edit': can_edit,
            'username': user.get_username(),
        })


class CsrfTokenView(APIView):
    """Выдает CSRF токен и устанавливает CSRF cookie."""
    permission_classes = [AllowAny]

    def get(self, request):
        token = get_token(request)
        return Response({'csrfToken': token})


class HeroSectionPatchView(APIView):
    """PATCH активной Hero секции."""
    permission_classes = [IsSiteEditor]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def patch(self, request):
        hero = HeroSection.get_active_hero()
        if not hero:
            return Response(
                {'detail': 'Активная Hero секция не найдена.'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = HeroSectionPatchSerializer(
            hero, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response_serializer = HeroSectionSerializer(
            hero, context={'request': request}
        )
        return Response(response_serializer.data)


class StatisticPatchView(generics.UpdateAPIView):
    """PATCH карточки статистики по id."""
    queryset = Statistic.objects.all()
    serializer_class = StatisticPatchSerializer
    permission_classes = [IsSiteEditor]
    http_method_names = ['patch']


class GalleryImageAdminListView(APIView):
    """GET список всех изображений галереи (включая неактивные)."""
    permission_classes = [IsSiteEditor]

    def get(self, request):
        queryset = GalleryImage.objects.all().order_by('position', 'column', 'order', 'id')
        serializer = GalleryImageSerializer(
            queryset, many=True, context={'request': request}
        )
        return Response(serializer.data)


class GalleryImageUploadView(APIView):
    """POST загрузка изображения галереи для edit-mode."""
    permission_classes = [IsSiteEditor]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = GalleryImageUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        response_serializer = GalleryImageSerializer(
            instance, context={'request': request}
        )
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class GalleryLayoutApplyView(APIView):
    """POST применение финальной раскладки галереи."""
    permission_classes = [IsSiteEditor]
    parser_classes = [JSONParser]

    def post(self, request):
        serializer = GalleryLayoutApplySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        items = serializer.validated_data['items']

        target_ids = {item['target_id'] for item in items}
        source_ids = {item.get('source_image_id') or item['target_id'] for item in items}
        required_ids = target_ids | source_ids

        with transaction.atomic():
            rows = GalleryImage.objects.select_for_update().filter(id__in=required_ids)
            rows_by_id = {row.id: row for row in rows}

            missing_ids = sorted(required_ids - set(rows_by_id.keys()))
            if missing_ids:
                return Response(
                    {'detail': f'Не найдены GalleryImage id: {missing_ids}'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Сначала деактивируем слоты, которые будут заменены другими source.
            replaced_targets = []
            for item in items:
                target = rows_by_id[item['target_id']]
                source_id = item.get('source_image_id') or item['target_id']
                if source_id != target.id and target.is_active:
                    target.is_active = False
                    replaced_targets.append(target)

            if replaced_targets:
                GalleryImage.objects.bulk_update(replaced_targets, ['is_active'])

            # Затем применяем итоговую раскладку к source-изображениям.
            updated_sources = []
            source_updates = {}
            for item in items:
                source_id = item.get('source_image_id') or item['target_id']
                source = rows_by_id[source_id]
                source.position = item['position']
                source.column = item.get('column')
                source.order = item['order']
                source.is_active = item.get('is_active', True)
                if 'alt_text' in item:
                    source.alt_text = item.get('alt_text')
                source_updates[source.id] = source

            updated_sources.extend(source_updates.values())
            if updated_sources:
                GalleryImage.objects.bulk_update(
                    updated_sources,
                    ['position', 'column', 'order', 'is_active', 'alt_text']
                )

        updated_queryset = GalleryImage.objects.filter(
            is_active=True, position='main'
        ).order_by('position', 'column', 'order', 'id')
        response_serializer = GalleryImageSerializer(
            updated_queryset, many=True, context={'request': request}
        )
        return Response({'items': response_serializer.data}, status=status.HTTP_200_OK)


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
    # Динамически формируем URL sitemap на основе текущего запроса
    scheme = request.scheme  # http или https
    host = request.get_host()  # host:port
    sitemap_url = f"{scheme}://{host}/api/sitemap.xml"

    content = f"""User-agent: *
Allow: /
Disallow: /admin/
Disallow: /api/

Sitemap: {sitemap_url}
"""
    return HttpResponse(content, content_type='text/plain')
