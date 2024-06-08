from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _



class ProductCategoryModel(models.Model):
    name = models.CharField(max_length=128, verbose_name=_('name'))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Product Category')
        verbose_name_plural = _('Product Categories')


class ProductTagModel(models.Model):
    name = models.CharField(max_length=128, verbose_name=_('name'))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Product Tag')
        verbose_name_plural = _('Product Tags')


class ProductColorModel(models.Model):
    name = models.CharField(max_length=128, verbose_name=_('name'))
    code = models.CharField(max_length=7)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Product Color')
        verbose_name_plural = _('Product Colors')


class ProductSizeModel(models.Model):
    name = models.CharField(max_length=128,verbose_name=_('name'))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Product Size')
        verbose_name_plural = _('Product Sizes')


class ProductManufacture(models.Model):
    name = models.CharField(max_length=128, verbose_name=_('name'))
    logo = models.ImageField(null=True, blank=True, upload_to='manufacture/')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Product Manufacture')
        verbose_name_plural = _('Product Manufactures')


class ProductModel(models.Model):
    image1 = models.ImageField(upload_to='products/')
    image2 = models.ImageField(upload_to='products/')

    name = models.CharField(max_length=255, verbose_name=_('name'))
    long_description = models.TextField(verbose_name=_('long_description'))
    short_description = models.CharField(max_length=255, verbose_name=_('short_description'))
    price = models.DecimalField(max_digits=7, decimal_places=2)
    discount = models.PositiveSmallIntegerField(default=0,
                                                validators=
                                                [MaxValueValidator(100), MinValueValidator(0)]
                                                )
    sku = models.CharField(max_length=10, unique=True)
    count = models.PositiveIntegerField()
    real_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    manufacture = models.ForeignKey(ProductManufacture, on_delete=models.CASCADE, related_name='products')
    colors = models.ManyToManyField(ProductColorModel, related_name='products')
    tags = models.ManyToManyField(ProductTagModel, related_name='products')
    categories = models.ManyToManyField(ProductCategoryModel, related_name='products')
    sizes = models.ManyToManyField(ProductSizeModel, related_name='products')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def is_discount(self):
        return self.discount != 0

    def is_available(self):
        return self.count != 0

    def get_price(self):
        if self.is_discount():
            return self.price - self.discount * self.price / 100

    def get_related_products(self):
        return ProductModel.objects.filter(categories=1).exclude(pk=self.pk)[:3]

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')


class ProductImageModel(models.Model):
    image = models.ImageField(upload_to='products/')
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='images')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = 'image'
        verbose_name_plural = 'images'

UserModel = get_user_model()

class ProductCommentModel(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='comments')
    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')