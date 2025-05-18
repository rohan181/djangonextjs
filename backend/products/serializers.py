from rest_framework import serializers
from .models import Product
from categories.serializers import CategorySerializer

class ProductSerializer(serializers.ModelSerializer):
    category_detail = CategorySerializer(source='category', read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'price', 
            'category', 'category_detail', 'image', 'featured',
            'stock', 'available', 'created_at'
        ]





  
        