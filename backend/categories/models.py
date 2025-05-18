from django.db import models

# Create your models here.


from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', null=True, blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    @property
    def has_children(self):
        return self.children.exists()

    # Method to get full category path for breadcrumbs
    def get_ancestors(self):
        ancestors = []
        category = self.parent
        
        while category:
            ancestors.insert(0, category)
            category = category.parent
            
        return ancestors