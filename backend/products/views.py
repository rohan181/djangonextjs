from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, filters
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(available=True)
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description', 'category__name']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by featured
        featured = self.request.query_params.get('featured')
        if featured:
            queryset = queryset.filter(featured=True)
            
        # Filter by category
        category_slug = self.request.query_params.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
            
        return queryset