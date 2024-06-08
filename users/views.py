import pytz
from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, FormView, UpdateView, ListView
from sympy import Product

from conf import settings
from products.models import ProductModel
from users.forms import RegisterForm, EmailVerificationForm, LoginForm, AccountModelForm
from users.models import VerificationCodeModel, AccountModel
import random

UserModel = get_user_model()


def send_email_verification(user):
    random_code = random.randint(100000, 999999)

    if VerificationCodeModel.objects.filter(code=random_code).exists():
        send_email_verification(user)

    else:
        VerificationCodeModel.objects.create(
            code=random_code,
            user=user
        )
        try:

            send_mail(
                'Verification Code',
                f'Your verification code is {random_code}',
                settings.EMAIL_HOST_USER, [user.email]
            )
            return True
        except Exception as e:
            return False


class RegisterView(CreateView):
    template_name = 'users/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('users:verify-email')

    def form_valid(self, form):
        storage = messages.get_messages(self.request)
        storage.used = True
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        #send verification code
        send_email_verification(user)
        return super().form_valid(form)

    def form_invalid(self, form):
        storage = messages.get_messages(self.request)
        storage.used = True
        messages.error(self.request, form.errors)
        return self.render_to_response(self.get_context_data(form=form))


def verify_email(request):
    storage = messages.get_messages(request)
    storage.used = True
    if request.method == 'POST':
        form = EmailVerificationForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            user_code = VerificationCodeModel.objects.filter(code=code).first()
            if user_code:
                now = datetime.now(pytz.timezone(settings.TIME_ZONE))
                sent_time = user_code.created_at.astimezone(pytz.timezone(settings.TIME_ZONE)) + timedelta(minutes=2)
                if sent_time > now:
                    UserModel.objects.filter(pk=user_code.user.pk).update(is_active=True)
                    return redirect('users:login')

                else:
                    messages.error(request, 'Verification code is expired.')

            else:
                messages.error(request, 'This code is invalid')

        else:
            messages.error(request, form.errors)
    return render(request, 'users/verify-email.html')


class LoginView(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('pages:home')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
            return redirect(self.success_url)

        else:
            messages.error(self.request, 'Invalid username or password')

    def form_invalid(self, form):
        storage = messages.get_messages(self.request)
        storage.used = True
        messages.error(self.request, 'Form is invalid')

        return self.render_to_response(self.get_context_data(form=form))


def logout_view(request):
    if request.method == 'GET':
        logout(request)
        return redirect(reverse_lazy('pages:home'))


class AccountView(LoginRequiredMixin, UpdateView):
    template_name = 'users/acount.html'
    form_class = AccountModelForm
    success_url = reverse_lazy('users:account')
    context_object_name = 'account'
    login_url = reverse_lazy('users:login')

    def get_object(self, queryset=None):
        account, _ = AccountModel.objects.get_or_create(user=self.request.user)
        return account


class WishlistView(TemplateView):
    template_name = 'users/wishlist.html'


class CartView(ListView):
    template_name = 'users/cart.html'
    context_object_name = 'products'

    def get_queryset(self):
        cart = self.request.session.get('cart', [])
        products = ProductModel.objects.filter(pk__in=cart)
        return products

    def calculate_total_price(self):
        cart = self.request.session.get('cart', [])
        products = ProductModel.objects.filter(pk__in=cart)
        total_price = 0
        for product in products:
            total_price += product.get_price()
        return total_price

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_price'] = self.calculate_total_price()
        return context


class ChangePassword(TemplateView):
    template_name = 'users/reset-password.html'

