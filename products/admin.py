from django.contrib import admin
from products.models import *


@admin.register(ProductManufacture)
class ProductManufactureAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at',)
    search_fields = ('name',)
    list_filter = ('name', 'created_at',)


@admin.register(ProductColorModel)
class ProductColorModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'created_at',)
    search_fields = ('name',)
    list_filter = ('name', 'created_at',)


@admin.register(ProductTagModel)
class ProductTagModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at',)
    search_fields = ('name',)
    list_filter = ('name', 'created_at',)


@admin.register(ProductSizeModel)
class ProductSizeModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at',)
    search_fields = ('name',)
    list_filter = ('name', 'created_at',)


@admin.register(ProductCategoryModel)
class ProductCategoryModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at',)
    search_fields = ('name',)
    list_filter = ('name', 'created_at',)


class ProductImageModelAdmin(admin.StackedInline):
    model = ProductImageModel


@admin.register(ProductModel)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'discount', 'created_at',)
    search_fields = ('name', 'short_description', 'long_description')
    list_filter = ('created_at', 'updated_at')
    inlines = [ProductImageModelAdmin]
    readonly_fields = ['real_price']


@admin.register(ProductCommentModel)
class ProductCommentModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'message', 'created_at', 'updated_at',)
    search_fields = ['message']
    list_filter = ('created_at', 'updated_at',)