from django import forms


class OrderModelForm(forms.ModelForm):
    phone = forms.CharField(max_length=128)
    address = forms.CharField(max_length=255)
