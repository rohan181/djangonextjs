from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Category
from .serializers import CategorySerializer

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    
    @action(detail=False, methods=['get'])
    def root_categories(self, request):
        """Get only root categories (no parent)"""
        categories = Category.objects.filter(parent=None)
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured categories"""
        categories = Category.objects.filter(featured=True)
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def products(self, request, slug=None):
        """Get products for a specific category and its subcategories"""
        category = self.get_object()
        
        # Get this category's products
        products = category.products.filter(available=True)
        
        # Also get products from all subcategories
        subcategories = self.get_subcategories(category)
        for subcategory in subcategories:
            products |= subcategory.products.filter(available=True)
        
        from products.serializers import ProductSerializer
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    def get_subcategories(self, category):
        """Helper method to get all subcategories recursively"""
        subcategories = list(category.children.all())
        for subcategory in list(subcategories):
            subcategories.extend(self.get_subcategories(subcategory))
        return subcategories