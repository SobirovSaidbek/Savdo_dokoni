from django.contrib import admin

from pages.models import ContactModel, UserCommentModel


@admin.register(ContactModel)
class ContactModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at',)
    search_fields = ('name', 'email', 'subject',)
    list_filter = ('email', 'created_at',)


@admin.register(UserCommentModel)
class UserCommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at',)
    search_fields = ('name', 'created_at',)
    list_filter = ('created_at',)