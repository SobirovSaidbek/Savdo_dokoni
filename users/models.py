from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

UserModel = get_user_model()


class VerificationCodeModel(models.Model):
    code = models.CharField(max_length=6, unique=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='verification_codes')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = _('Verification Code')
        verbose_name_plural = _('Verification Codes')


class AccountModel(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='account')
    full_name = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('full_name'))
    company = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('company'))
    city = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('city'))
    address = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('address'))
    postcode = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True, verbose_name=_('phone'))
    country = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'

