"""
API filters
"""
from rest_framework import filters


class CustomSearchFilter(filters.SearchFilter):
    """Custom search filter"""
    search_param = 'search'
