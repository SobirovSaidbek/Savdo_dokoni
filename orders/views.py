from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView

from orders.forms import OrderModelForm
from orders.models import OrderModel, OrderItem
from products.models import ProductModel
from users.models import AccountModel


class CheckoutView(TemplateView):
    template_name = 'products/checkout.html'



@login_required
def order_create(request):
    if request.method == 'POST':
        form = OrderModelForm(request.POST)
        if form.is_valid():
            new_order = OrderModel.objects.create(user=request.user, status=False)
            cart = request.session.get('cart', None)
            if cart is None:
                return redirect('products:list')
            products = ProductModel.objects.filter(pk__in=cart)
            for product in products:
                OrderItem.objects.create(
                    product=product,
                    product_name=product.name,
                    quantity=1,
                    price=product.real_price,
                    size='test',
                    order=new_order,
                    image1=product.image1,
                    image2=product.image2,
                )
            request.session['cart'] = []

            return redirect('orders:history')
        else:
            return render(request, 'products/checkout.html')


@login_required
def order_history_view(request):
    if request.method == 'GET':
        orders = OrderModel.objects.filter(user=request.user)
        context = {'orders': orders}
        return render(request, 'users/order-history.html', context)