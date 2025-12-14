from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import LodgeType, Lodge
from .serializers import LodgeTypeSerializer, LodgeSerializer
from .filters import LodgeFilter


class LodgeTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для типов размещения"""
    queryset = LodgeType.objects.filter(is_active=True).prefetch_related('lodges')
    serializer_class = LodgeTypeSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['is_active']
    ordering_fields = ['order', 'name']
    ordering = ['order', 'name']

    def get_serializer_context(self):
        """Передаем request в контекст сериализатора"""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class LodgeViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для размещений"""
    queryset = Lodge.objects.filter(is_active=True).select_related('lodge_type').prefetch_related('images')
    serializer_class = LodgeSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = LodgeFilter
    search_fields = ['name', 'description', 'short_description']
    ordering_fields = ['order', 'name', 'price_from', 'capacity']
    ordering = ['order', 'name']

    def get_serializer_context(self):
        """Передаем request в контекст сериализатора"""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
