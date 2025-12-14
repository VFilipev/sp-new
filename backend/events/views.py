from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import EventType
from .serializers import EventTypeSerializer


class EventTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для типов мероприятий"""
    queryset = EventType.objects.filter(is_active=True)
    serializer_class = EventTypeSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['is_active']
    ordering_fields = ['order', 'title']
    ordering = ['order', 'title']

    def get_serializer_context(self):
        """Передаем request в контекст сериализатора"""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
