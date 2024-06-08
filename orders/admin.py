from django.contrib import admin

from orders.models import OrderModel, OrderItem


@admin.register(OrderModel)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'created_at', 'updated_at',)
    list_filter = ('created_at', 'status',)


@admin.register(OrderItem)
class OrderItemModelAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'quantity', 'price', 'size',)
    list_filter = ('product_name',)
