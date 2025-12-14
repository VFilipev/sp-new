from django_filters import rest_framework as filters
from .models import Lodge


class LodgeFilter(filters.FilterSet):
    """Фильтр для размещений"""
    price_from_min = filters.NumberFilter(field_name='price_from', lookup_expr='gte')
    price_from_max = filters.NumberFilter(field_name='price_from', lookup_expr='lte')
    capacity_min = filters.NumberFilter(field_name='capacity', lookup_expr='gte')
    capacity_max = filters.NumberFilter(field_name='capacity', lookup_expr='lte')

    class Meta:
        model = Lodge
        fields = ['lodge_type', 'is_active', 'price_from_min', 'price_from_max', 'capacity_min', 'capacity_max']

