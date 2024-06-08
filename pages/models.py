from django.db import models
from django.utils.translation import gettext_lazy as _



class ContactModel(models.Model):
    name = models.CharField(max_length=128, verbose_name=_('name'))
    email = models.EmailField()
    subject = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('subject'))
    message = models.TextField(verbose_name=_('message'))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('contact')
        verbose_name_plural = _('contacts')


class UserCommentModel(models.Model):
    name = models.CharField(max_length=128, verbose_name=_('name'))
    comment = models.TextField(verbose_name=_('comment'))
    profession = models.CharField(max_length=128,verbose_name=_('profession'))
    image = models.ImageField(upload_to='media/')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('User Comment')
        verbose_name_plural = _('User Comments')