from django.contrib import admin

# Register your models here.
from search.models import Product, Shop


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'image_link')
    search_fields = ('product_src_id', 'name',)

admin.site.register(Product, ProductAdmin)
admin.site.register(Shop)
