from django import forms

from products.models import ProductCommentModel


class ProductCommentModelForm(forms.ModelForm):
    class Meta:
        model = ProductCommentModel
        fields = ['message']