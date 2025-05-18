from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.utils.html import format_html
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'stock', 'available', 'featured', 'display_image', 'created_at')
    list_filter = ('available', 'featured', 'category')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('price', 'stock', 'available', 'featured')
    readonly_fields = ('created_at', 'updated_at')
    
    # Make slug field readonly after creation

    
    # Display thumbnail in list view
    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.image.url)
        return "No Image"
    display_image.short_description = 'Thumbnail'
    
    # Customize the filter for category to show hierarchy
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category":
            from categories.models import Category
            # Get all categories and format their names to show hierarchy
            categories = Category.objects.all()
            for category in categories:
                ancestors = category.get_ancestors()
                if ancestors:
                    prefix = " > ".join([a.name for a in ancestors])
                    category.name = f"{prefix} > {category.name}"
            kwargs["queryset"] = categories.order_by('name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Product, ProductAdmin)