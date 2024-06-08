from django.urls import path

from products.views import ProductsListView, ProductDetailView, add_or_remove, add_or_remove_likes, ProductCommentView

app_name = 'products'

urlpatterns = [
    path('detail/<int:pk>/', ProductDetailView.as_view(), name='detail'),
    path('cart/<int:pk>/', add_or_remove, name='add-or-remove'),
    path('comment/<int:pk>/', ProductCommentView.as_view(), name='comment'),
    path('likes/<int:pk>/', add_or_remove_likes, name='add-or-remove-likes'),
    path('', ProductsListView.as_view(), name='list'),
]