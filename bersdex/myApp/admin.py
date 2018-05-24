from django.contrib import admin

# Register your models here.
from .models import Products, Category

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name', )}

admin.site.register(Category, CategoryAdmin)    

class ItemModelAdmin(admin.ModelAdmin):
    list_display = ["title", "created_at", "is_original"]
    list_display_links = ["title"]
    list_filter = ["created_at", "is_original"]
    search_fields = ["title", "body"]
    class Meta:
        model = Products
        verbose_name_plural = "Product"


admin.site.register(Products, ItemModelAdmin)