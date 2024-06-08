from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView

from products.forms import ProductCommentModelForm
from products.models import ProductModel, ProductCategoryModel, ProductColorModel, ProductTagModel, ProductManufacture, \
    ProductImageModel, ProductCommentModel


class ProductsListView(ListView):
    template_name = 'products/product-list.html'
    model = ProductModel
    context_object_name = 'products'

    @staticmethod
    def change_colors_structure():
        colors = ProductColorModel.objects.all()
        colors_list = []
        temp_colors = []

        for color in colors:
            temp_colors.append(color)
            if len(temp_colors) == 2:
                colors_list.append(temp_colors)
                temp_colors = []  # Reset temp_colors to a new list after appending

        # Append any remaining colors in temp_colors if it is not empty
        if temp_colors:
            colors_list.append(temp_colors)

        return colors_list

    def get_queryset(self):
        products = self.model.objects.all().order_by('-created_at')
        tag = self.request.GET.get('tag')
        cat = self.request.GET.get('cat')
        col = self.request.GET.get('col')
        man = self.request.GET.get('man')
        sort = self.request.GET.get('sort')
        q = self.request.GET.get('q')

        if tag:
            products = products.filter(tags__in=tag)
        if cat:
            products = products.filter(categories__in=cat)
        if col:
            products = products.filter(colors__in=col)
        if man:
            products = products.filter(manufacture__in=man)
        if sort:
            if sort == '-price':
                products = products.order_by('-real_price')
            else:
                products = products.order_by('real_price')
        if q:
            products = products.filter(name__icontains=q)

        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ProductCategoryModel.objects.all()
        context['manufactures'] = ProductManufacture.objects.all()
        context['tags'] = ProductTagModel.objects.all()
        context['colors'] = ProductColorModel.objects.all()
        return context


class ProductDetailView(DetailView):
    template_name = 'products/product-detail.html'
    model = ProductModel
    context_object_name = 'product'

    @staticmethod
    def change_colors_structure():
        colors = ProductColorModel.objects.all()
        colors_list = []
        temp_colors = []

        for color in colors:
            temp_colors.append(color)
            if len(temp_colors) == 2:
                colors_list.append(temp_colors)
                temp_colors = []  # Reset temp_colors to a new list after appending

        # Append any remaining colors in temp_colors if it is not empty
        if temp_colors:
            colors_list.append(temp_colors)

        return colors_list

    def get_context_data(self, *, object_list=None,  **kwargs):
        product = ProductModel.objects.get(id=self.kwargs["pk"])
        context = super().get_context_data(**kwargs)
        context.update({
            'comments': product.comments.all(),
            'products': ProductModel.objects.all(),
            'categories': ProductCategoryModel.objects.all(),
            'manufactures': ProductManufacture.objects.all(),
            'tags': ProductTagModel.objects.all(),
            'colors': ProductColorModel.objects.all()
        })
        return context


def add_or_remove(request, pk):
    cart = request.session.get('cart', [])
    if pk in cart:
        cart.remove(pk)

    else:
        cart.append(pk)

    request.session['cart'] = cart
    return redirect(request.GET.get('next', 'products:list'))


def add_or_remove_likes(request, pk):
    likes = request.session.get('likes', [])
    if pk in likes:
        likes.remove(pk)

    else:
        likes.append(pk)

    request.session['likes'] = likes
    return redirect(request.GET.get('nextt', 'products:list'))


class ProductCommentView(LoginRequiredMixin, CreateView):
    template_name = 'products/product-detail.html'
    form_class = ProductCommentModelForm
    login_url = reverse_lazy('users:login')

    def form_valid(self, form):
        product_id = self.kwargs['pk']
        product = ProductModel.objects.get(pk=product_id)
        comment = form.save(commit=False)
        comment.user = self.request.user
        comment.product = product
        comment.save()
        return self.get_success_url()

    def form_invalid(self, form):
        return self.success_url()

    def get_success_url(self):
        return redirect(self.request.GET.get('next', 'products:list'))