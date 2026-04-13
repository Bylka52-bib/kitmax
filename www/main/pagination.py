from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    """Custom pagination class with configurable page size"""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class SmallResultsSetPagination(PageNumberPagination):
    """Small pagination for compact views"""
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 20


class LargeResultsSetPagination(PageNumberPagination):
    """Large pagination for data-heavy views"""
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 200