from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.utils.html import format_html
from .models import Category

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'featured', 'order', 'display_image', 'created_at')
    list_filter = ('featured', 'parent')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('featured', 'order')
    
    # Display hierarchy in dropdown
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "parent":
            kwargs["queryset"] = Category.objects.all().order_by('name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    # Display thumbnail in list view
    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.image.url)
        return "No Image"
    display_image.short_description = 'Thumbnail'

    # Make slug field readonly after creation
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return ('slug',)
        return ()

admin.site.register(Category, CategoryAdmin)