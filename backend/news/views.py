from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from .models import News
from .serializers import NewsListSerializer, NewsDetailSerializer


class NewsViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для новостей"""
    queryset = News.objects.filter(is_published=True, published_at__lte=timezone.now())
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_published']
    search_fields = ['title', 'content', 'short_description']
    ordering_fields = ['published_at', 'created_at']
    ordering = ['-published_at', '-created_at']

    def get_serializer_class(self):
        """Используем разные сериализаторы для списка и детальной страницы"""
        if self.action == 'retrieve':
            return NewsDetailSerializer
        return NewsListSerializer

    def get_serializer_context(self):
        """Передаем request в контекст сериализатора"""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
