from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'image', 'parent', 'children', 'featured']
    
    def get_children(self, obj):
        # Only get direct children, not all descendants
        children = obj.children.all()
        if children:
            return CategorySerializer(children, many=True).data
        return []