from django.urls import path

from orders.views import CheckoutView, order_create, order_history_view

app_name = 'orders'

urlpatterns = [
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('history/', order_history_view, name='history'),
    path('order/', order_create, name='order')
]