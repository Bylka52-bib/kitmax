from django_filters import rest_framework as filters
from .models import Book, Lead


class BookFilter(filters.FilterSet):
    """Advanced filter for Book model"""
    # Фильтр для цены (диапазон)
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')

    # Фильтр для страниц
    min_pages = filters.NumberFilter(field_name="pages", lookup_expr='gte')
    max_pages = filters.NumberFilter(field_name="pages", lookup_expr='lte')

    # Поиск по названию без учета регистра
    title = filters.CharFilter(lookup_expr='icontains')

    # Фильтр по имени автора
    author_name = filters.CharFilter(field_name="author__name", lookup_expr='icontains')

    # Фильтр по дате
    published_after = filters.DateFilter(field_name="published_date", lookup_expr='gte')
    published_before = filters.DateFilter(field_name="published_date", lookup_expr='lte')

    class Meta:
        model = Book
        fields = ['is_active', 'author', 'min_price', 'max_price', 'min_pages',
                  'max_pages', 'title', 'author_name']


class LeadFilter(filters.FilterSet):
    """Filter for Lead model"""
    created_after = filters.DateTimeFilter(field_name="created_at", lookup_expr='gte')
    created_before = filters.DateTimeFilter(field_name="created_at", lookup_expr='lte')

    class Meta:
        model = Lead
        fields = ['user_type', 'status']