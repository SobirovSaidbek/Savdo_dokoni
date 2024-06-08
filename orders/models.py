from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


from products.models import ProductModel

UserModel = get_user_model()

class OrderModel(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='orders')
    status = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')


class OrderItem(models.Model):
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(ProductModel, on_delete=models.SET_NULL, related_name='orders', null=True)
    product_name = models.CharField(max_length=255, verbose_name=_('product_name'))
    quantity = models.PositiveSmallIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.CharField(max_length=128, verbose_name=_('size'))
    image1 = models.ImageField(upload_to='orders')
    image2 = models.ImageField(upload_to='orders')

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = _('order item')
        verbose_name_plural = _('orders items')
